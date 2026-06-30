import face_recognition 
import json
import csv 
import os
import threading
import calendar
import time
from datetime import datetime
from flask import Flask, request, jsonify, Response
import cv2
import numpy as np
import base64
from flask_cors import CORS, cross_origin
import bcrypt

# CRITICAL: Import init_database from database.py to ensure tables are created
from database import init_database

# Initialize the database when the Flask app starts
app = Flask(__name__)

@app.after_request
def add_header(response):
    """Ensure API responses are never cached by the browser."""
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=True
)

from core_logic import (
    calculate_monthly_payroll,
    register_new_user,
    create_reset_token,
    authenticate_user,
    load_users,
    save_users,
    load_leaves,
    save_leaves,
    load_encodings,
    save_encodings,
    enroll_new_staff_core,
    log_shift_clocking_api,
    get_full_shift_log,
    get_staff_shift_log,
    detect_and_recognize_multiple_faces,
    is_attendance_window_active,
    get_staff_total_clockings,
    get_registered_staff_count,
    get_present_today_count,
    get_face_encoding,
    update_staff_face_encodings,
    search_staff_logic,
    update_staff_record,
    is_in_shift_window, # Used in video_feed and check_shift_window
    SHIFT_WINDOWS, # Used in is_in_shift_window
    verify_and_reset_password_logic
)

ROLE_MAP = {
    "System Administrator": "Admin",
    "shift_supervisor": "shift supervisor",
    "staff_member": "Staff"
}


LEAVES_FILE = "leave_requests.json"
camera_status = {"running": False, "supervisor_id": None}

recorded_ids = set()
first_seen_time = {}
face_history = {}   

last_logged = {}
face_history = {}

def is_likely_real_face(pid, current_time, box):
    """Anti-spoofing: Detects natural movement"""
    global face_history
    top, right, bottom, left = box
    center_x = (left + right) // 2

    key = pid
    if key not in face_history:
        face_history[key] = []

    face_history[key].append((current_time, center_x))
    face_history[key] = [entry for entry in face_history[key] if current_time - entry[0] < 1.8]

    if len(face_history[key]) < 6:
        return True

    xs = [p[1] for p in face_history[key]]
    movement = max(xs) - min(xs)
    return movement >= 5


@app.route('/api/video_feed')
def video_feed():
    return Response(generate_streaming_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_streaming_frames():
    """Camera stays OPEN during full window - Multiple staff friendly"""
    print("🎥 Camera Started - Full Window Mode (Multiple Staff Ready)")

    camera = None
    for i in [0, 1, 2]:
        if os.name == 'nt':
            camera = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        else:
            camera = cv2.VideoCapture(i)
        if camera.isOpened():
            print(f"✅ Camera opened on index {i}")
            break

    if not camera or not camera.isOpened():
        print("❌ Failed to open camera!")
        return

    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    try:
        db = load_encodings()
        known_encodings = [np.array(enc) for enc in db.get('Encodings', [])]
        known_ids = db.get('IDs', [])
        known_names = db.get('Names', [])
        camera_status["running"] = True

        global last_logged
        last_logged = {}   # Reset cooldowns when stream starts

        while camera_status.get("running", True):
            success, frame = camera.read()
            if not success:
                time.sleep(0.08)
                continue

            shift_type = is_in_shift_window()
            current_time = time.time()

            if not shift_type:
                # Window closed
                cv2.rectangle(frame, (0, 0), (640, 90), (0, 0, 100), -1)
                cv2.putText(frame, "ATTENDANCE WINDOW CLOSED", (70, 55),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 3)
            else:
                # === PROCESSING DURING OPEN WINDOW ===
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_small)
                face_encodings = face_recognition.face_encodings(rgb_small, face_locations)

                for (top, right, bottom, left), encoding in zip(face_locations, face_encodings):
                    top, right, bottom, left = top*4, right*4, bottom*4, left*4

                    face_area = (bottom - top) * (right - left)
                    if face_area < 9000:   # Only process decent sized faces
                        continue

                    distances = face_recognition.face_distance(known_encodings, encoding)
                    min_dist = np.min(distances) if len(distances) > 0 else 1.0

                    name = "Unknown"
                    pid = "Unknown"
                    color = (0, 165, 255)  # Orange = scanning

                    if min_dist < 0.40:
                        idx = np.argmin(distances)
                        name = known_names[idx]
                        pid = str(known_ids[idx])

                        # Anti-spoof + Logging
                        if is_likely_real_face(pid, current_time, (top, right, bottom, left)):
                            if (pid not in last_logged or current_time - last_logged[pid] > 60):
                                last_logged[pid] = current_time
                                threading.Thread(
                                    target=log_shift_clocking_api,
                                    args=(pid, name),
                                    daemon=True
                                ).start()

                                color = (0, 255, 0)
                                # Success banner (stays for ~3-4 seconds due to cooldown)
                                cv2.rectangle(frame, (left-10, top-100), (right+10, top-45), (0, 200, 0), -1)
                                cv2.putText(frame, "✅ ATTENDANCE SAVED!", (left+5, top-65),
                                            cv2.FONT_HERSHEY_DUPLEX, 0.95, (255, 255, 255), 2)

                        else:
                            color = (0, 0, 255)  # Red = suspicious

                    # Always show name and ID clearly
                    cv2.rectangle(frame, (left, top), (right, bottom), color, 3)
                    cv2.putText(frame, f"{name} ({pid})", (left + 8, top - 12),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.82, (255, 255, 255), 2)

                # Top status banner - always visible during window
                cv2.rectangle(frame, (0, 0), (640, 58), (25, 35, 55), -1)
                cv2.putText(frame, f"ACTIVE {shift_type.upper()} SHIFT - Next Staff Please", 
                            (35, 42), cv2.FONT_HERSHEY_SIMPLEX, 0.85, (0, 255, 255), 2)

            # Encode and stream
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

            time.sleep(0.035)  # Smooth streaming

    except Exception as e:
        print(f"❌ Camera Error: {e}")
    finally:
        if camera and camera.isOpened():
            camera.release()
        print("🎥 Camera stream ended.")
                                            
def get_staff_department(staff_id):
    """
    Retrieves the department for a given staff member.
    """
    if staff_id == "1001":
        return "Computing"
    return "General"
    
@app.route('/api/start_shift_logging', methods=['POST'])
def start_shift_logging():
    try:
        data = request.get_json()
        supervisor_id = data.get('supervisor_id', 'Unknown')
        
        print(f"New shift started by Supervisor {supervisor_id}: Memory and Timers cleared.")
        
        # Ensure your response looks EXACTLY like this dictionary format:
        return jsonify({
            "status": "success",
            "success": True,
            "message": f"Shift initialized successfully by {supervisor_id}"
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "success": False, "message": str(e)}), 500        
         
@app.route("/api/stop_attendance", methods=["POST"])
def stop_attendance():
    camera_status["running"] = False
    camera_status["supervisor_id"] = None
    return jsonify(status="success", message="Attendance stopped"), 200

from datetime import datetime

def is_camera_window_open():
    from datetime import datetime
    now = datetime.now()
    hour = now.hour

    # Match the HTML windows: 
    # Day Shift: 09:00 to 13:00 (1 PM) | Night Shift: 17:00 to 23:00 (11 PM)
    if (9 <= hour < 13) or (17 <= hour < 23):
        return True
    return False

@app.route('/api/check_shift_window', methods=['GET'])
def check_shift_window():
    shift = is_in_shift_window()
    if shift:
        action = "Clock In" if "in" in shift else "Clock Out"
        return jsonify({
            "success": True, 
            "shift_type": shift,
            "action": action,
            "message": f"{action} window is OPEN"
        })
    return jsonify({
        "success": False, 
        "message": "Attendance is currently closed."
    })
    
# 2. Add the route here
@app.route('/api/process_frame', methods=['POST'])
def process_frame():
    if not is_camera_window_open():
        return jsonify({
            "status": "closed", 
            "message": "Camera is disabled outside of shift hours (2-3 & 11-12)."
        }), 403

    # If window is open, proceed with recognition
    # (Call the function you already have in core_logic)
    # ... existing recognition code ...
    return jsonify({"status": "success", "data": "attendance_logged"})
    now = datetime.now().time()
    
    # Morning Window: 02:00 to 03:00 (2-3 hr)
    morning_start = now.replace(hour=8, minute=0, second=0, microsecond=0)
    morning_end = now.replace(hour=9, minute=0, second=0, microsecond=0)
    
    # Evening/Clock-out Window: 11:00 to 12:00 (11-12 hr)
    evening_start = now.replace(hour=20, minute=0, second=0, microsecond=0)
    evening_end = now.replace(hour=24, minute=0, second=0, microsecond=0)

    if morning_start <= now <= morning_end:
        return True, "Morning Shift"
    elif evening_start <= now <= evening_end:
        return True, "Evening Shift"
    
    return False, None

# -------------------------------------------------
@app.route("/api/register_user", methods=["POST"])
def register_user():
    data = request.get_json() or {}
    name = data.get("name")
    password = data.get("password")
    role = data.get("role")
    
    # CRITICAL FIX: Get the ACTUAL ID from the frontend form
    # Make sure your frontend JavaScript is sending 'staff_id'
    # in the body.
    actual_id = data.get("staff_id") 

    # We validate that all fields, including the ID, are present
    if not all([name, password, role, actual_id]):
        return jsonify(status="error", message="Missing fields. Did you provide an ID?"), 400

    # Strip whitespaces and force string to prevent formatting issues
    clean_id = str(actual_id).strip()
    
    # We pass the ID we received directly to the logic layer
    success, msg = register_new_user(name, password, role, clean_id)
    return jsonify(status="success" if success else "error", message=msg)

@app.route('/api/login', methods=['POST'])
def login():
    print("--- LOGIN START ---")
    try:
        data = request.get_json()
        if not data:
            print("ERROR: No JSON data received")
            return jsonify({"message": "Missing JSON"}), 400
            
        u_id = data.get('user_id')
        u_pass = data.get('password')
        print(f"DEBUG: Attempting ID {u_id}")

        user = authenticate_user(u_id, u_pass)
        
        if user:
            print(f"DEBUG: Login Success for {u_id}")
            return jsonify({
                "status": "success",
                "user_id": u_id,
                "role": user.get("role"),
                "user_name": user.get("name"),
                "is_first_login": user.get("is_first_login", False)
            }), 200
        else:
            print("DEBUG: Login Failed - Invalid Credentials")
            return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    except Exception as e:
        print(f"!!! CRASH IN LOGIN ROUTE: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route('/api/request-password-reset', methods=['POST'])
def request_password_reset():
    """
    Generates a 6-digit token. 
    DOES NOT return it to the frontend.
    Prints to server console for Admin/Admin verification.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"message": "Staff ID is required."}), 400

        users = load_users()
        # Check if user exists first to prevent unnecessary token generation
        if user_id not in users:
            # Optional: Hide whether user exists for security, or reveal it for convenience.
            # Here we hide it to prevent user enumeration.
            return jsonify({"message": "If the account exists, a reset code has been generated."}), 200
        
        # 1. Generate the secure token (this also invalidates old ones)
        token = create_reset_token(user_id)
        
        # 2. LOG IT TO CONSOLE (For the Admin/Developer to see)
        print(f"🔐 PASSWORD RESET TOKEN FOR {user_id}: {token}")
        
        # 3. Return success WITHOUT the token
        return jsonify({
            "message": "If the account exists, a reset code has been generated. Please contact the Administrator.",
            "status": "success"
        }), 200
        
    except Exception as e:
        print(f"CRITICAL ERROR IN RESET REQUEST: {e}")
        return jsonify({"message": "Server error occurred."}), 500
    
@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    """
    Verifies the token using the 3 checks (ID, Used=False, Time < 15min)
    and updates the password if successful.
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id')
        token = data.get('token')
        new_password = data.get('new_password')
        
        if not all([user_id, token, new_password]):
             return jsonify({"message": "Missing data fields."}), 400

        # 1. Verify token and update password via Core Logic
        # This function checks: ID match, Used=0, Time < Expired
        success, message = verify_and_reset_password_logic(user_id, token, new_password)
        
        if success:
            return jsonify({"message": message, "status": "success"}), 200
        else:
            return jsonify({"message": message}), 400
            
    except Exception as e:
        print(f"RESET PASSWORD ERROR: {e}")
        return jsonify({"message": "Server error processing reset."}), 500
    
        
@app.route('/api/complete_setup', methods=['POST']) # This route seems unused, but keeping for now
def complete_setup():
    data = request.json
    user_id = data.get('user_id')
    new_password = data.get('new_password')
    
    users = load_users()
    if user_id in users:
        # Hash the new password using bcrypt
        hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
        users[user_id]['password_hash'] = hashed.decode('utf-8')
        users[user_id]['is_first_login'] = False
        save_users(users)
        return jsonify({"message": "Setup complete"}), 200
    return jsonify({"message": "User not found"}), 404


@app.route("/api/setup_password", methods=["POST"])
def setup_password():
    try:
        data = request.get_json()
        # Ensure we catch both 'id' and 'user_id' just in case
        staff_id = str(data.get("user_id") or data.get("id")).strip()
        new_password = data.get("new_password")

        if not staff_id or not new_password:
            return jsonify({"status": "error", "message": "Missing ID or Password"}), 400

        users = load_users()

        if staff_id in users:
            # 1. Hash the new password
            from core_logic import generate_bcrypt_hash
            users[staff_id]["password_hash"] = generate_bcrypt_hash(new_password)
            
            # 2. CRITICAL: Set first login to False
            users[staff_id]["is_first_login"] = False
            
            # 3. Save back to users.json
            save_users(users)
            
            print(f"✅ Success: Password updated in users.json for {staff_id}")
            return jsonify({"status": "success", "message": "Password updated successfully"})
        else:
            print(f"❌ Error: ID {staff_id} not found in users.json keys: {list(users.keys())}")
            return jsonify({"status": "error", "message": "User ID not found in database"}), 404

    except Exception as e:
        print(f"❌ Server Error: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
    

@app.route("/api/enroll_staff", methods=["POST"])
def enroll_staff():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
    
    s_id = str(data.get("staff_id", "")).strip()
    
    # Use explicit variables to ensure they aren't lost
    name = data.get("full_name")
    dept = data.get("department")
    sex = data.get("sex") 
    salary = float(data.get("base_monthly_salary", 0))
    overtime = float(data.get("overtime_rate", 0))
    caps = int(data.get("num_captures", 5))

    print(f"DEBUG: Processing {s_id}, Sex={sex}, Salary={salary}")

    try:
        # Run core with parameters
        enroll_new_staff_core(s_id, name, dept, sex, salary, overtime, caps)

        users = load_users()
        users[s_id] = {
            "id": s_id,
            "name": name,
            "sex": sex,
            "password_hash": bcrypt.hashpw(f"Hosp_{s_id}".encode(), bcrypt.gensalt()).decode(),
            "role": "staff",
            "department": dept,
            "base_monthly_salary": salary,
            "overtime_rate": overtime,
            "is_first_login": True
        }
        save_users(users)
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
            
# DASHBOARD
# -------------------------------------------------

@app.route("/api/dashboard_metrics")
def dashboard():
    return jsonify(
        status="success",
        total_staff=get_registered_staff_count(),
        present_today=get_present_today_count(),
        shift_running=camera_status["running"]
    )
    
# Look for your "LEAVE MANAGEMENT" section in flask_api.py and add this route:
@app.route('/api/admin/all_requests', methods=['GET'])
def get_all_requests():
    try:
        # Use the global LEAVES_FILE variable defined at the top of flask_api.py
        leaves = load_leaves()
        return jsonify(leaves), 200
    except Exception as e:
        print(f"Error fetching admin leaves: {e}")
        return jsonify({"error": str(e)}), 500
        
    
@app.route('/api/admin_stats', methods=['GET'])
def get_admin_stats():
    try:
        users_dict = load_users()
        face_data = load_encodings()
        today_present_count = get_present_today_count()   # ← Now more accurate

        staff_count = sum(1 for u in users_dict.values() if u.get('role') in ['staff', 'staff_member'])
        
        face_ids = face_data.get('IDs', [])
        enrolled_count = len(set(face_ids))

        stats_data = {
            "total_staff": staff_count,
            "enrolled_faces": enrolled_count,
            "present_today": today_present_count   # ← Updated
        }

        return jsonify(stats_data), 200

    except Exception as e:
        print(f"Error syncing dashboard: {e}")
        return jsonify({"total_staff": 0, "enrolled_faces": 0, "present_today": 0}), 200
     
 
 
    
def get_ethiopian_shift_type(time_str):
    """
    Fixed shift classification using Local Time cutoff.
    Day Shift: 06:00 AM to 17:59 PM
    Night Shift: 18:00 PM to 05:59 AM
    """
    try:
        hour = int(time_str.split(":")[0])
        
        # Logic: If hour is between 6 (inclusive) and 18 (exclusive), it's Day.
        # Anything else (18:00 to 05:59) is Night.
        if 6 <= hour < 18:
            return "Day"
        else:
            return "Night"
    except:
        return "Day"  

@app.route("/api/attendance_report/<date>", methods=["GET"])
@app.route("/api/get_report", methods=["GET"])
def attendance_report(date=None):
    try:
        if not date:
            date = request.args.get('date')
        if not date:
            return jsonify({"status": "error", "message": "Missing date"}), 400

        target_date = str(date).strip()
        role = request.args.get('role', '').lower()
        user_id = request.args.get('user_id')

        # Handle Role-Based Access Control (RBAC)
        # If the user is Staff, restrict the data to their own ID only
        if role in ['staff', 'staff_member']:
            if not user_id:
                return jsonify({"status": "error", "message": "User ID required for restricted role"}), 400
            all_records = get_staff_shift_log(user_id, filter_date=target_date)
            print(f"🔒 Restricted Report: Loading logs for Staff {user_id}")
        else:
            all_records = get_full_shift_log() 
            print(f"📊 Admin Report: Loading all records for {target_date}")

        day_shift = []
        night_shift = []
        
        for rec in all_records:
            csv_date = str(rec.get('Date', '')).strip()
            if csv_date == target_date:
                check_in = rec.get('Check_In', '--:--:--')
                check_out = rec.get('Check_Out', '--:--:--')
                
                # Status logic: Check-In + Check-Out = Present, Check-In only = Incomplete
                status = "Present" if check_out not in ["", "-", "--:--:--"] else "Incomplete Shift"

                normalized_record = {
                    "id": rec.get('ID'),
                    "name": rec.get('Name'),
                    "dept": rec.get('Department', 'General'),
                    "date": rec.get('Date'),
                    "clock_in": check_in,
                    "clock_out": check_out,
                    "status": status
                }
                
                shift_type = get_ethiopian_shift_type(normalized_record["clock_in"])
                print(f"Record {rec.get('ID')} at {normalized_record['clock_in']} -> {shift_type} Shift")
                
                if shift_type == "Day":
                    day_shift.append(normalized_record)
                else:
                    night_shift.append(normalized_record)
        
        print(f"✅ Final: Day={len(day_shift)}, Night={len(night_shift)}")

        return jsonify({
            "status": "success",
            "day_shift": day_shift,
            "night_shift": night_shift
        }), 200

    except Exception as e:
        print(f"❌ Report Error: {e}")
        return jsonify({
            "status": "error",
            "day_shift": [],
            "night_shift": []
        }), 500
               
            
@app.route("/api/my_attendance_report/<staff_id>/<date>", methods=["GET"])
@cross_origin(supports_credentials=True)
def my_attendance_report(staff_id, date):
    try:
        # Clean down lookup string keys
        target_staff_id = str(staff_id).strip()
        target_date = str(date).strip()
        
        all_records = get_full_shift_log() or [] 
        my_records = []
        
        for rec in all_records:
            # Handle every key schema variant used across your data lifecycle layers
            rec_id = str(rec.get('ID') or rec.get('staff_id') or rec.get('id') or "").strip()
            rec_date = str(rec.get('Date') or rec.get('date') or "").strip()
            
            if rec_id == target_staff_id and rec_date == target_date:
                # Calculate shifts safely based on local check-in markers
                check_in_time = rec.get('Check_In') or rec.get('clock_in') or rec.get('time') or ""
                rec['shift_type'] = get_ethiopian_shift_type(check_in_time)
                
                # Copy properties safely to avoid missing rendering fields on components
                rec['staff_id'] = rec_id
                rec['name'] = rec.get('Name') or rec.get('name') or "Hospital Staff"
                rec['date'] = rec_date
                my_records.append(rec)
                
        print(f"SECURITY CONTEXT: Sandboxed {len(my_records)} logs exclusively for Worker ID: {target_staff_id}")
        return jsonify(my_records), 200
        
    except Exception as e:
        print(f"CRITICAL BOUNDARY RUNTIME FAULT: {e}")
        return jsonify([]), 500
    
    
    

@app.route("/api/monthly_summary/<month_year>", methods=["GET"])
@cross_origin(supports_credentials=True)
def monthly_summary(month_year):
    try:
        STANDARD_DAYS = 30
        
        users = load_users()
        leaves = load_leaves()
        all_records = get_full_shift_log()  # Reads your CSV clocking database
        
        # 1. READ FRONTEND CLIENT IDENTIFIERS SENT VIA SEARCH HEADERS/QUERY PARAMS
        # This helps determine if the current request is from a regular staff member or an administrator
        requesting_id = request.args.get('user_id', '').strip()
        requesting_role = request.args.get('role', '').lower().strip()
        
        summary = []

        for s_id, u_info in users.items():
            current_staff_id = str(s_id).strip()
            current_role = str(u_info.get('role', '')).lower().strip()
            
            # Skip records that do not belong to basic staff members
            if current_role not in ['staff', 'staff_member']:
                continue
                
            # PRIVACY LAYER: If the caller is staff, instantly drop any records that aren't theirs
            if requesting_role in ['staff', 'staff_member'] and requesting_id != "":
                if current_staff_id != requesting_id:
                    continue

            # --- CALCULATE PRESENCE ---
            days_present = set()
            for rec in all_records:
                rec_id = str(rec.get('ID') or rec.get('staff_id') or "").strip()
                rec_date = str(rec.get('Date') or rec.get('date') or "").strip()
                check_out = str(rec.get('Check_Out') or "").strip()
                
                # Only count as present if the shift was completed (has Check_Out)
                if (rec_id == current_staff_id and rec_date.startswith(month_year) and 
                    check_out not in ["", "-", "None"]):
                    days_present.add(rec_date)
            
            present_count = len(days_present)
            
            # --- CALCULATE APPROVED LEAVES ---
            approved_leaves = sum(1 for l in leaves if str(l.get('staff_id', '')).strip() == current_staff_id 
                                 and str(l.get('status', '')).strip() == 'approved' 
                                 and month_year in str(l.get('start_date', '')))

            # --- CALCULATE ABSENCES ---
            absences = STANDARD_DAYS - present_count - approved_leaves
            if absences < 0: 
                absences = 0

            summary.append({
                "staff_id": current_staff_id,
                "name": u_info.get('name', 'Unknown'),
                "total_present": present_count,
                "approved_leaves": approved_leaves,
                "absent_days": absences,
                "performance": "⭐ Excellent" if present_count >= 25 else ("⚠️ Low Attendance" if absences > 5 else "Standard")
            })

        return jsonify(summary), 200
    except Exception as e:
        print(f"Error in summary processing engine: {e}")
        return jsonify([]), 500


PAYROLL_STORAGE_DIR = "finance_data"

if not os.path.exists(PAYROLL_STORAGE_DIR):
    os.makedirs(PAYROLL_STORAGE_DIR)

@app.route('/api/finance/get-report/<month>', methods=['GET'])
@cross_origin() # Ensures your frontend can access it without CORS blocks
def get_finance_report(month):
    file_path = os.path.join(PAYROLL_STORAGE_DIR, f"payroll_source_{month}.json")
    
    if not os.path.exists(file_path):
        return jsonify({"message": "No processed financial statement reports found"}), 404
        
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if isinstance(data, list):
            data = {"records": data}
            
        # Enrich data with latest names/departments from users.json
        users = load_users()
        for rec in data.get('records', []):
            u = users.get(str(rec.get('staff_id')))
            if u:
                rec['name'] = u.get('name', rec.get('name'))
                rec['department'] = u.get('department', rec.get('department'))
            
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"message": f"Error parsing report data: {str(e)}"}), 500
    
@app.route('/api/get_staff_list', methods=['GET'])
def get_staff_list_api():
    try:
        return jsonify(load_users()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/admin/send_to_finance', methods=['POST'])
def send_to_finance():
    data = request.get_json()
    month = data.get('month')
    file_path = os.path.join(PAYROLL_STORAGE_DIR, f"payroll_source_{month}.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
    return jsonify({"status": "success", "message": "Saved successfully!"}), 200



@app.route("/api/get_attendance_report", methods=["GET", "OPTIONS"])
@cross_origin()
def get_attendance_report_query():
    date = request.args.get("date")  # ?date=YYYY-MM-DD
    try:
        records = get_full_shift_log(filter_date=date)
        return jsonify(status="success", records=records), 200
    except Exception as e:
        return jsonify(status="error", message=str(e)), 500


# -------------------------------------------------
@app.route('/api/staff_metrics/<staff_id>', methods=['GET'])
def get_staff_metrics(staff_id):
    leaves = load_leaves()
    
    # Filter only the leaves for THIS staff member
    my_leaves = [l for l in leaves if str(l.get('staff_id')) == str(staff_id)]
    
    # Count them
    approved = sum(1 for l in my_leaves if l.get('status') == 'approved')
    denied = sum(1 for l in my_leaves if l.get('status') == 'denied')
    
    return jsonify({
        "approved_leaves": approved,
        "unexcused_absences": denied, # Denied requests show as unexcused
        "total_attended": get_staff_total_clockings(staff_id)
    }), 200
    
@app.route('/api/admin/staff_list', methods=['GET'])
def get_admin_staff_list():
    search_query = request.args.get('search', '').lower()
    
    # Load both sources of truth
    data = load_encodings()
    users = load_users() # Load the dictionary with salary data
    
    staff_records = []

    for i in range(len(data['IDs'])):
        s_id = str(data['IDs'][i])
        s_name = str(data['Names'][i]).lower()
        
        if not search_query or search_query in s_id or search_query in s_name:
            # Look up the salary/overtime in the users dictionary using the ID
            user_info = users.get(s_id, {})
            
            staff_records.append({
                "id": s_id,
                "name": data['Names'][i],
                "department": data['Departments'][i] if i < len(data['Departments']) else "N/A",
                "base_monthly_salary": user_info.get("base_monthly_salary", 0),
                "overtime_rate": user_info.get("overtime_rate", 0)
            })
            
            if len(staff_records) >= 20: break 
            
    return jsonify(staff_records)

@app.route('/api/admin/delete_staff/<staff_id>', methods=['DELETE'])
def delete_staff_api(staff_id):
    data = load_encodings()
    if staff_id in data['IDs']:
        idx = data['IDs'].index(staff_id)
        # Remove from all lists
        data['IDs'].pop(idx)
        data['Names'].pop(idx)
        data['Encodings'].pop(idx)
        if 'Departments' in data:
            data['Departments'].pop(idx)
        
        save_encodings(data)
        return jsonify({"success": True, "message": "Staff deleted successfully"})
    return jsonify({"success": False, "message": "Staff ID not found"}), 404


@app.route('/api/admin/update_staff', methods=['POST'])
def handle_update():
    try:
        req_data = request.json
        target_id = str(req_data.get('old_id'))
        new_id = str(req_data.get('new_id'))
        delete_face = req_data.get('delete_face', False)
        salary = req_data.get('salary')
        overtime = req_data.get('overtime')

        # Update the text records (Name, ID, Dept)
        success = update_staff_record(
            old_id=target_id,
            new_id=new_id,
            new_name=req_data.get('name'),
            new_dept=req_data.get('dept'),
            salary=salary,
            overtime=overtime,
            delete_face=delete_face
        )
        
        # If the user checked "Re-scan", we return a special status 
        # so the frontend knows to keep the camera modal open.
        return jsonify({
            "success": success, 
            "re_scan_triggered": delete_face
        })
        
    except Exception as e:
        print(f"CRITICAL ERROR DURING UPDATE: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
    



@app.route("/api/update_face_biometrics", methods=["POST", "OPTIONS"])
def update_face_biometrics():
    # HANDLE CORS PREFLIGHT REQUEST
    if request.method == "OPTIONS":
        response = jsonify({"status": "ok"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    try:
        print("UPDATE FACE API HIT")
        data = request.get_json()
        print("DATA RECEIVED:", data)

        staff_id = str(data.get("staff_id")).strip()
        images = data.get("images", [])

        # --- WRAP THE CORE LOGIC IN TRY/EXCEPT ---
        try:
            success, message = update_staff_face_encodings(staff_id, images)
        except Exception as core_error:
            print("CRASH IN CORE LOGIC:", core_error)
            # If core logic crashes, treat as failure
            success = False
            message = f"Processing Error: {str(core_error)}"

        response = jsonify({
            "status": "success" if success else "error",
            "message": message
        })

        response.headers.add("Access-Control-Allow-Origin", "*")
        # Return 200 OK even if logic failed, so frontend can read the error message
        return response

    except Exception as e:
        print("SERVER ROUTE ERROR:", str(e))
        response = jsonify({
            "status": "error",
            "message": f"Server Route Error: {str(e)}"
        })
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 500  
        
@app.route('/api/enroll_face_live', methods=['POST'])
@cross_origin(supports_credentials=True) # This route seems unused, but keeping for now
def enroll_face_live():
    data = request.get_json()
    staff_id = data.get('id')
    image_data = data.get('image')

    try:
        # Decode image
        header, encoded = image_data.split(",", 1)
        image_bytes = base64.b64decode(encoded)
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Get encoding
        boxes = face_recognition.face_locations(rgb_img)
        encodings = face_recognition.face_encodings(rgb_img, boxes)

        if len(encodings) == 1:
            # Use the functions we just imported
            db = load_encodings() 
            if staff_id in db['IDs']:
                idx = db['IDs'].index(staff_id)
                db['Encodings'][idx] = encodings[0].tolist()
                save_encodings(db) # This will now work!
                return jsonify({"success": True, "message": "Face updated!"})
            else:
                return jsonify({"success": False, "message": "ID not found"})
        else:
            return jsonify({"success": False, "message": "Face not detected clearly"})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"success": False, "message": str(e)}), 500
    
# ==================== UPDATE PASSWORD (First Login) ====================
@app.route('/api/update_password', methods=['POST']) # This route seems unused, but keeping for now
def update_password():
    try:
        data = request.get_json()
        staff_id = str(data.get('staff_id', '')).strip()
        new_password = data.get('new_password')

        print(f"🔍 Received staff_id: '{staff_id}'")   # ← Debug log

        if not staff_id or not new_password:
            return jsonify({"message": "Staff ID and password are required"}), 400

        users = load_users()
        print(f"Available user keys: {list(users.keys())}")   # ← Very useful debug

        user_key = None

        # Try to find user by key or by 'id' field
        for key in users.keys():
            if key == staff_id or users[key].get('id') == staff_id:
                user_key = key
                break

        if not user_key:
            return jsonify({
                "message": f"User not found. ID: {staff_id}. Available: {list(users.keys())}"
            }), 404

        # Update password
        from core_logic import generate_bcrypt_hash
        users[user_key]['password_hash'] = generate_bcrypt_hash(new_password)
        users[user_key]['is_first_login'] = False

        save_users(users)

        print(f"✅ Password updated successfully for: {staff_id}")
        return jsonify({"message": "Password updated successfully"}), 200

    except Exception as e:
        print(f"❌ Update Password Error: {e}")
        return jsonify({"message": f"Server error: {str(e)}"}), 500
    
        

@app.route('/api/permission_requests', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin(supports_credentials=True) # This route seems unused, but keeping for now
def permission_requests():
    leaves = load_leaves() or []
    users = load_users() or {}

    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    if request.method == "POST":
        staff_id = request.form.get('staff_id')
        start_date = request.form.get('start_date')
        duration = request.form.get('duration', '1') # Default to 1 day if empty
        leave_type = request.form.get('leave_type', 'short_absence')
        reasonText = request.form.get('reason', '')

        if not staff_id or not start_date or not reasonText:
            return jsonify({"message": "Missing required fields"}), 400

        staff_name = users.get(staff_id, {}).get('name', 'Unknown')

        # Format the reason based on the selected type so our yearly calculator can find it
        if leave_type == "yearly_leave":
            final_reason = f"[YEARLY LEAVE] {reasonText}"
        elif leave_type == "emergency_leave":
            final_reason = f"[EMERGENCY] {reasonText}"
        else:
            final_reason = reasonText

        # 1. Create the structured request object including duration and leave_type
        new_request = {
            "id": int(time.time()), # Using timestamp ensures completely unique IDs
            "staff_id": staff_id,
            "name": staff_name,
            "start_date": start_date,
            "duration": int(duration), # Saved as an integer for math calculations
            "leave_type": leave_type,
            "reason": final_reason,
            "status": "pending",
            "file_path": None,
            "file_viewed": False,
            "admin_remarks": "",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # 2. FILE HANDLING
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                if not os.path.exists(UPLOAD_FOLDER):
                    os.makedirs(UPLOAD_FOLDER)
                
                filename = f"{staff_id}_{int(time.time())}_{file.filename}"
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                
                new_request['file_path'] = filename

        # 3. Save everything back to leave_requests.json
        leaves.append(new_request)
        save_leaves(leaves)

        return jsonify({"message": "Leave request submitted successfully"}), 200

    # GET request logic: return pending requests for the admin review dashboard
    pending_requests = [l for l in leaves if l.get('status') == 'pending']
    return jsonify(pending_requests), 200
    

@app.route('/api/permission_review', methods=['POST'])
@cross_origin(supports_credentials=True) # This route seems unused, but keeping for now
def review_permission():
    data = request.get_json() or {}
    request_id = data.get('request_id')
    new_status = data.get('status') # 'approved' or 'denied'
    admin_remarks = data.get('admin_remarks', '')

    if not request_id or not new_status:
        return jsonify({"message": "Missing ID or Status"}), 400

    leaves = load_leaves() or []
    found = False

    for leave in leaves:
        if str(leave.get('id')) == str(request_id):
            leave['status'] = new_status
            leave['admin_remarks'] = admin_remarks
            found = True
            break

    if found:
        try:
            save_leaves(leaves) # Writes change directly to leave_requests.json
            return jsonify({"message": f"Request {request_id} successfully {new_status}"}), 200
        except Exception as e:
            return jsonify({"message": f"File save error: {str(e)}"}), 500
    else:
        return jsonify({"message": "Request ID not found in database"}), 404
@app.route('/api/admin/process_request', methods=['POST'])
@cross_origin(supports_credentials=True) # This route seems unused, but keeping for now
def process_request():
    payload = request.json
    if not payload:
        return jsonify({"error": "Missing payload data"}), 400
        
    # Safely extract and explicitly convert types
    try:
        req_id = int(payload.get('id'))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid or missing Request ID format."}), 400
        
    new_status = payload.get('status')
    remarks = payload.get('admin_remarks', '').strip()

    try:
        # Use your backend's built-in function to open leave_requests.json safely
        requests_list = load_leaves()
        request_found = False
        
        for req in requests_list:
            # Defensive Type Matching: cast file ID to int to ensure a clean match
            if int(req.get('id')) == req_id:
                req['status'] = new_status
                req['admin_remarks'] = remarks  # Saves the typed evaluation remarks text
                request_found = True
                break
                
        if not request_found:
            return jsonify({"error": f"Request record with ID {req_id} not found."}), 404
            
        # Use your backend's built-in function to commit the update back to disk
        save_leaves(requests_list)
            
        return jsonify({"message": "Successfully saved updated administrative evaluation data."}), 200
        
    except Exception as e:
        print(f"ERROR processing admin request: {e}")
        return jsonify({"error": f"File save error description: {str(e)}"}), 500


@app.route('/api/payroll/<month>', methods=['GET'])
def get_payroll(month):

    try:

        payroll = calculate_monthly_payroll(month)

        return jsonify({
            "status": "success",
            "payroll": payroll
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500  
        
        
@app.route('/api/users', methods=['GET'])
@cross_origin()
def get_all_users_for_payroll():
    try:
        # Reuses your existing function from core_logic that reads users.json
        users_data = load_users() 
        return jsonify(users_data), 200
    except Exception as e:
        print("ERROR FETCHING MASTER USERS FOR PAYROLL:", e)
        return jsonify({"status": "error", "message": str(e)}), 500                 
    
@app.route('/api/admin_notifications', methods=['GET'])
def get_admin_notifications(): # This route seems unused, but keeping for now
    try:
        # Load the leave requests
        with open('leave_requests.json', 'r') as f:
            leaves = json.load(f)
        
        # Count requests where status is 'pending'
        pending_count = sum(1 for leave in leaves if leave.get('status') == 'pending')
        
        return jsonify({"pending_count": pending_count}), 200
    except Exception as e:
        return jsonify({"pending_count": 0, "error": str(e)}), 500
    
@app.route('/api/my_requests/<staff_id>', methods=['GET']) # This route seems unused, but keeping for now
def get_my_requests(staff_id):
    try:
        # 1. Load the database file
        with open('leave_requests.json', 'r') as f:
            leaves = json.load(f)
        
        # 2. Filter: only keep requests where staff_id matches the one logged in
        # We use str() to ensure '1001' (string) matches 1001 (int)
        user_history = [l for l in leaves if str(l.get('staff_id')) == str(staff_id)]
        
        return jsonify(user_history), 200
    except Exception as e:
        print(f"Error fetching staff history: {e}")
        return jsonify([]), 500    

# Ensure this folder exists on your computer
UPLOAD_FOLDER = 'uploads/permissions' 

@app.route('/api/view_file/<int:request_id>/<filename>')
def view_file(request_id, filename):
    """Marks the file as viewed in the JSON and serves the file to the Admin."""
    try:
        # 1. Load the leaves and update the 'file_viewed' status
        leaves = load_leaves()
        updated = False
        for leave in leaves:
            if str(leave.get('id')) == str(request_id):
                leave['file_viewed'] = True
                updated = True
                break
        
        # 2. Save the updated list back to the JSON file
        if updated:
            save_leaves(leaves)
            print(f"DEBUG: File for request {request_id} marked as viewed.")

        # 3. Serve the file from the directory
        return send_from_directory(UPLOAD_FOLDER, filename)
    except Exception as e:
        print(f"View File Error: {e}")
        return jsonify({"message": "File not found or error updating status"}), 404
# -------------------------------------------------
# ERROR HANDLING
# -------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return jsonify(status="error", message="Endpoint not found"), 404


@app.errorhandler(Exception)
def server_error(e):
    return jsonify(status="error", message="Internal server error"), 500

if __name__ == "__main__":
    USERS_FILE = "users.json"
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)