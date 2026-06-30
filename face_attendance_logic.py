import time
import json
import csv 
import os
from datetime import datetime
from flask import Flask, request, jsonify, Response
import cv2
import numpy as np
from flask_cors import CORS, cross_origin
app = Flask(__name__)
CORS(app, supports_credentials=True)
 
from core_logic import (
    register_new_user,
    authenticate_user,
    load_users,
    load_encodings,
    enroll_new_staff_core,
    log_shift_clocking_api,
    get_full_shift_log,
    get_staff_shift_log,
    detect_and_recognize_multiple_faces,
    get_staff_total_clockings,
    get_registered_staff_count,
    get_present_today_count
)

ROLE_MAP = {
    "hr_payroll_admin": "Admin",
    "shift_supervisor": "shift supervisor",
    "staff_member": "Staff"
}

# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------

LEAVES_FILE = "leave_requests.json"
camera_status = {"running": False, "supervisor_id": None}

app = Flask(__name__)
CORS(app)


# -------------------------------------------------
# LEAVE MANAGEMENT
# -------------------------------------------------

def load_leaves():
    if not os.path.exists(LEAVES_FILE):
        return []
    try:
        with open(LEAVES_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return []


def save_leaves(data):
    with open(LEAVES_FILE, "w") as f:
        json.dump(data, f, indent=4)


# -------------------------------------------------
# VIDEO STREAM
# Global variable to track who was logged in the CURRENT shift
# 1. MOVE THIS TO THE TOP OF YOUR FILE (Outside any function)
# This stays alive as long as the Flask server is running
# -------------------------------------------------
# VIDEO STREAM CONFIGURATION
# -------------------------------------------------

# CRITICAL: Define this variable HERE at the top level of the file
# This is the memory that survives even if the camera restarts.
recorded_ids = set()

def generate_frames():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    global recorded_ids  # Now Python correctly finds the global set above

    while camera_status["running"]:
        success, frame = cap.read()
        if not success: 
            break

        frame = cv2.flip(frame, 1)
        
        # Load the encodings for recognition
        data = load_encodings()
        recognized = detect_and_recognize_multiple_faces(
            frame, data['Encodings'], data['IDs'], data['Names']
        )

        supervisor_id = camera_status.get("supervisor_id")

        for person in recognized:
            name, pid = person["name"], person["id"]
            top, right, bottom, left = person["box"]

            # --- VISUALS: Rectangle & Name (Always shows in browser) ---
            # Blue color: (255, 0, 0)
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)
            
            # Green text: (0, 255, 0)
            label = f"{name} {pid}"
            cv2.putText(frame, label, (left, top - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            # --- REPORT LOGIC: Only logs known people and ONLY ONCE ---
            if pid != "Unknown":
                if pid not in recorded_ids:
                    if supervisor_id:
                        result = log_shift_clocking_api(pid, name, supervisor_id)
                        if result.get("success"):
                            # This is where we stop the duplicates!
                            recorded_ids.add(pid) 
                            print(f"REPORT SAVED: {name} ({pid}) captured once.")
            else:
                # This is an Unknown person. 
                # They have a box on screen, but we do NOTHING here.
                # They never touch the CSV.
                pass

        # Send the drawn-on frame to the frontend
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret: continue
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    cap.release()
# SHIFT CONTROL
# -------------------------------------------------
@app.route("/api/start_shift_logging", methods=["POST"])
def start_shift_logging():
    global recorded_ids
    
    # CLEAR THE MEMORY for the new shift
    recorded_ids.clear() 
    print("New shift started: Memory cleared for all staff.")

    data = request.get_json()
    supervisor_id = data.get("supervisor_id")
    camera_status["running"] = True
    camera_status["supervisor_id"] = supervisor_id
    
    return jsonify({"status": "success", "message": "Shift started, duplicates blocked."})


@app.route("/api/stop_attendance", methods=["POST"])
def stop_attendance():
    camera_status["running"] = False
    camera_status["supervisor_id"] = None
    return jsonify(status="success", message="Attendance stopped"), 200



@app.route("/api/video_feed")
def video_feed():
    if not camera_status["running"]:
        return jsonify(status="error", message="Shift not active"), 404

    return Response(
        generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame'
    )
    
# -------------------------------------------------
# USER MANAGEMENT
# -------------------------------------------------

@app.route("/api/register_user", methods=["POST"])
def register_user():
    data = request.get_json() or {}
    name = data.get("name")
    password = data.get("password")
    role = data.get("role")

    if not all([name, password, role]):
        return jsonify(status="error", message="Missing fields"), 400

    success, msg = register_new_user(name, password, role)
    return jsonify(status="success" if success else "error", message=msg)


@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    name = data.get("name")
    password = data.get("password")
    role = data.get("role")

    if not all([name, password, role]):
        return jsonify(status="error", message="Missing credentials"), 400

    success, user = authenticate_user(name, password, role)

    if not success:
        return jsonify(status="error", message=user), 401

    return jsonify(
        status="success",
        user_id=user.get("id"),
        user_name=user.get("name"),
        role=user.get("role")
    )


# -------------------------------------------------
# ENROLLMENT
# -------------------------------------------------

@app.route("/api/enroll_staff", methods=["POST"])
def enroll_staff():
    data = request.get_json() or {}
    requester_role = data.get("requester_role", "").lower()   # comes from frontend

    # Map frontend nice names → backend names
    role_map = {
        "admin":           "hr_payroll_admin",
        "shift_supervisor":"shift_supervisor",
        "shift supervisor":"shift_supervisor",   # in case old value slips through
    }

    backend_role = role_map.get(requester_role, requester_role)

    if backend_role not in ["hr_payroll_admin", "shift_supervisor"]:
        return jsonify({
            "status": "error",
            "message": f"Only Admin and Shift Supervisors can enroll staff (your role: {requester_role})"
        }), 403

    # rest of the function remains the same...
    s_id   = data.get("staff_id")
    name   = data.get("full_name")
    dept   = data.get("department")
    count  = data.get("num_captures", 5)

    try:
        result = enroll_new_staff_core(s_id, name, dept, count)
        return jsonify({"status": "success", "message": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
# -------------------------------------------------
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
    
@app.route('/api/admin_stats', methods=['GET'])
def get_admin_stats():
    try:
        # Load data
        users = load_users() # Ensure this returns a list
        from core_logic import load_encodings, get_present_today_count
        
        face_data = load_encodings()
        # Count unique IDs in the pickle file
        face_ids = face_data.get('IDs', [])
        unique_faces = len(set(face_ids))

        stats = {
            "total_staff": len(users),
            "enrolled_faces": unique_faces,
            "present_today": get_present_today_count()
        }
        print(f"Sending Stats to Dashboard: {stats}") # This shows in your Python terminal
        return jsonify(stats), 200
    except Exception as e:
        print(f"Error calculating stats: {e}")
        return jsonify({"total_staff": 0, "enrolled_faces": 0, "present_today": 0}), 200
# -------------------------------------------------
# ATTENDANCE REPORTS
# -------------------------------------------------
@app.route("/api/attendance_report/<date>", methods=["GET"])
def attendance_report(date):
    try:
        role = request.args.get("role")
        user_id = request.args.get("user_id")

        # ADMIN → see all
        if role == "admin":
            records = get_full_shift_log(filter_date=date)

        # SUPERVISOR → see all (optional: you can filter later)
        elif role == "shift_supervisor":
            records = get_full_shift_log(filter_date=date)

        # STAFF → see ONLY their own records
        elif role == "staff":
            records = get_staff_shift_log(user_id, filter_date=date)

        else:
            return jsonify({"error": "Invalid role"}), 403

        return jsonify(records), 200

    except Exception as e:
        print("REPORT ERROR:", e)
        return jsonify([]), 200
    
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
# LEAVE MANAGEMENT


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
    
    
@app.route('/api/permission_requests', methods=['GET', 'POST', 'OPTIONS'])
@cross_origin()
def permission_requests():
    leaves = load_leaves()
    users = load_users()  # ensure this returns dict keyed by staff_id

    if request.method == "OPTIONS":
        return jsonify({"message": "Preflight OK"}), 200

    if request.method == "POST":
        staff_id = request.form.get('staff_id')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        reason = request.form.get('reason')

        if not staff_id or not start_date or not reason:
            return jsonify({"message": "Missing required fields"}), 400

        staff_name = users.get(staff_id, {}).get('name', 'Unknown')

        new_request = {
            "id": len(leaves) + 1,
            "staff_id": staff_id,
            "name": staff_name,
            "start_date": start_date,
            "end_date": end_date if end_date else "",
            "reason": reason,
            "status": "pending"
        }

        leaves.append(new_request)
        save_leaves(leaves)

        return jsonify({"message": "Leave request submitted successfully"}), 200

    # GET: return all pending requests with names
    pending_requests = []
    for leave in leaves:
        if leave.get('status') == 'pending':
            if 'name' not in leave:
                leave['name'] = users.get(leave['staff_id'], {}).get('name', 'Unknown')
            pending_requests.append(leave)

    return jsonify(pending_requests), 200

@app.route('/api/permission_review', methods=['POST'])
def review_permission():
    data = request.get_json()
    request_id = data.get('request_id')
    new_status = data.get('status') # This will be 'approved' or 'denied'

    if not request_id or not new_status:
        return jsonify({"message": "Missing ID or Status"}), 400

    leaves = load_leaves()
    found = False

    for leave in leaves:
        # We use str() to ensure the IDs match regardless of type
        if str(leave.get('id')) == str(request_id):
            leave['status'] = new_status
            found = True
            break

    if found:
        # CRITICAL: This part actually writes the change to your leave_requests.json
        try:
            with open(LEAVES_FILE, 'w') as f:
                json.dump(leaves, f, indent=4)
            return jsonify({"message": f"Request {request_id} successfully {new_status}"}), 200
        except Exception as e:
            return jsonify({"message": f"File save error: {str(e)}"}), 500
    else:
        return jsonify({"message": "Request ID not found in database"}), 404


@app.route('/api/permission_requests', methods=['GET'])
def get_permission_requests():
    leaves = load_leaves()  
    users = load_users()     
    
    for leave in leaves:
        # Get the user info using the staff_id from the leave request
        user_info = users.get(leave['staff_id'])
        if user_info:
            leave['name'] = user_info.get('name', 'Unknown Staff')
        else:
            leave['name'] = "Unknown ID: " + leave['staff_id']

    return jsonify(leaves), 200
# -------------------------------------------------
# ERROR HANDLING
# -------------------------------------------------

@app.errorhandler(404)
def not_found(e):
    return jsonify(status="error", message="Endpoint not found"), 404


@app.errorhandler(Exception)
def server_error(e):
    return jsonify(status="error", message="Internal server error"), 500


# -------------------------------------------------
# RUN SERVER
# -------------------------------------------------

if __name__ == "__main__":
    load_users()
    if not os.path.exists(LEAVES_FILE):
        save_leaves([])
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)