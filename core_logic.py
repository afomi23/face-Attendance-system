import cv2
import face_recognition
import numpy as np
import os
import csv
import pickle
import json
import base64
import pandas as pd
from datetime import datetime, time
import secrets 
import re 
from database import get_db_connection
import bcrypt 
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return {}

def save_users(users_data):
    """Saves users to the users.json file."""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users_data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving users.json: {e}")
        return False

def load_leaves():
    """Loads leave requests from the leave_requests.json file."""
    if not os.path.exists(LEAVES_FILE):
        return []
    try:
        with open(LEAVES_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception):
        return []

def save_leaves(data):
    """Saves leave requests to the leave_requests.json file."""
    try:
        with open(LEAVES_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving leave_requests.json: {e}")
        return False

camera_status = {"running": False, "supervisor_id": None}
def load_submissions():
    if not os.path.exists('finance_reports.json'):
        return {}
    with open('finance_reports.json', 'r') as f:
        return json.load(f)

def save_submissions(data):
    with open('finance_reports.json', 'w') as f:
        json.dump(data, f, indent=4)
        
# --- 1. Constants and Configuration ---
ENCODINGS_FILE = 'face_encodings.pickle'
LOG_FILE = 'attendance_log.csv' # Shift Logging/Payroll File
USERS_FILE = 'users.json'
LEAVES_FILE = 'leave_requests.json' # Placeholder for future leave request logic

# --- 2. Data Persistence (Encodings) ---
def load_encodings():
    if not os.path.exists(ENCODINGS_FILE):
        # Added 'Departments' to the default empty structure
        return {"IDs": [], "Encodings": [], "Names": [], "Departments": []}
    with open(ENCODINGS_FILE, 'rb') as f:
        try:
            data = pickle.load(f)
            # Safety check: if an old file exists without the key, add it
            if 'Departments' not in data:
                data['Departments'] = []
            return data
        except (EOFError, pickle.UnpicklingError):
            return {"IDs": [], "Encodings": [], "Names": [], "Departments": []}
def save_encodings(data):
    """Saves face encodings and metadata."""
    if 'Encodings' in data:
        data['Encodings'] = [e.tolist() if isinstance(e, np.ndarray) else e for e in data['Encodings']]
    with open(ENCODINGS_FILE, 'wb') as f:
        pickle.dump(data, f)

# --- 3. User Management Functions ---

def authenticate_user(user_id, password):
    """Authenticates a user against the SQLite database."""
    users = load_users()
    user_id = str(user_id).strip()
    if user_id in users:
        user = users[user_id]
        stored_hash = user.get('password_hash')
        
        if not stored_hash:
            return None

        try:
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                return user
        except Exception:
            return None
    return None

def generate_bcrypt_hash(password):
    """Generates a secure bcrypt hash for a given password string."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

import secrets
from datetime import datetime, timedelta
from database import get_db_connection

def create_reset_token(staff_id):
    # Requirement: Secure 6-digit numeric token for easy manual communication via Admin
    token = "".join(secrets.choice("0123456789") for _ in range(6))
    expires_at = (datetime.now() + timedelta(minutes=15)).isoformat()

    conn = get_db_connection()
    cursor = conn.cursor()

    # Invalidate old tokens for this user
    cursor.execute('UPDATE password_resets SET used = 1 WHERE staff_id = ?', (staff_id,))

    # Insert new token
    cursor.execute('''
        INSERT INTO password_resets (staff_id, token, expires_at, used)
        VALUES (?, ?, ?, 0)
    ''', (staff_id, token, expires_at))

    conn.commit()
    conn.close()
    return token


def verify_and_reset_password_logic(staff_id, token, new_password):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if valid, unused, and not expired
    now = datetime.now().isoformat()
    cursor.execute('SELECT id FROM password_resets WHERE staff_id = ? AND token = ? AND used = 0 AND expires_at > ?', 
                   (staff_id, token, now))

    row = cursor.fetchone()

    if row:
        new_hash = generate_bcrypt_hash(new_password)

        cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, staff_id))
        cursor.execute('UPDATE password_resets SET used = 1 WHERE id = ?', (row['id'],))
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False

def _read_and_standardize_log():
    """Helper to load and clean the attendance log CSV."""
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        return pd.DataFrame(columns=['ID', 'Date', 'Check_Out'])
        
    try:
        df = pd.read_csv(LOG_FILE, encoding='latin1')
        df.columns = df.columns.str.strip() 
        
        if 'ID' in df.columns:
            df['ID'] = df['ID'].astype(str).str.strip()
            
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime("%Y-%m-%d")
        
        return df
    except Exception:
        return pd.DataFrame(columns=['ID', 'Date', 'Check_Out'])

def get_registered_staff_count():
    """Counts the number of users registered with the 'staff_member' role."""
    users = load_users()
    return sum(1 for u in users.values() if u.get('role') == 'staff_member')

def get_present_today_count():
    """Count only staff who have BOTH clock in and clock out today"""
    today = datetime.now().strftime("%Y-%m-%d")
    count = 0
    try:
        df = _read_and_standardize_log()
        if df.empty:
            return 0
            
        today_records = df[df['Date'] == today]
        
        # Count only those who have Check_Out filled
        completed_shifts = today_records[
            today_records['Check_Out'].notna() & 
            (today_records['Check_Out'].astype(str).str.strip() != "") &
            (today_records['Check_Out'].astype(str).str.strip() != "-") &
            (today_records['Check_Out'].astype(str).str.strip() != "--:--:--")
        ]
        count = completed_shifts['ID'].nunique()
        
    except Exception as e:
        print(f"Error counting present today: {e}")
    
    return count
        
# --- 4. Core Shift Logging & Enrollment ---

def detect_and_recognize_multiple_faces(frame, known_encodings, known_ids, known_names, tolerance=0.5):
    if frame is None:
        return []

    # Use a smaller frame for faster detection
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
    
    recognized_people = []
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        name = "Unknown"
        pid = "Unknown"

        if len(known_encodings) > 0:
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=tolerance)
            if True in matches:
                first_match_index = matches.index(True)
                name = known_names[first_match_index]
                pid = known_ids[first_match_index]

        recognized_people.append({
            "name": name,
            "id": pid,
            # Scaling back to original 640x480 resolution
            "box": (top * 4, right * 4, bottom * 4, left * 4)
        })
    return recognized_people


def process_frame():
    open_status, shift_type = is_camera_window_open()
    
    if not open_status:
        return jsonify({"status": "closed", "message": "Outside of shift hours"})

    # Process faces but DO NOT shut down the camera logic here
    # Just return the result and let the frontend keep sending frames
    results = detect_and_recognize_multiple_faces(frame)
    return jsonify({"status": "active", "results": results})


def enroll_new_staff_core(staff_id, staff_name, staff_dept, sex, salary, overtime, num_captures=5, time_limit_sec=15):
    staff_id = str(staff_id).strip()
    staff_name = str(staff_name).strip()
    staff_dept = str(staff_dept).strip()
    
    data = load_encodings()
    if staff_id in data['IDs']:
        raise Exception(f"Staff ID {staff_id} is already enrolled.")

    cap = None
    encodings = []
    
    try:
        if os.name == 'nt':
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(0)
            
        if not cap.isOpened():
            raise Exception("Could not open webcam.")
            
        print(f"📸 Camera opened successfully. Attempting to capture {num_captures} face variations...")
            
        for i in range(num_captures):
            captured = False
            loop_start = datetime.now()
            
            while (datetime.now() - loop_start).total_seconds() < time_limit_sec:
                ret, frame = cap.read()
                if not ret:
                    cv2.waitKey(10)
                    continue
                
                frame = cv2.flip(frame, 1)
                small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
                rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
                
                single_face_locations = face_recognition.face_locations(rgb_small, model="hog")
                
                # Visual desktop feedback decoration
                display_frame = frame.copy()
                if len(single_face_locations) == 1:
                    # Scale coordinates back up to map original frame bounds
                    t, r, b, l = [v * 2 for v in single_face_locations[0]]
                    cv2.rectangle(display_frame, (l, t), (r, b), (34, 197, 94), 2)
                    cv2.putText(display_frame, f"Capturing {i+1}/{num_captures} - HOLD STILL", (30, 40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (34, 197, 94), 2, cv2.LINE_AA)
                    
                    rgb_full = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    full_loc = face_recognition.face_locations(rgb_full)
                    
                    if full_loc:
                        encoded_list = face_recognition.face_encodings(rgb_full, full_loc)
                        if encoded_list and len(encoded_list) > 0:
                            encodings.append(encoded_list[0].tolist())
                            captured = True
                            print(f"   --> Captured snapshot matrix variance sample {i+1}/{num_captures}")
                            
                            # Show green box briefly on screen so user knows it captured
                            cv2.imshow("HOSPITAL STAFF ENROLLMENT ENVIRONMENT", display_frame)
                            cv2.waitKey(600) 
                            break
                else:
                    cv2.putText(display_frame, "ALIGN 1 FACE IN CENTER", (30, 40), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)

                # 🌟 FORCES DISPLAY WINDOW TO POP UP LOCALLY ON WINDOWS
                cv2.imshow("HOSPITAL STAFF ENROLLMENT ENVIRONMENT", display_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    raise Exception("Enrollment cancelled by supervisor.")
                
            if not captured: 
                print(f"⚠️ Face Sample variance capture {i+1} timed out or failed to align.")
            
    finally:
        if cap: 
            cap.release()
        cv2.destroyAllWindows() 
        print("🔒 Camera hardware stream released safely from enrollment lock.")
        
    if len(encodings) < 2: 
        raise Exception("Insufficient face captures obtained. Please align your face clearly.")

    mean_encoding = np.mean(np.array(encodings), axis=0).tolist()
    
    data = load_encodings()
    data['IDs'].append(staff_id) 
    data['Names'].append(staff_name)
    data['Departments'].append(staff_dept)
    data.setdefault('Sex', []).append(sex)
    data.setdefault('Salaries', []).append(float(salary))
    data.setdefault('Overtime', []).append(float(overtime))
    data['Encodings'].append(mean_encoding) 
    
    save_encodings(data)
    return True

def is_shift_already_clocked(staff_id, shift_type=None):
    """Updated version - supports shift level check"""
    target_date = datetime.now().strftime("%Y-%m-%d")
    df = _read_and_standardize_log()
    
    if df.empty:
        return False
        
    mask = (df['Date'] == target_date) & (df['ID'] == staff_id.strip())
    
    if shift_type:
        mask = mask & (df.get('ShiftType', '') == shift_type)
        
    return not df[mask].empty


        
def get_staff_department(staff_id):
    """Retrieves the department for a given staff member ID from the encodings file."""
    data = load_encodings()
    try:
        index = data['IDs'].index(staff_id.strip())
        return data['Departments'][index]
    except ValueError:
        return "N/A" # Return 'N/A' if ID not found in encodings

def calculate_monthly_payroll(target_month):
    """
    Calculates hospital payroll using a strict 30-day pro-rated model.
    Zero attendance = Zero salary (full deduction).
    """
    print(f"--- CALCULATING PAYROLL FOR {target_month} ---")

    users = load_users()
    leaves = load_leaves()
    df_log = _read_and_standardize_log()

    if not df_log.empty and 'Date' in df_log.columns:
        df_log = df_log[df_log['Date'].astype(str).str.startswith(target_month)].copy()

    payroll_records = []

    for uid, udata in users.items():
        user_role = str(udata.get('role', '')).lower()
        if user_role not in ['staff', 'staff_member']:
            continue

        base_salary = float(udata.get('base_monthly_salary', 0))
        if base_salary <= 0: # Ensure base_salary is positive for calculations
            continue

        # Count completed shifts
        staff_scans = df_log[
            (df_log['ID'].astype(str).str.strip() == str(uid).strip()) &
            (df_log['Check_Out'].notna()) &
            (df_log['Check_Out'].astype(str).str.strip().replace('-', '').replace('--:--:--', '') != "")
        ]
        days_present = staff_scans['Date'].nunique()

        # Count approved leave days
        leave_count = sum(
            int(l.get('duration', 1))
            for l in leaves 
            if str(l.get('staff_id')).strip() == str(uid).strip()
            and l.get('status') == 'approved'
            and str(l.get('start_date', '')).startswith(target_month)
        )

        # Using 30 working days for payroll calculation as per user's request
        WORKING_DAYS_IN_MONTH = 30
        credited_days = min(WORKING_DAYS_IN_MONTH, days_present + leave_count)
        absent_days = max(0, WORKING_DAYS_IN_MONTH - credited_days)

        daily_rate = base_salary / WORKING_DAYS_IN_MONTH if WORKING_DAYS_IN_MONTH > 0 else 0

        calculated_final_salary = credited_days * daily_rate
        calculated_deduction = base_salary - calculated_final_salary

        # Ensure final salary and deduction are not negative
        final_salary_to_report = max(0.0, calculated_final_salary)
        deduction_to_report = max(0.0, calculated_deduction)

        payroll_records.append({
            "staff_id": str(uid),
            "name": udata.get('name', 'Unknown'),
            "department": udata.get('department', 'General'),
            "present_days": int(days_present), # Changed key to match frontend expectation
            "absent_days": int(absent_days),
            "base_monthly_salary": base_salary,
            "deduction": f"{deduction_to_report:.2f}",
            "final_salary": f"{final_salary_to_report:.2f}"
        })

    return payroll_records


def register_new_user(name, password, role, actual_id, base_monthly_salary=0, daily_overtime_rate=0):
    """
    Registers a new user with dedicated financial parameters and default password setup.
    """
    data = load_users()
    dict_key = str(actual_id).strip()
    
    if dict_key in data:
        return False, f"Error: A user with ID '{actual_id}' already exists."

    data[dict_key] = {
        "id": dict_key,
        "name": name,
        "password_hash": generate_bcrypt_hash(password),
        "role": role,
        "is_first_login": True, # Flag to trigger password change on first login
        "base_monthly_salary": float(base_monthly_salary),
        "daily_overtime_rate": float(daily_overtime_rate)
    }
    
    save_users(data)
    return True, f"User {name} registered successfully."

def log_shift_clocking(staff_id, staff_name, supervisor_id):
    staff_id = staff_id.strip()
    staff_name = staff_name.strip()
    supervisor_id = supervisor_id.strip()

    now = datetime.now()
    today_str = now.strftime("%Y-%m-%d")

    shift_start = datetime.strptime(SHIFT_START, "%H:%M:%S").time()
    shift_end = datetime.strptime(SHIFT_END, "%H:%M:%S").time()

    # Read existing log
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        df = pd.read_csv(LOG_FILE)
    else:
        df = pd.DataFrame(columns=[
            "ID", "Name", "Department",
            "SupervisorID", "Date",
            "Check_In", "Check_Out", "Status"
        ])

    staff_dep = get_staff_department(staff_id)

    # Filter today's record
    today_records = df[(df["ID"] == staff_id) & (df["Date"] == today_str)]

    # ---------------- CHECK-IN ----------------
    if today_records.empty:

        status = "On-Time"
        if now.time() > shift_start:
            status = "Late"

        new_entry = {
            "ID": staff_id,
            "Name": staff_name,
            "Department": staff_dep,
            "SupervisorID": supervisor_id,
            "Date": today_str,
            "Check_In": now.strftime("%H:%M:%S"),
            "Check_Out": "",
            "Status": status
        }

        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(LOG_FILE, index=False)

        return True, f"{staff_name} checked in ({status})"

    # ---------------- CHECK-OUT ----------------
    else:
        index = today_records.index[0]
        check_in_time = today_records.iloc[0]["Check_In"]
        check_out_time = today_records.iloc[0]["Check_Out"]

        last_check_in = datetime.strptime(check_in_time, "%H:%M:%S")
        last_check_in = datetime.combine(now.date(), last_check_in.time())

        if (now - last_check_in) < timedelta(minutes=DUPLICATE_WINDOW_MINUTES):
            return False, "Duplicate scan ignored"

        if pd.isna(check_out_time) or check_out_time == "":
            df.at[index, "Check_Out"] = now.strftime("%H:%M:%S")

            if now.time() > shift_end:
                df.at[index, "Status"] = "Completed + Overtime"
            else:
                df.at[index, "Status"] = "Completed"

            df.to_csv(LOG_FILE, index=False)

            return True, f"{staff_name} checked out"

        return False, "Shift already completed"
    
    


SHIFT_WINDOWS = {
    # 2:00 - 3:00 AM (Eth)
    "day_in":    (time(8, 0),  time(9, 59)),   
    
    # 11:00 - 12:00 PM (Eth)
    "day_out":   (time(17, 0), time(17, 59)),  
    
    # 12:00 - 1:00 PM (Eth - Night shift starts)
    "night_in":  (time(18, 0), time(18, 59)),  
    
    # 1:00 - 2:00 AM (Next day)
    "night_out": (time(6, 0),  time(7, 59)),   
}

def is_in_shift_window():
    """Returns shift_type if current time is in allowed window"""
    now = datetime.now().time()
    for shift_key, (start, end) in SHIFT_WINDOWS.items():
        if start <= now <= end:
            return shift_key
    return None

def is_attendance_window_active():
    """For frontend to know if camera should be active"""
    shift = is_in_shift_window()
    return (True, shift) if shift else (False, None)

# ====================== IMPROVED CLOCKING LOGIC ======================
def log_shift_clocking_api(staff_id, name, supervisor_id="1001"):
    """Fixed: Supports both Day and Night shifts for same doctor"""
    staff_id = str(staff_id).strip()
    name = str(name).strip()
    supervisor_id = str(supervisor_id).strip()

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    shift_type = is_in_shift_window()   # e.g., "day_in", "night_out", etc.
    if not shift_type:
        return {
            "success": False, 
            "message": "❌ Attendance is closed. Please come during your official shift time."
        }

    # Load log
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        df = pd.read_csv(LOG_FILE, encoding='latin1')
        df.columns = [c.strip() for c in df.columns]
    else:
        df = pd.DataFrame(columns=['ID', 'Name', 'Department', 'SupervisorID', 'Date', 
                                 'Check_In', 'Check_Out', 'Status', 'ShiftType'])

    # ==================== KEY FIX ====================
    # Filter by BOTH Date AND Shift Type
    today_shift_records = df[
        (df['ID'].astype(str).str.strip() == staff_id) & 
        (df['Date'] == date_str) & 
        (df.get('ShiftType', '') == shift_type.split('_')[0])  # "day" or "night"
    ]
    # ================================================

    staff_dept = get_staff_department(staff_id)

    is_in_window = "in" in shift_type
    is_out_window = "out" in shift_type

    if today_shift_records.empty:
        # ==================== CLOCK IN ====================
        if not is_in_window:
            return {"success": False, "message": "❌ You can only Clock In during IN window."}
        
        new_entry = {
            "ID": staff_id,
            "Name": name,
            "Department": staff_dept,
            "SupervisorID": supervisor_id,
            "Date": date_str,
            "Check_In": time_str,
            "Check_Out": "",
            "Status": f"Clocked In ({shift_type.replace('_', ' ')})",
            "ShiftType": shift_type.split('_')[0]   # "day" or "night"
        }
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(LOG_FILE, index=False)
        
        return {
            "success": True, 
            "message": f"✅ Clock In successful ({shift_type}) at {time_str}",
            "action": "in",
            "shift_type": shift_type
        }

    else:
        # ==================== CLOCK OUT ====================
        idx = today_shift_records.index[0]
        check_out = df.at[idx, 'Check_Out']

        if pd.isna(check_out) or str(check_out).strip() == "":
            if not is_out_window:
                return {"success": False, "message": "❌ You can only Clock Out during OUT window."}
            
            df.at[idx, 'Check_Out'] = time_str
            df.at[idx, 'Status'] = f"Completed ({shift_type.replace('_', ' ')})"
            
            df.to_csv(LOG_FILE, index=False)
            
            return {
                "success": True, 
                "message": f"✅ Clock Out successful ({shift_type}) at {time_str}",
                "action": "out",
                "shift_type": shift_type
            }
        else:
            return {"success": False, "message": f"✅ You have already completed your {shift_type.split('_')[0]} shift today."}
        
               
         
    
def get_full_shift_log(filter_date=None):
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        return []

    try:
        df = pd.read_csv(LOG_FILE, encoding='latin1')
        df.columns = [c.strip() for c in df.columns]
        
        if len(df.columns) == 8:
            df.columns = ['ID', 'Name', 'Department', 'SupervisorID', 'Date', 'Check_In', 'Check_Out', 'Status']
        
        df = df.fillna("-")

        if filter_date:
            df = df[df['Date'].astype(str).str.strip() == str(filter_date).strip()]

        return df.to_dict('records')
    except Exception as e:
        print(f"Report Error: {e}")
        return []

def get_staff_shift_log(staff_id, filter_date=None):
    """
    Returns shift log records for a specific staff member, filtered by date or full history.
    """
    # 1. Get all logs first
    full_log_data = get_full_shift_log(filter_date=None)
    
    if not full_log_data:
        return []

    df = pd.DataFrame(full_log_data)
    
    if df.empty or 'ID' not in df.columns:
        return []

    # 2. MATCH THE ID (Force string comparison)
    target_id = str(staff_id).strip() 
    df_filtered_by_id = df[df['ID'].astype(str).str.strip() == target_id].copy()

    if df_filtered_by_id.empty:
        return []
        
    df_final = df_filtered_by_id.copy() 
    
    # 3. FILTER BY DATE
    if filter_date and isinstance(filter_date, str) and filter_date.strip():
        try:
            target_date_str = pd.to_datetime(filter_date.strip(), errors='coerce').strftime("%Y-%m-%d")
            df_final = df_final[df_final['Date'].astype(str).str.strip() == target_date_str].copy()
        except Exception as ve:
            print(f"Warning: Staff date filtering error: {ve}")

    # 4. SELECT COLUMNS FOR HTML TABLE
    final_columns = [
        'ID', 'Name', 'Department',
        'Date', 'Check_In', 'Check_Out', 'Status'
    ]

    cols_to_select = [col for col in final_columns if col in df_final.columns]
    
    return df_final[cols_to_select].to_dict('records')

def get_staff_total_clockings(staff_id):
    """Calculates the total number of unique days a staff member clocked in."""
    try:
        # Get history for the specific staff member
        full_staff_log = get_staff_shift_log(staff_id, filter_date=None)
        if not full_staff_log:
            return 0
            
        df = pd.DataFrame(full_staff_log)
        # Use nunique on the standardized 'Date' column
        return df['Date'].nunique()
        
    except Exception as e:
        print(f"Error calculating total clockings for {staff_id}: {e}")
        return 0

def update_staff_record(old_id, new_id=None, new_name=None, new_dept=None, salary=None, overtime=None, delete_face=False):
    # --- Part 1: Update users.json ---
    users = load_users()
    id_changed = new_id and str(new_id) != str(old_id)
    
    if old_id in users:
        user_data = users.pop(old_id)
        if new_name: user_data['name'] = new_name
        if new_id: user_data['id'] = str(new_id)
        if new_dept: user_data['department'] = new_dept
        if salary is not None: user_data['base_monthly_salary'] = float(salary or 0)
        if overtime is not None: user_data['overtime_rate'] = float(overtime or 0)
        
        final_id = new_id if new_id else old_id
        users[final_id] = user_data
        
        save_users(users)

    # --- Part 2: Update face_encodings (Biometrics) ---
    data = load_encodings()
    if old_id in data['IDs']:
        idx = data['IDs'].index(old_id)
        
        if delete_face:
            # Clear face data for re-scan
            for key in ['IDs', 'Encodings', 'Names', 'Departments', 'Sex', 'Salaries', 'Overtime']:
                if key in data and idx < len(data[key]):
                    data[key].pop(idx)
        else:
            # Standard metadata update
            if new_id: data['IDs'][idx] = str(new_id)
            if new_name: data['Names'][idx] = new_name
            if new_dept: data['Departments'][idx] = new_dept
            # Sync financial data if your biometric file also tracks it
            if salary is not None and 'Salaries' in data: 
                data['Salaries'][idx] = float(salary)
            if overtime is not None and 'Overtime' in data: 
                data['Overtime'][idx] = float(overtime)
            
        save_encodings(data)
        return True
    return False

def update_staff_face_encodings(staff_id, images):
    # Normalize input ID
    staff_id = str(staff_id).strip()
    
    # Load data
    try:
        data = load_encodings()
    except Exception as e:
        return False, f"Database Load Error: {str(e)}"

    # 1. Check Existence
    # Ensure IDs in the list are strings for comparison
    string_ids = [str(i) for i in data.get("IDs", [])]
    
    if staff_id not in string_ids:
        return False, "Error: Staff ID not found in the database. The record may have been deleted."

    collected_encodings = []

    print(f"Starting processing for {staff_id} with {len(images)} images...")

    for img_data in images:
        try:
            # 1. Clean Base64 header
            if "," in img_data:
                img_data = img_data.split(",", 1)[1]
            
            # 2. Decode bytes to image
            image_bytes = base64.b64decode(img_data)
            np_arr = np.frombuffer(image_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            if frame is None:
                print("DEBUG: Frame is None (could not decode image)")
                continue

            # 3. Resize while PRESERVING aspect ratio (max side = 640px)
            # Forcing 640x480 distorts portrait webcam feeds and breaks HOG detection
            h, w = frame.shape[:2]
            max_side = 640
            if max(h, w) > max_side:
                scale = max_side / max(h, w)
                frame = cv2.resize(frame, (int(w * scale), int(h * scale)))

            print(f"DEBUG: Frame shape after resize: {frame.shape}")

            # 4. Convert to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 5. Detect face locations with higher upsample count (2 instead of 1)
            # upsample=2 catches faces that are smaller or at trickier angles
            face_locations = face_recognition.face_locations(rgb_frame, model="hog", number_of_times_to_upsample=2)
            
            print(f"DEBUG: Detected {len(face_locations)} face(s) in this frame.")

            if len(face_locations) > 0:
                # 6. Generate encodings for the found locations
                encodings = face_recognition.face_encodings(rgb_frame, face_locations)
                
                # We only take the first face found
                if len(encodings) > 0:
                    collected_encodings.append(encodings[0])
                    print(f"DEBUG: Encoding collected. Total so far: {len(collected_encodings)}")
            else:
                print("DEBUG: No face locations found in this frame.")

        except Exception as e:
            print("IMAGE PROCESS ERROR:", e)

    print(f"DEBUG: Total valid captures collected: {len(collected_encodings)}")

    # 7. Check if we have at least 1 valid sample (lowered from 2 to be more forgiving)
    if len(collected_encodings) < 1:
        return False, f"No face detected in any of the {len(images)} captured frames. Please ensure your face is clearly visible, well-lit, and centred in the camera view."

    # 8. Calculate mean encoding (or use single encoding if only 1)
    mean_encoding = np.mean(np.array(collected_encodings), axis=0).tolist()
    
    # 9. SAFE UPDATE INDEX LOOKUP
    try:
        idx = string_ids.index(staff_id)
    except ValueError:
        print(f"CRITICAL ERROR: ID {staff_id} lookup failed. List: {string_ids}")
        return False, "System Error: ID mismatch in database. Please refresh the page and try again."

    # 10. Update and SAFE SAVE
    try:
        data["Encodings"][idx] = mean_encoding
        save_encodings(data)
    except Exception as e:
        print(f"CRITICAL SAVE ERROR: {e}")
        return False, f"Database Save Failed: {str(e)}. Check file permissions."

    return True, f"Biometrics updated successfully using {len(collected_encodings)} valid capture(s)."

def search_staff_logic(query):
    data = load_encodings()
    results = []
    query = query.lower()

    for i in range(len(data['IDs'])):
        staff_id = str(data['IDs'][i])
        staff_name = str(data['Names'][i]).lower()
        
        if query in staff_id or query in staff_name:
            results.append({
                "id": data['IDs'][i],
                "name": data['Names'][i],
                "department": data['Departments'][i] if i < len(data['Departments']) else "N/A"
            })
        if len(results) >= 20: break 
            
    return results 

def get_face_encoding(image):
    """Helper to extract encoding from a single BGR frame."""
    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_img)
    return encodings # Returns a list of encodings    
