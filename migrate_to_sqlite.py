import os
import json
import csv
from database import get_db_connection

def migrate():
    """Migrate data from JSON/CSV to SQLite"""
    conn = get_db_connection()
    cursor = conn.cursor()

    print("🚀 Starting migration to SQLite...")

    # 1. Migrate users.json
    if os.path.exists('users.json'):
        print("📁 Migrating users.json...")
        with open('users.json', 'r', encoding='utf-8') as f:
            users = json.load(f)
        
        for uid, u in users.items():
            cursor.execute('''
                INSERT OR REPLACE INTO users 
                (id, name, password_hash, role, department, base_monthly_salary, 
                 overtime_rate, sex, is_first_login)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                uid, 
                u.get('name'), 
                u.get('password_hash'), 
                u.get('role', 'staff'),
                u.get('department'), 
                u.get('base_monthly_salary', 0),
                u.get('overtime_rate', 0), 
                u.get('sex'),
                u.get('is_first_login', 1)
            ))
        print(f"   ✅ Migrated {len(users)} users")

    # 2. Migrate leave_requests.json
    if os.path.exists('leave_requests.json'):
        print("📁 Migrating leave_requests.json...")
        with open('leave_requests.json', 'r', encoding='utf-8') as f:
            leaves = json.load(f)
        
        for leave in leaves:
            cursor.execute('''
                INSERT OR REPLACE INTO leave_requests 
                (id, staff_id, name, start_date, duration, leave_type, reason, 
                 status, admin_remarks, file_path, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                leave.get('id'), 
                leave.get('staff_id'), 
                leave.get('name'),
                leave.get('start_date'), 
                leave.get('duration'), 
                leave.get('leave_type'), 
                leave.get('reason'),
                leave.get('status', 'pending'), 
                leave.get('admin_remarks'),
                leave.get('file_path'), 
                leave.get('timestamp')
            ))
        print(f"   ✅ Migrated {len(leaves)} leave requests")

    # 3. Migrate attendance_log.csv
    if os.path.exists('attendance_log.csv'):
        print("📁 Migrating attendance_log.csv...")
        with open('attendance_log.csv', 'r', encoding='latin1') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                cursor.execute('''
                    INSERT OR IGNORE INTO attendance_log 
                    (staff_id, name, department, supervisor_id, date, 
                     check_in, check_out, status, shift_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row.get('ID'), 
                    row.get('Name'), 
                    row.get('Department'),
                    row.get('SupervisorID'), 
                    row.get('Date'),
                    row.get('Check_In'), 
                    row.get('Check_Out'),
                    row.get('Status'), 
                    row.get('ShiftType')
                ))
                count += 1
        print(f"   ✅ Migrated {count} attendance records")

    # 4. Migrate finance_data/payroll_source_*.json files
    payroll_dir = "finance_data"
    if os.path.exists(payroll_dir):
        print(f"📁 Migrating payroll reports from {payroll_dir}...")
        migrated_payroll_count = 0
        for filename in os.listdir(payroll_dir):
            if filename.startswith("payroll_source_") and filename.endswith(".json"):
                month = filename.replace("payroll_source_", "").replace(".json", "")
                file_path = os.path.join(payroll_dir, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        report_data = json.load(f)
                    cursor.execute('''
                        INSERT OR REPLACE INTO payroll_reports (month, report_data)
                        VALUES (?, ?)
                    ''', (month, json.dumps(report_data)))
                    migrated_payroll_count += 1
                except Exception as e:
                    print(f"     ❌ Error migrating {filename}: {e}")
        print(f"   ✅ Migrated {migrated_payroll_count} payroll reports")
    else:
        print(f"   ℹ️ Payroll data directory '{payroll_dir}' not found, skipping migration.")

    conn.commit()
    conn.close()
    print("🎉 Migration completed successfully! SQLite is now ready.")

if __name__ == "__main__":
    migrate()