import sqlite3
import json
import os
from datetime import datetime

DB_FILE = 'hospital.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
    return conn

def init_database():
    """Create all tables if they don't exist"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL,
            department TEXT,
            base_monthly_salary REAL DEFAULT 0,
            overtime_rate REAL DEFAULT 0,
            sex TEXT,
            is_first_login INTEGER DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 2. Leave Requests Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leave_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id TEXT,
            name TEXT,
            start_date TEXT,
            duration INTEGER,
            leave_type TEXT,
            reason TEXT,
            status TEXT DEFAULT 'pending',
            admin_remarks TEXT,
            file_path TEXT,
            file_viewed INTEGER DEFAULT 0,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (staff_id) REFERENCES users(id)
        )
    ''')

    # 3. Attendance Log Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id TEXT,
            name TEXT,
            department TEXT,
            supervisor_id TEXT,
            date TEXT,
            check_in TEXT,
            check_out TEXT,
            status TEXT,
            shift_type TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 4. Password Resets Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            staff_id TEXT NOT NULL,
            token TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            used INTEGER DEFAULT 0
        )
    ''')

    # 5. Payroll Reports Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payroll_reports (
            month TEXT PRIMARY KEY,
            report_data TEXT NOT NULL, -- Store JSON string of the payroll records
            generated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')


    conn.commit()
    conn.close()
    print("✅ SQLite Database initialized successfully!")

# Run initialization when imported
init_database()