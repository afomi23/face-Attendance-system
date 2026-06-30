<!doctype html>
<html lang="en">

<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>FaceAttend System</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.0.0/css/all.min.css" />
  <style>
    /* Ensure only one main page shows at a time */
    #loginPage,
    #registerPage,
    #passwordSetupPage,
    #dashboard {
      display: none;
    }


    /* Base style for the active state - adjust to your layout preference */
    .active-page {
      display: flex !important;
    }

    /* Global Reset and Base */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: "Poppins", sans-serif;
    }

    /* ===== LOGIN / REGISTER ===== */
    /* Shared styles for high-impact login/register pages */
    #loginPage,
    #registerPage {
      /* Change this in your <style> tag */
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
      /* Changed from height: 100% */
      width: 100%;
      /* Added width to ensure it spans across */

      margin: 0;
      padding: 0;

      background:
        linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
        url(images/hospital002.webp);
      background-size: cover;
      background-position: center;
    }

    .login-box,
    .register-box {
      background: rgba(51, 50, 50, 0.95);
      width: 380px;
      padding: 50px 35px;
      border-radius: 25px;
      text-align: center;
      box-shadow: 0 20px 50px rgba(0, 0, 0, 0.4);
      transition:
        transform 0.3s,
        box-shadow 0.3s;
    }

    .login-box:hover,
    .register-box:hover {
      transform: translateY(-5px);
      box-shadow: 0 25px 60px rgba(0, 0, 0, 0.5);
    }

    .login-box h2,
    .register-box h2 {
      color: #ffffff;
      margin-bottom: 8px;
    }

    .login-box p,
    .register-box p {
      color: #94a3b8;
      margin-bottom: 20px;
    }

    .input-box {
      position: relative;
      margin-bottom: 15px;
    }

    .input-box i {
      position: absolute;
      left: 12px;
      top: 50%;
      transform: translateY(-50%);
      color: #7ba3f9;
    }

    .input-box input,
    .input-box select,
    .input-box textarea {
      width: 100%;
      padding: 14px 14px 14px 40px;
      border-radius: 14px;
      border: 1px solid #a1afe7;
      outline: none;
      transition: all 0.3s;
      color: #1e293b;
      background-color: #f8fafc;
    }

    /* Adjusted padding for textarea, as it doesn't need the icon space */
    .input-box textarea {
      padding: 14px;
      padding-left: 14px;
    }

    .input-box input:hover,
    .input-box select:hover,
    .input-box textarea:hover,
    .input-box input:focus,
    .input-box select:focus,
    .input-box textarea:focus {
      border-color: #9333ea;
      box-shadow: 0 0 10px rgba(147, 51, 234, 0.3);
    }

    button {
      width: 100%;
      padding: 14px;
      margin-top: 10px;
      background: linear-gradient(135deg, #2563eb, #9333ea);
      border: none;
      border-radius: 16px;
      color: white;
      font-size: 16px;
      cursor: pointer;
      transition: 0.3s;
    }

    button:hover {
      opacity: 0.9;
      transform: translateY(-2px);
    }

    .action-button {
      padding: 8px 15px;
      border-radius: 8px;
      color: white;
      border: none;
      cursor: pointer;
      margin-right: 5px;
      transition: background 0.2s;
    }

    .approve-btn {
      background-color: #10b981;
    }

    .approve-btn:hover {
      background-color: #059669;
    }

    .deny-btn {
      background-color: #ef4444;
    }

    .deny-btn:hover {
      background-color: #dc2626;
    }

    .pending-label {
      display: inline-block;
      padding: 5px 10px;
      border-radius: 5px;
      background-color: #fcd34d;
      /* Yellow */
      color: #92400e;
      font-weight: 600;
    }

    .approved-label {
      display: inline-block;
      padding: 5px 10px;
      border-radius: 5px;
      background-color: #10b981;
      /* Green */
      color: white;
      font-weight: 600;
    }

    .denied-label {
      display: inline-block;
      padding: 5px 10px;
      border-radius: 5px;
      background-color: #ef4444;
      /* Red */
      color: white;
      font-weight: 600;
    }

    #dashboard {
      /* Set the dashboard background here */
      background:
        linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
        url(images/doctor.jpg);
      background-size: cover;
      background-position: center;
      background-attachment: fixed;
      /* Optional: Keep the background static */

      display: flex;
      width: 100%;
      height: 100vh;
      color: #1e293b;
    }

    .main {
      flex: 1;
      padding: 20px;
      overflow-y: auto;
      background: rgba(164, 168, 168, 0.95), url(images/hospital002.webp);
    }

    .card,
    .table-container {
      background: rgba(255, 255, 255, 0.98);
      padding: 25px;
      border-radius: 18px;
    }

    .sidebar {
      width: 260px;
      /* Ensure sidebar remains opaque for clean navigation */
      background: rgb(205, 206, 209);
      /* Changed from 0.85 to 1 for full opacity */
      padding: 25px;
      color: rgb(26, 25, 25);
      flex-shrink: 0;
    }

    .sidebar h2 {
      margin-bottom: 40px;
      color: #1a1919;
    }

    .sidebar a {
      display: flex;
      gap: 12px;
      padding: 12px;
      margin-bottom: 8px;
      color: #111112;
      text-decoration: none;
      border-radius: 10px;
      cursor: pointer;
      transition: background 0.3s;
    }

    .sidebar a:hover {
      background: #1e293b;
    }

    .topbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 30px;
      color: #c8c9cb;
      padding-bottom: 10px;
      border-bottom: 2px solid #e2e8f0;
    }

    .topbar h2 {
      font-size: 1.8rem;
    }

    .user-info {
      font-size: 0.9rem;
      color: #d9dde3;
    }

    .cards {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }

    .card {
      color: #65696e;
      border-left: 5px solid #2563eb;
      box-shadow: 0 8px 25px rgba(82, 2, 2, 0.1);
    }

    .card h4 {
      color: #64748b;
      margin-bottom: 5px;
    }

    .card h2 {
      font-size: 2.2rem;
    }

    .dashboard-greeting {
      color: #cbced4;
      font-weight: 600;
    }

    .card-student-total {
      background-color: #f7f3ff;
      /* Light purple background */
      border-left: 5px solid #28044a;
      /* Purple accent bar */
      padding: 20px;
      border-radius: 8px;
      box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .card-student-total h4 {
      color: #1b1b1c;
      font-size: 1.1em;
      margin-bottom: 5px;
    }

    .card-student-total h2 {
      color: #1a202c;
      font-size: 2.5em;
      margin: 0;
    }

    .card-student-total p {
      color: #f6f7f8;
      font-size: 0.9em;
      margin-top: 5px;
    }

    .camera-box {
      margin-top: 20px;
      padding: 22px;
      border-radius: 20px;
      color: rgb(17, 16, 16);
      background: #d3deef;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      position: relative;
    }

    .camera-box h3 {
      margin-bottom: 10px;
      color: #151515;
    }

    .camera-feed {
      width: 100%;
      max-width: 800px;
      height: auto;
      border-radius: 15px;
      border: 5px solid #2563eb;
      margin-top: 15px;
    }

    .table-container {
      margin-top: 20px;
      box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
      overflow-x: auto;
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
    }

    .data-table th,
    .data-table td {
      padding: 12px 15px;
      text-align: left;
      border-bottom: 1px solid #e2e8f0;
    }

    .data-table th {
      background-color: #f1f5f9;
      color: #1e293b;
      text-transform: uppercase;
      font-size: 0.85rem;
    }

    .data-table tbody tr:hover {
      background-color: #f8fafc;
    }

    /* Specific content containers */
    #registerStaff,
    #attendanceSession,
    #reportsSection,
    #requestPermission,
    #permissionReview {
      display: none;
    }

    .form-group {
      margin-bottom: 15px;
      display: flex;
      flex-direction: column;
      gap: 5px;
    }

    .form-group label {
      font-weight: 600;
      color: #dbd4d4;
    }

    /* Container for the camera UI */
    .camera-capture-box {
      display: none;
      /* Controlled by JS */
      margin-top: 20px;
      border-top: 2px solid #f0f2f5;
      padding-top: 15px;
      text-align: center;
    }

    .camera-status-label {
      color: #2563eb;
      font-weight: 600;
      font-size: 15px;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
    }

    /* Prevents the video from being cut off */
    .video-wrapper {
      position: relative;
      width: 100%;
      background: #000;
      border-radius: 12px;
      overflow: hidden;
      /* Clips the video to the border radius */
      line-height: 0;
      /* Removes extra spacing at bottom of video */
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
      margin-bottom: 15px;
    }

    #updateVideo {
      width: 100%;
      height: auto;
      max-height: 400px;
      /* Adjust this if the page is still too long */
      object-fit: cover;
      /* Ensures the face fills the area nicely */
    }

    /* Styling for the Action Buttons */
    .btn-capture {
      width: 100%;
      background: #2563eb;
      color: white;
      border: none;
      padding: 12px;
      border-radius: 8px;
      font-weight: 500;
      cursor: pointer;
      transition: background 0.3s ease;
    }

    .btn-capture:hover {
      background: #1d4ed8;
    }

    .btn-open-camera {
      width: 100%;
      margin-top: 15px;
      background: #f59e0b;
      color: white;
      border: none;
      padding: 12px;
      border-radius: 8px;
      font-weight: 500;
      cursor: pointer;
      transition:
        transform 0.2s ease,
        background 0.3s ease;
    }

    .btn-open-camera:hover {
      background: #d97706;
      transform: translateY(-1px);
    }

    @media (max-width: 100%) {
      .financial-cards-row {
        flex-direction: column !important;
      }
    }

    .input-box input,
    .form-control {
      transition: border-color 0.2s ease, background-color 0.2s ease;
      border: 1px solid #475569 !important;
      /* Forces initial matching default state */
    }

    .content-section {
      transition: opacity 0.3s ease-in-out;
      opacity: 1;
    }

    .btn-primary:hover {
      background: #2980b9;
    }

    input:focus {
      border-color: #3498db;
      outline: none;
      align-items: center;
      justify-content: center;
    }

    #resetPasswordPage {
      position: fixed;
      inset: 0;
      display: none;
      justify-content: center;
      align-items: center;
      background: #f8fafc;
      z-index: 9999;
    }

    #resetPasswordPage>div {
      width: 90%;
      max-width: 380px;
      background: #fff;
      border-radius: 24px;
      padding: 2.5rem;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08);
      text-align: center;
      border: 1px solid #e2e8f0;
    }
  </style>
</head>

<body onload="checkAuth()">
  <div id="loginPage" style="display: flex; justify-content: center; align-items: center; min-height: 100vh;">
    <div class="login-box">
      <h2>Welcome to FaceAttend</h2>
      <p style="color: #94a3b8">Enter your credentials to continue</p>

      <div class="input-box">
        <i class="fas fa-id-card"></i>
        <input id="loginId" placeholder="Staff ID" autocomplete="off" />
      </div>

      <div class="input-box">
        <i class="fas fa-lock"></i>
        <input id="loginPassword" type="password" placeholder="Password" autocomplete="new-password" />
      </div>

      <button onclick="login()">Login</button>
      <div id="error" style="color: red; margin-top: 8px"></div>

      <p style="text-align: right; margin-top: 10px;">
        <a href="#" onclick="showPage('forgotPasswordPage')"
          style="color: #3498db; text-decoration: none; font-size: 0.8rem;"></a>
      </p>
    </div>
  </div>


  <div id="forgotPasswordPage"
    style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #f8fafc; justify-content: center; align-items: center; z-index: 9999;">

    <div
      style="background: #ffffff; padding: 2.5rem; border-radius: 24px; width: 90%; max-width: 380px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08); text-align: center; border: 1px solid #e2e8f0;">

      <h2 style="color: #1e293b; font-size: 1.5rem; margin-bottom: 0.5rem;">Forgot Password? 🔑</h2>

      <p style="color: #64748b; margin-bottom: 1.5rem; font-size: 1rem;">No worries! Enter your Staff ID to receive a
        reset link.</p>

      <input type="text" id="fpStaffId" placeholder="Staff ID"
        style="width: 100%; padding: 14px; margin-bottom: 1rem; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 1rem; box-sizing: border-box;">

      <button onclick="requestReset()"
        style="width: 100%; padding: 14px; background: #3498db; color: white; border: none; border-radius: 12px; font-weight: 600; cursor: pointer;">Send
        Reset Link</button>

      <button onclick="showPage('loginPage')"
        style="width: 100%; padding: 12px; background: transparent; color: #94a3b8; border: none; margin-top: 10px; cursor: pointer; font-size: 0.85rem;">←
        Back to Login</button>

    </div>
  </div>
  <div id="resetPasswordPage"
    style="display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: #f8fafc; justify-content: center; align-items: center; z-index: 9999;">

    <div
      style="background: #ffffff; padding: 2.5rem; border-radius: 24px; width: 90%; max-width: 380px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08); text-align: center; border: 1px solid #e2e8f0;">

      <h2 style="color: #1e293b; font-size: 1.5rem; margin-bottom: 0.5rem;">Set New Password 🔐</h2>

      <p style="color: #64748b; margin-bottom: 1.5rem; font-size: 1rem;">Enter the token you received and your new
        password.</p>

      <input type="text" id="tokenInput" placeholder="Enter Token"
        style="width: 100%; padding: 14px; margin-bottom: 1rem; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 1rem; box-sizing: border-box;">

      <input type="password" id="newPassword" placeholder="New Password"
        style="width: 100%; padding: 14px; margin-bottom: 1rem; border: 2px solid #e2e8f0; border-radius: 12px; font-size: 1rem; box-sizing: border-box;">

      <button onclick="submitReset()"
        style="width: 100%; padding: 14px; background: #27ae60; color: white; border: none; border-radius: 12px; cursor: pointer; font-weight: 600;">Update
        Password</button>

      <button onclick="showPage('loginPage')"
        style="width: 100%; padding: 12px; background: transparent; color: #94a3b8; border: none; margin-top: 10px; cursor: pointer;">←
        Back to Login</button>
    </div>
  </div>



  <div id="passwordWrapper" style="
          display: none;
          align-items: center;
          justify-content: center;
          min-height: 100vh;
          width: 100%;
          background:
            linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)),
            url(images/strong.png);
        ">
    <div id="passwordSection" style="
            display: block;
            background: rgba(221, 236, 239, 0.95);
            width: 100%;
            max-width: 400px;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            border-top: 5px solid #6366f1;
            backdrop-filter: blur(10px);
          ">
      <h2 style="
              color: #080808;
              font-size: 26px;
              margin-bottom: 8px;
              font-weight: 700;
            ">
        Set Secure Password
      </h2>
      <p style="color: #191a1a; font-size: 14px; margin-bottom: 24px">
        For security, you must change your default password now.
      </p>

      <div style="
              background-color: rgba(99, 102, 241, 0.1);
              padding: 12px;
              border-radius: 10px;
              color: #0f0f0f;
              font-size: 13px;
              margin-bottom: 25px;
              border-left: 4px solid #6366f1;
            ">
        <strong>Requirement:</strong> Minimum 8 characters. Must contain at least one letter, one number, and one
        special
        sign
        (e.g., @, #, $, %, !).
      </div>

      <div id="passwordError" style="display: none; margin-bottom: 20px;"></div>

      <div style="margin-bottom: 20px">
        <label style="
                display: block;
                font-size: 14px;
                font-weight: 500;
                color: #131415;
                margin-bottom: 8px;
              ">New Strong Password</label>
        <input type="password" id="newPass" placeholder="••••••••" style="
                width: 100%;
                padding: 14px;
                background: #d9dae0;
                border: 1px solid #4b5563;
                border-radius: 10px;
                color: rgb(17, 16, 16);
                outline: none;
                box-sizing: border-box;
                transition: border-color 0.2s ease;
              " />
      </div>

      <div style="margin-bottom: 30px">
        <label style="
                display: block;
                font-size: 14px;
                font-weight: 500;
                color: #0e0f0f;
                margin-bottom: 8px;
              ">Confirm Password</label>
        <input type="password" id="confirmPass" placeholder="••••••••" style="
                width: 100%;
                padding: 14px;
                background: #ebedf9;
                border: 1px solid #4b5563;
                border-radius: 10px;
                color: rgb(14, 13, 13);
                outline: none;
                box-sizing: border-box;
                transition: border-color 0.2s ease;
              " />
      </div>

      <button onclick="finishSetup()" style="
              width: 100%;
              background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
              color: #ffffff;
              padding: 16px;
              border: none;
              border-radius: 12px;
              font-weight: 600;
              cursor: pointer;
              font-size: 16px;
              transition: transform 0.2s;
              box-shadow: 0 4px 15px rgba(79, 70, 229, 0.4);
            ">
        Update & Access Dashboard
      </button>

      <div style="margin-top: 20px; text-align: center">
        <button onclick="showLogin()" style="
                background: none;
                border: none;
                color: #19191a;
                cursor: pointer;
                text-decoration: none;
                font-size: 0.9rem;
                transition: color 0.3s;
              " onmouseover="this.style.color = '#4f46e5'" onmouseout="this.style.color = '#19191a'">
          ← Back to Login
        </button>
      </div>
    </div>
  </div>


  <div id="dashboard" style="display: none">
    <div class="sidebar">
      <h2>Face Attendance</h2>
      <div id="sidebar-links">
        <a id="dashBtn" onclick="showSection('dashboardContent')"><i class="fas fa-tachometer-alt"></i> Dashboard</a>
        <a id="registerStaffBtn" onclick="showSection('registerStaff')">
          <i class="fas fa-user-plus"></i> Register Staffs
        </a>
        <a id="attendanceBtn" onclick="showSection('attendanceSession')"><i class="fas fa-video"></i> Attendance
          Session</a>
        <a id="reportsBtn" onclick="showSection('reportsSection')"><i class="fas fa-file-alt"></i> Reports</a>
        <a id="financialBtn" onclick="showSection('financialDashboard')">
          <i class="fas fa-money-bill-wave"></i> Financial Dashboard
        </a>
        <a id="manageStaffBtn" onclick="
              showSection('staffManagement');
              loadStaffList();
            " style="display: none">
          <i class="fas fa-user-edit"></i> Manage Staffs
        </a>

        <a id="permissionReviewBtn" onclick="showSection('permissionReview')" style="display: none">
          <i class="fas fa-check-square"></i> Permission Review
          <span id="nav-notification-badge"
            style="background: red; color: white; border-radius: 50%; padding: 2px 6px; font-size: 10px; display: none; margin-left: 5px;">0</span>
        </a>

        <a id="requestPermissionBtn" onclick="showSection('requestPermission'); switchInnerTab('new-request');"
          style="display: none">
          <i class="fas fa-paper-plane"></i> Permission Request
        </a>

        <a id="myFinancialBtn" onclick="showSection('myFinancialSection')" style="display: none;">
          <i class="fa-solid fa-wallet"></i> My Financial Report
        </a>

      </div>
      <div class="margin-top: 50px">
        <a onclick="logout()"><i class="fas fa-sign-out-alt"></i> Logout</a>
      </div>
    </div>
    <div class="main">
      <div class="topbar">
        <h2 id="roleTitle"></h2>
        <div class="user-info">
          <i class="fas fa-user-circle"></i> <span id="userNameDisplay"></span>
        </div>
      </div>
      <div id="admin-notification-banner"
        style="display:none; background: #ff4757; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; align-items: center; justify-content: space-between; display: none;">
        <span><i class="fas fa-bell"></i> You have <span id="pending-request-count">0</span> new permission requests to
          review.</span>
        <button onclick="showSection('permissionReview')"
          style="background: white; color: #ff4757; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-weight: bold;">View
          Now</button>
      </div>


      <div id="dashboardContent" class="content-section" style="display: block">
        <div id="adminTeacherCards" class="cards">
          <div class="card card-student-total">
            <h4>Total Registered Staffs</h4>
            <h2 id="totalStaffCount">0</h2>
          </div>
          <div class="card card-student-total" style="border-left: 5px solid #502202; background-color: #fff7ed">
            <h4 style="color: #0f0e0e">Enrolled Face Records</h4>
            <h2 id="enrolledFacesCount">0</h2>
          </div>
          <div class="card card-student-total" style="border-left: 5px solid #052262; background-color: #eff6ff">
            <h4 style="color: #0f0f10">Present Today</h4>
            <h2 id="presentTodayCount">0</h2>
          </div>
        </div>

        <div id="staffDashboardInfo" style="display: none; padding: 20px">
          <h3 class="dashboard-greeting" style="color: #dbe5f5; font-size: 24px; margin-bottom: 5px">
            Hello, <span id="staffNameGreeting">Staff</span>!
          </h3>
          <p style="color: #b9bec6; margin-bottom: 25px">
            Welcome to your personalized attendance overview.
          </p>

          <div class="cards" style="
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 20px;
              ">
            <div class="card card-student-total" style="
                  padding: 20px;
                  border-radius: 10px;
                  border-left: 5px solid #2563eb;
                  background-color: #f8fafc;
                  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                ">
              <h4 style="
                    color: #64748b;
                    font-size: 14px;
                    text-transform: uppercase;
                  ">
                Total Attended
              </h4>

              <h2 id="totalClassesAttended" style="font-size: 36px; margin: 10px 0; color: #1e293b">
                --
              </h2>
              <p style="font-size: 12px; color: #94a3b8">
                Attendance records found in this month
              </p>
            </div>

            <div class="card card-student-total" style="
                  padding: 20px;
                  border-radius: 10px;
                  border-left: 5px solid #440202;
                  background-color: #fef2f2;
                  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                ">
              <h4 style="
                    color: #0b0b0b;
                    font-size: 14px;
                    text-transform: uppercase;
                  ">
                Unexcused Absences
              </h4>
              <h2 id="unexcusedAbsences" style="font-size: 36px; margin: 10px 0; color: #0b0b0b">
                --
              </h2>
              <p style="font-size: 12px; color: #991b1b">
                Unexcused absences this month.
              </p>
            </div>

            <div class="card card-student-total" style="
                  padding: 20px;
                  border-radius: 10px;
                  border-left: 5px solid #013414;
                  background-color: #f0fdf4;
                  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                ">
              <h4 style="
                    color: #121312;
                    font-size: 14px;
                    text-transform: uppercase;
                  ">
                Approved Leaves
              </h4>
              <h2 id="approvedLeavesCount" style="font-size: 36px; margin: 10px 0; color: #121312">
                --
              </h2>
              <p style="font-size: 12px; color: #14532d">
                Excused absences this month.
              </p>
            </div>
          </div>
        </div>
      </div>

      <div id="requestPermission" class="content-section">
        <h2 style="color: white; margin-bottom: 5px;"><i class="fas fa-paper-plane"></i> Leave Management Portal</h2>
        <p style="color: #e3e5e8; margin-bottom: 20px">Manage your absence authorizations and check real-time evaluation
          states.</p>

        <div class="inner-tabs"
          style="display: flex; gap: 10px; margin-bottom: 20px; border-bottom: 1px solid #334155; padding-bottom: 10px;">
          <button id="tab-new-request" onclick="switchInnerTab('new-request')"
            style="background: #2563eb; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 500; transition: all 0.3s;">
            <i class="fas fa-plus-circle"></i> New Absence Request
          </button>
          <button id="tab-request-history" onclick="switchInnerTab('request-history')"
            style="background: #1e293b; color: #94a3b8; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer; font-weight: 500; transition: all 0.3s;">
            <i class="fas fa-history"></i> View Request History
          </button>
        </div>

        <div id="inner-view-new-request" class="inner-tab-content" style="display: block;">
          <div class="card"
            style="padding: 30px; max-width: 600px; background: white; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <div id="leaveFormMessage" style="color: #0e0e0f; margin-bottom: 15px; font-weight: 500;"></div>

            <div class="form-group" style="margin-bottom: 15px;">
              <label for="leaveType" style="color: #0b0b0b; display: block; margin-bottom: 8px; font-weight: 600;">
                <i class="fas fa-layer-group"></i> Type of Leave / ፍቃድ አይነት <span style="color: red">*</span>
              </label>
              <select id="leaveType" name="leaveType" onchange="toggleLeaveTypeNotice()"
                style="width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #a1afe7; outline: none; font-size: 14px; background: white; color: black;"
                required>
                <option value="emergency_leave">Emergency Leave / አስቸኳይ ፍቃድ </option>
                <option value="yearly_leave">Yearly Leave / ዓመት እረፍት ፍቃድ </option>

              </select>
            </div>

            <div class="form-group" style="margin-bottom: 15px;">
              <label for="leaveDateRange" style="color: #0b0b0b; display: block; margin-bottom: 8px; font-weight: 600;">
                <i class="fas fa-calendar-alt"></i> Start Date / መነሻ ቀን <span style="color: red">*</span>
              </label>
              <input type="date" id="leaveDateRange" name="leaveDateRange"
                style="width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #a1afe7; outline: none;"
                required />
            </div>

            <div class="form-group" style="margin-bottom: 15px;">
              <label for="leaveDuration" style="color: #0b0b0b; display: block; margin-bottom: 8px; font-weight: 600;">
                <i class="fas fa-hourglass-half"></i> Duration (Number of Days) / የባዶ ቀናት ብዛት <span
                  style="color: red">*</span>
              </label>
              <input type="number" id="leaveDuration" name="leaveDuration" min="1" max="30" value="1"
                style="width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #a1afe7; outline: none;"
                required />
            </div>

            <div class="form-group" style="margin-bottom: 20px;">
              <label for="reasonText" style="color: #0b0b0b; display: block; margin-bottom: 8px; font-weight: 600;">
                Reason for Absence / የፍቃድ ምክንያት <span style="color: red">*</span>
              </label>
              <div class="input-box">
                <textarea id="reasonText" name="reasonText" rows="3"
                  placeholder="e.g., Annual family trip, medical rest requirement, etc. Description is required for administrative verification."
                  style="width: 100%; padding: 10px; border-radius: 10px; border: 1px solid #a1afe7; outline: none; transition: all 0.3s; resize: vertical;"></textarea>

                <div class="form-group" style="margin-top: 15px;">
                  <label for="supportingFile"
                    style="color: #0b0b0b; display: block; margin-bottom: 4px; font-weight: 600;">Supporting
                    Document</label>
                  <input type="file" class="form-control" id="supportingFile" accept=".pdf, .jpg, .png, .jpeg"
                    style="width:100%;" />
                  <small class="form-text text-muted" style="display:block; margin-top:4px;">Max file size 2MB. Accepts
                    PDF,
                    JPG, or PNG.</small>
                </div>
              </div>
            </div>

            <button onclick="submitLeaveRequest()"
              style="width: 100%; padding: 12px; border-radius: 8px; background: #2563eb; color: white; border: none; font-weight: bold; cursor: pointer; font-size: 16px; transition: background 0.2s;">
              Submit Leave Request
            </button>
          </div>
        </div>

        <div id="inner-view-request-history" class="inner-tab-content" style="display: none;">
          <div class="card" style="max-width: 800px; background: rgba(30, 41, 59, 0.7); padding: 25px;">
            <h3 style="color: white; margin-bottom: 15px;"><i class="fas fa-history"></i> My Request History</h3>
            <div class="table-container">
              <table class="data-table" style="width: 100%; border-collapse: collapse; text-align: left;">
                <thead>
                  <tr style="border-bottom: 2px solid #334155; color: #94a3b8;">
                    <th style="padding: 12px;">Date Requested</th>
                    <th style="padding: 12px;">My Reason</th>
                    <th style="padding: 12px;">Status</th>
                    <th style="padding: 12px;">Admin Remarks / Notes</th>
                  </tr>
                </thead>
                <tbody id="staffRequestHistory">
                  <tr>
                    <td colspan="4" class="text-center" style="padding: 20px; color: #64748b;">No requests found.</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
      <div id="permissionReview" class="content-section">
        <h2 style="color: white">Review Absence Requests</h2>
        <div id="requestsTableContainer" class="table-container">
          <table id="requestsTable" class="data-table">
            <thead>
              <tr>
                <th>Request ID</th>
                <th>Staff ID</th>
                <th>Staff Name</th>
                <th>Date</th>
                <th>Duration</th>
                <th>Reason</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody id="requestsTableBody">
              <tr>
                <td colspan="7" class="text-center">
                  No pending absence requests found.
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div id="admin-notification-banner"
          style="display:none; background: #ff4757; color: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; align-items: center; justify-content: space-between;">
          <span><i class="fas fa-bell"></i> You have <span id="pending-request-count">0</span> new permission requests
            to
            review.</span>
          <button onclick="showPage('permissionReview')"
            style="background: white; color: #ff4757; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; font-weight: bold;">View
            Now</button>
        </div>

      </div>
      <div id="registerStaff" class="content-section" style="
            display: none;
            min-height: 100vh;
            background:
              linear-gradient(rgba(0, 0, 0, 0.55), rgba(0, 0, 0, 0.65)),
              url(&quot;./images/student.png&quot;) center/cover no-repeat fixed;
          ">
        <div style="max-width: 900px; margin: 40px auto; padding: 20px">
          <h2 style="
                color: #ffffff;
                text-shadow: 0 2px 8px rgba(0, 0, 0, 0.7);
                margin-bottom: 8px;
              ">
            Register New Staff Member
          </h2>
          

          <div class="card" style="
                background: rgba(40, 44, 52, 0.92);
                backdrop-filter: blur(8px);
                border: 1px solid rgba(100, 110, 130, 0.35);
                border-radius: 20px;
                padding: 35px 40px;
                box-shadow: 0 15px 40px rgba(0, 0, 0, 0.55);
              ">
            <div id="enrollMessage" style="
                  min-height: 24px;
                  margin-bottom: 24px;
                  font-weight: 500;
                  font-size: 1.05rem;
                "></div>

            <div class="form-group" style="margin-bottom: 24px">
              <label for="staffIdInput" style="
                    color: #e0e7ff;
                    font-weight: 500;
                    margin-bottom: 8px;
                    display: block;
                  ">
                Staff ID
              </label>
              <div class="input-box">
                <i class="fas fa-id-card"></i>
                <input type="text" id="staffIdInput" placeholder="Staff ID" />
              </div>
            </div>

            <div class="form-group" style="margin-bottom: 24px">
              <label for="staffNameInput" style="
                    color: #e0e7ff;
                    font-weight: 500;
                    margin-bottom: 8px;
                    display: block;
                  ">
                Full Name
              </label>
              <div class="input-box">
                <i class="fas fa-user"></i>
                <input type="text" id="staffNameInput" placeholder="Full Name" />
              </div>
            </div>

            <div class="form-group mb-3">
              <label style="font-weight: 600; color: #cbd5e1; display: block; margin-bottom: 8px;">Sex</label>
              <select id="registerSex" class="form-control"
                style="width: 100%; padding: 10px; border-radius: 6px; background: #1e293b; color: white; border: 1px solid #475569;">
                <option value="" disabled selected>Select Sex</option>
                <option value="Female">Female</option>
                <option value="Male">Male</option>
              </select>
            </div>

            <div class="form-group" style="margin-bottom: 24px">
              <label for="staffDeptInput" style="
                    color: #e0e7ff;
                    font-weight: 500;
                    margin-bottom: 8px;
                    display: block;
                  ">
                Department
              </label>
              <div class="input-box">
                <i class="fas fa-building"></i>
                <input type="text" id="staffDeptInput" placeholder=" Department" />
              </div>
            </div>

            <div class="form-group" style="margin-bottom: 15px;">
              <label style="color: #cbd5e1; display: block; margin-bottom: 5px; font-weight: 500;">Monthly Salary 
                </label>
              <input type="number" id="regBaseSalary" placeholder="e.g., 18000" min="0" required
                style="width: 100%; padding: 10px; background: #1e293b; border: 1px solid #334155; color: white; border-radius: 6px;">
            </div>

            <div class="form-group" style="margin-bottom: 15px;">
              <label style="color: #cbd5e1; display: block; margin-bottom: 5px; font-weight: 500;">Daily Salary
                
                </label>
              <input type="number" id="regOvertimeRate" placeholder="e.g., 250" min="0" required
                style="width: 100%; padding: 10px; background: #1e293b; border: 1px solid #334155; color: white; border-radius: 6px;">
            </div>

            <div class="form-group" style="margin-bottom: 32px">
              <label for="numCaptures" style="
                    color: #e0e7ff;
                    font-weight: 500;
                    margin-bottom: 8px;
                    display: block;
                  ">
                Number of face photos to capture
              </label>
              <select id="numCaptures" style="
                    background: #1f2937;
                    color: #e5e7eb;
                    border: 1px solid #4b5563;
                    padding: 12px 16px;
                    border-radius: 10px;
                    width: 100%;
                  ">
                <option value="3">3 – faster but less accurate</option>
                <option value="5" selected>
                  5 – good balance (recommended)
                </option>
                <option value="7">7 – better accuracy</option>
                <option value="10">10 – highest accuracy</option>
              </select>
            </div>

            <button onclick="enroll_staff(event)" style="width: 100%; padding: 14px; font-size: 1.1rem">
              Start Face Enrollment
            </button>
          </div>
        </div>
      </div>

      <div id="attendanceSession" class="content-section">
        <h2 style="color: white">Live Attendance Session</h2>
        <div style="display: flex; gap: 15px; margin-bottom: 20px">
          <button onclick="startAttendance()" style="
                width: 200px;
                background: #22c55e;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                cursor: pointer;
              ">
            Start Live Feed
          </button>
          <button onclick="stopAttendance()" style="
                width: 200px;
                background: #dc2626;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                cursor: pointer;
              ">
            Stop Live Feed
          </button>
        </div>

        <div class="camera-box" style="
              background: #000;
              padding: 10px;
              border-radius: 10px;
              min-height: 400px;
              display: flex;
              flex-direction: column;
              align-items: center;
              justify-content: center;
            ">
          <h3 style="color: #ccc">Live Camera Feed</h3>
          <img id="cameraFeed" class="camera-feed" style="
                display: none;
                width: 100%;
                max-width: 640px;
                border: 3px solid #22c55e;
                background: #000;
              " />
          <div id="cameraStatus" style="color: white; margin-top: 10px">
            Feed Stopped. Click 'Start Live Feed'
          </div>
        </div>
        <div id="attendanceMessage" style="margin-top: 15px; font-weight: bold"></div>
      </div>


      <div id="reportsSection" class="content-section">
        <h2 style="color: white; margin-bottom: 20px">
          <i class="fas fa-chart-bar"></i> Hospital Attendance Reports
        </h2>

        <div class="tab-navigation" style="display: flex; gap: 10px; margin-bottom: 20px">
          <button onclick="switchReportTab('daily')" id="tabBtnDaily" class="btn btn-primary">
            Daily Shift Report
          </button>
          <button onclick="switchReportTab('monthly')" id="tabBtnMonthly" class="btn btn-secondary">
            Monthly Summary
          </button>
          <button onclick="switchReportTab('yearly')" id="tabBtnYearly" class="btn btn-secondary">
            Yearly Balance(ዓመት እረፍት ፍቃድ ሪፖርት)
          </button>
        </div>

        <div id="tabDailyContent">
          <div class="report-controls card p-3 mb-4" style="background: #f1f5f9; border-left: 5px solid #64748b">
            <div style="display: flex; gap: 20px; align-items: center">
              <label style="font-weight: 600; color: #1e293b">View Date:</label>
              <input type="date" id="reportDate" class="form-control" onchange="loadReports()" style="width: auto" />
              <span id="reportStatus" style="color: #64748b">Select a date</span>
            </div>
          </div>

          <h3 style="color: #f1c40f"><i class="fas fa-sun"></i> Day Shift (2- 12)</h3>
          <div class="table-container mb-4">
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Dept</th>
                  <th>Date</th>
                  <th>Clock In(2-3)</th>
                  <th>Clock Out(11-12)</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody id="dayReportsTableBody"></tbody>
            </table>
          </div>

          <h3 style="color: #1908b1e7"><i class="fas fa-moon"></i> Night Shift (12 - 2)</h3>
          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Dept</th>
                  <th>Date</th>
                  <th>Clock In(12-1)</th>
                  <th>Clock Out(1-2)</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody id="nightReportsTableBody"></tbody>
            </table>
          </div>
        </div>

        <div id="tabMonthlyContent" style="display: none">
          <div class="report-controls card p-3 mb-4" style="background: #f1f5f9; border-left: 5px solid #27ae60">
            <div style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
              <label style="font-weight: 600; color: #1e293b; margin: 0;">Select Month:</label>
              <input type="month" id="summaryMonth" class="form-control" style="width: auto" value="" />
              <button onclick="loadMonthlySummary()" class="btn btn-success">
                <i class="fas fa-sync"></i> Generate Summary
              </button>

              <button onclick="sendCompiledReportToFinance()" id="btnSendFinance" class="btn"
                style="background: #10b981; color: white; font-weight: bold; display: none; padding: 8px 16px; border-radius: 6px; border: none; cursor: pointer;">
                <i class="fas fa-paper-plane"></i> Send to Finance
              </button>
            </div>
          </div>

          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Staff ID</th>
                  <th>Name</th>
                  <th>Days Present</th>
                  <th>Approved Leaves</th>
                  <th>Absences</th>
                  <th>Performance</th>
                </tr>
              </thead>
              <tbody id="summaryTableBody">
                <tr>
                  <td colspan="6" class="text-center">Click "Generate Summary" to load data</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div id="tabYearlyContent" style="display: none">
          <div class="report-controls card p-3 mb-4" style="background: #f1f5f9; border-left: 5px solid #3b82f6">
            <div style="display: flex; gap: 20px; align-items: center">
              <label style="font-weight: 600; color: #1e293b">Select Year:</label>
              <select id="summaryYear" class="form-control"
                style="width: auto; background: white; color: black; border: 1px solid #cbd5e1; padding: 6px 12px; border-radius: 4px;">
                <option value="2026" selected>2026</option>
                <option value="2027">2027</option>
              </select>
              <button onclick="loadYearlySummary()" class="btn btn-primary"
                style="background: #3b82f6; border: none; padding: 7px 15px; border-radius: 4px; color: white; font-weight: bold;">
                Generate Yearly Log
              </button>
            </div>
          </div>

          <div class="table-container">
            <table class="data-table">
              <thead>
                <tr style="background: #1e293b; color: #38bdf8;">
                  <th>Staff ID</th>
                  <th>Name</th>
                  <th>Total Approved Leave Days</th>
                  <th>Remaining Balance (From 30 Days)</th>
                  <th>Status Track</th>
                </tr>
              </thead>
              <tbody id="yearlyTableBody">
                <tr>
                  <td colspan="5" class="text-center" style="color: #94a3b8; padding: 20px; font-style: italic;">
                    Select a year and click "Generate Yearly Log" to calculate tracking data.
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

      </div>

      <!-- ==================== STAFF MANAGEMENT ==================== -->
      <div id="staffManagement" class="content-section" style="display: none; padding: 20px">
        <h2 style="color: white; margin-bottom: 20px">
          <i class="fas fa-users-cog"></i> Manage Hospital Staff Records
        </h2>
        <div class="search-wrapper" style="position: relative; margin-bottom: 20px; width: 100%">
          <span
            style="position: absolute; left: 12px; top: 50%; transform: translateY(-50%); display: flex; align-items: center;">
            <svg width="20" height="20" viewBox="0 0 25 25" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M10.4167 0C15.7555 0 20.0833 4.32792 20.0833 9.66667C20.0833 11.9759 19.2736 14.0959 17.9227 15.7584L24.4571 22.2929C24.8476 22.6835 24.8476 23.3165 24.4571 23.7071C24.1021 24.0621 23.5465 24.0944 23.1551 23.8039L23.0429 23.7071L16.5084 17.1727C14.8459 18.5236 12.7259 19.3333 10.4167 19.3333C5.07792 19.3333 0.75 15.0055 0.75 9.66667C0.75 4.32792 5.07792 0 10.4167 0ZM10.4167 2C6.18248 2 2.75 5.43248 2.75 9.66667C2.75 13.9008 6.18248 17.3333 10.4167 17.3333C14.6508 17.3333 18.0833 13.9008 18.0833 9.66667C18.0833 5.43248 14.6508 2 10.4167 2Z"
                fill="#767676"></path>
            </svg>
          </span>
          <input type="text" id="staffSearchInput" onkeyup="filterStaffTable()" placeholder="Search"
            style="width: 100%; padding: 12px 12px 12px 40px; border: 1px solid #cbd5e1; border-radius: 8px; font-size: 15px; outline: none;" />
        </div>
        <div class="table-container" style="background: rgba(255, 255, 255, 0.9); border-radius: 10px; padding: 15px;">
          <table class="data-table" style="width: 100%; border-collapse: collapse">
            <thead>
              <tr style="background: #1e293b; color: white">
                <th style="padding: 12px">Staff ID</th>
                <th>Full Name</th>
                <th>Department</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody id="staffTableBody" style="color: #1e293b; text-align: center"></tbody>
          </table>
        </div>
      </div>

      <!-- ==================== EDIT MODAL (Cleaned) ==================== -->
      <div id="editModal"
        style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0, 0, 0, 0.7); z-index: 10000; overflow-y: auto; padding: 20px 0;">
        <div
          style="background: white; width: 95%; max-width: 460px; margin: 30px auto; padding: 25px; border-radius: 12px; box-shadow: 0 15px 35px rgba(0,0,0,0.3); position: relative;">

          <h3 style="margin-bottom: 20px; color: #1e293b; border-bottom: 1px solid #e2e8f0; padding-bottom: 10px;">
            Edit Staff Record
          </h3>

          <input type="hidden" id="editOldId" />

          <div style="margin-bottom: 15px">
            <label style="display: block; font-size: 13px; font-weight: 600; color: #475569; margin-bottom: 5px;">Staff
              ID:</label>
            <input type="text" id="editNewId"
              style="width: 100%; padding: 9px; border: 1px solid #cbd5e1; border-radius: 6px;" />
          </div>

          <div style="margin-bottom: 15px">
            <label style="display: block; font-size: 13px; font-weight: 600; color: #475569; margin-bottom: 5px;">Full
              Name:</label>
            <input type="text" id="editName"
              style="width: 100%; padding: 9px; border: 1px solid #cbd5e1; border-radius: 6px;" />
          </div>

          <div style="margin-bottom: 15px">
            <label
              style="display: block; font-size: 13px; font-weight: 600; color: #475569; margin-bottom: 5px;">Department:</label>
            <input type="text" id="editDept"
              style="width: 100%; padding: 9px; border: 1px solid #cbd5e1; border-radius: 6px;" />
          </div>

          <div style="margin-bottom: 15px">
            <label style="display: block; font-size: 13px; font-weight: 600; color: #475569; margin-bottom: 5px;">Base
              Monthly
              Salary (ETB):</label>
            <input type="number" id="editSalary"
              style="width: 100%; padding: 9px; border: 1px solid #cbd5e1; border-radius: 6px;" />
          </div>

          <div style="margin-bottom: 20px">
            <label style="display: block; font-size: 13px; font-weight: 600; color: #475569; margin-bottom: 5px;">Daily
              Overtime Rate (ETB):</label>
            <input type="number" id="editOvertime"
              style="width: 100%; padding: 9px; border: 1px solid #cbd5e1; border-radius: 6px;" />
          </div>

          <!-- Re-scan Option -->
          <div
            style="margin: 20px 0; padding: 12px; background: #fff7ed; border: 1px solid #fed7aa; border-radius: 8px;">
            <label style="display: flex; align-items: center; cursor: pointer; color: #9a3412; font-weight: bold;">
              <input type="checkbox" id="reScanFace" style="margin-right: 10px; width: 18px; height: 18px;" />
              Update Face Image (Re-scan)
            </label>
            <p style="font-size: 11px; color: #c2410c; margin: 5px 0 0 28px; line-height: 1.4;">
              Checking this will delete current face data and enable the camera capture section below.
            </p>
          </div>

          <!-- Camera Section -->
          <div id="directUpdateArea" class="camera-capture-box" style="margin-top: 15px; display: none;">
            <p class="camera-status-label" style="font-size: 14px; margin-bottom: 10px;">
              <i class="fas fa-video"></i> Live Face Update
            </p>
            <div class="video-wrapper" style="background:#000; border-radius:8px; overflow:hidden; margin-bottom:10px;">
              <video id="updateVideo" autoplay playsinline
                style="width:100%; max-height:260px; object-fit:cover;"></video>
              <canvas id="updateCanvas" style="display:none;"></canvas>
            </div>
            <div id="captureProgress" style="margin-bottom:12px; font-weight:bold; color:#2563eb; text-align:center;">
              Ready to capture
            </div>
            <div style="display:flex; gap:10px;">
              <button type="button" onclick="captureMultipleFaces(event)"
                style="flex:2; padding:11px; background:#2563eb; color:white; border:none; border-radius:6px; font-weight:600;">
                <i class="fas fa-camera"></i> Capture & Update
              </button>
              <button type="button" onclick="cancelReScan()"
                style="flex:1; padding:11px; background:#ef4444; color:white; border:none; border-radius:6px;">
                Cancel
              </button>
            </div>
          </div>

          <button type="button" onclick="openUpdateCamera()"
            style="width:100%; margin:15px 0; padding:11px; background:#f59e0b; color:white; border:none; border-radius:6px; cursor:pointer;">
            <i class="fas fa-video"></i> Open Camera for New Scan
          </button>

          <!-- Bottom Buttons -->
          <div style="text-align:right; margin-top:25px; padding-top:15px; border-top:1px solid #e2e8f0;">
            <button onclick="closeEditModal()"
              style="padding:10px 20px; margin-right:10px; background:#64748b; color:white; border:none; border-radius:6px; cursor:pointer;">
              Cancel
            </button>
            <button type="button" onclick="saveEdit(); return false;"
              style="padding:10px 22px; background:#2563eb; color:white; border:none; border-radius:6px; cursor:pointer; font-weight:600;">
              Save Changes
            </button>
          </div>
        </div>
      </div>

      <div id="financialDashboard" class="content-section"
        style="background: #ffffff; padding: 32px; border-radius: 24px; border: 1px solid #e2e8f0; box-shadow: 0 20px 40px -15px rgba(148, 163, 184, 0.12); font-family: 'Poppins', sans-serif; transition: all 0.3s ease;">

        <div
          style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; flex-wrap: wrap; gap: 24px;">
          <div>
            <h2
              style="color: #0f172a; margin-bottom: 8px; font-size: 1.75rem; font-weight: 600; display: flex; align-items: center; gap: 14px; letter-spacing: -0.5px;">
              <span
                style="background: linear-gradient(135deg, #e6fbf7, #e0f2fe); color: #0d9488; width: 48px; height: 48px; border-radius: 16px; display: inline-flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(13, 148, 136, 0.08);">
                <i class="fas fa-money-bill-wave" style="font-size: 1.25rem;"></i>
              </span>
              Financial Dashboard
            </h2>
            <p style="color: #64748b; font-size: 0.95rem; margin-left: 2px;">Calculate administrative salaries based on
              validated attendance tracking records (<span style="color: #0d9488; font-weight: 600;">Birr</span>).</p>
          </div>

          <div style="display: flex; align-items: center; justify-content: flex-end; gap: 16px; flex-wrap: wrap;">

            <div
              style="display: flex; align-items: center; gap: 12px; background: #f8fafc; padding: 6px 18px; border-radius: 14px; border: 1px solid #e2e8f0; height: 48px; box-shadow: 0 2px 4px rgba(0,0,0,0.01); transition: all 0.2s ease-in-out;"
              onmouseover="this.style.borderColor='#0d9488'; this.style.background='#ffffff'; this.style.boxShadow='0 4px 12px rgba(13, 148, 136, 0.05)';"
              onmouseout="this.style.borderColor='#e2e8f0'; this.style.background='#f8fafc'; this.style.boxShadow='0 2px 4px rgba(0,0,0,0.01)';">
              <label
                style="color: #475569; font-size: 0.78rem; font-weight: 700; margin: 0; white-space: nowrap; text-transform: uppercase; letter-spacing: 0.8px; display: flex; align-items: center; gap: 6px;">
                <i class="far fa-calendar-alt" style="color: #0d9488; font-size: 0.9rem;"></i> Payroll Month
              </label>
              <input type="month" id="financialMonth" class="form-control" onchange="loadPayroll()"
                style="width: 140px !important; background: transparent; color: #0f172a; border: none; padding: 0; font-size: 0.95rem; font-weight: 600; outline: none; cursor: pointer; font-family: inherit;">
            </div>

            <button class="btn-success"
              style="padding: 0 24px; height: 48px; border-radius: 14px; border: none; cursor: pointer; white-space: nowrap; background: linear-gradient(135deg, #0ea5e9, #0d9488); color: #ffffff; font-weight: 600; font-size: 0.95rem; display: inline-flex; align-items: center; gap: 10px; box-shadow: 0 6px 20px rgba(13, 148, 136, 0.18); transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1); font-family: inherit;"
              onclick="downloadFinancialReport()"
              onmouseover="this.style.transform='translateY(-2px)'; this.style.boxShadow='0 8px 24px rgba(13, 148, 136, 0.28)'; this.style.filter='brightness(1.05)';"
              onmouseout="this.style.transform='translateY(0)'; this.style.boxShadow='0 6px 20px rgba(13, 148, 136, 0.18)'; this.style.filter='brightness(1)';">
              <i class="fas fa-download" style="font-size: 0.9rem;"></i> Download Export
            </button>
          </div>
        </div>

        <div class="table-container"
          style="background: #ffffff; border-radius: 20px; border: 1px solid #e2e8f0; overflow: hidden; box-shadow: 0 4px 16px rgba(148, 163, 184, 0.02);">
          <table class="data-table"
            style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.92rem;">
            <thead>
              <tr style="background: linear-gradient(180deg, #f8fafc, #f1f5f9); border-bottom: 2px solid #e2e8f0;">
                <th
                  style="padding: 20px 18px; color: #475569; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.8px;">
                  Staff ID</th>
                <th
                  style="padding: 20px 18px; color: #475569; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.8px;">
                  Name</th>
                <th
                  style="padding: 20px 18px; color: #475569; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.8px;">
                  Department</th>
                <th
                  style="padding: 20px 18px; color: #475569; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.8px; text-align: center;">
                  Present Days</th>
                <th
                  style="padding: 20px 18px; color: #475569; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.8px; text-align: center;">
                  Absent Days</th>
                <th
                  style="padding: 20px 18px; color: #475569; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.8px;">
                  Base Salary</th>
                <th
                  style="padding: 20px 18px; color: #475569; font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.8px;">
                  Deduction</th>
                <th
                  style="padding: 20px 18px; color: #0d9488; font-weight: 700; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.8px; background: rgba(13, 148, 136, 0.02);">
                  Final Salary</th>
              </tr>
            </thead>
            <tbody id="payrollTableBody">
              <tr>
                <td colspan="8" style="padding: 70px 24px; text-align: center; background: #ffffff;">
                  <div
                    style="display: flex; flex-direction: column; align-items: center; gap: 16px; max-width: 420px; margin: 0 auto;">
                    <div
                      style="background: linear-gradient(135deg, #f1f5f9, #e2e8f0); color: #94a3b8; width: 64px; height: 64px; border-radius: 50%; display: inline-flex; align-items: center; justify-content: center; box-shadow: 0 4px 12px rgba(0,0,0,0.02);">
                      <i class="far fa-calendar-alt" style="font-size: 1.75rem; color: #64748b;"></i>
                    </div>
                    <div style="display: flex; flex-direction: column; gap: 4px;">
                      <span style="font-size: 1rem; color: #334155; font-weight: 600;">No Payroll Generated</span>
                      <span style="font-size: 0.88rem; line-height: 1.5; color: #64748b;">Select an administrative
                        target
                        month window from the selection menu to evaluate user logs.</span>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <div id="myFinancialSection" class="content-section"
        style="display: none; width: 100%; height: 100%; box-sizing: border-box; font-family: 'Poppins', sans-serif; padding: 20px; overflow-y: auto;">

        <div style="width: 100%; min-height: 100%; display: flex; flex-direction: column; gap: 20px;">

          <div class="card" style="
                          background: rgba(255, 255, 255, 0.98); 
                          border-radius: 18px; 
                          padding: 20px 30px; 
                          display: flex; 
                          justify-content: space-between; 
                          align-items: center;
                          box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
                          border-left: 5px solid #3b82f6;
                        ">
            <!-- Left: Title & User -->
            <div>
              <h2 style="margin: 0; font-size: 22px; font-weight: 700; color: #1e293b;">
                <i class="fa-solid fa-file-invoice-dollar" style="color: #3b82f6; margin-right: 10px;"></i>My Financial
                Report
              </h2>
              <div
                style="color: #64748b; font-size: 13px; margin-top: 5px; display: flex; align-items: center; gap: 8px;">
                <i class="fas fa-user-circle" style="color: #94a3b8;"></i>
                <span id="currentStaffProfileName" style="font-weight: 600; color: #334155;">Staff Member</span>
              </div>
            </div>

            <!-- Right: Controls -->
            <div style="display: flex; gap: 15px; align-items: center;">
              <div
                style="display: flex; align-items: center; gap: 10px; background: #f8fafc; padding: 8px 15px; border-radius: 10px; border: 1px solid #e2e8f0;">
                <i class="far fa-calendar-alt" style="color: #64748b;"></i>
                <input type="month" id="staffMonthInput"
                  style="background: transparent; border: none; color: #1e293b; font-size: 14px; font-weight: 600; outline: none; cursor: pointer; width: 130px; color-scheme: light;">
              </div>
              <button onclick="loadStaffPersonalPayroll()"
                style="background: linear-gradient(135deg, #2563eb, #1d4ed8); color: white; border: none; padding: 10px 22px; border-radius: 10px; cursor: pointer; font-weight: 600; font-size: 14px; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2); transition: transform 0.2s; display: flex; align-items: center; gap: 8px;">
                <i class="fa-solid fa-sync"></i> Generate
              </button>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px; flex: 1;">

            <div id="personalReportCard" class="card"
              style="display: none; background: rgba(255, 255, 255, 0.98); border-radius: 18px; border-left: 5px solid #10b981; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); padding: 0; overflow: hidden;">

              <div
                style="background: #f8fafc; padding: 15px 25px; border-bottom: 1px solid #e2e8f0; display: flex; justify-content: space-between; align-items: center;">
                <h3 id="myReportTitle" style="margin: 0; color: #334155; font-size: 16px; font-weight: 700;">Salary
                  Statement
                </h3>
                <div
                  style="background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 6px; font-size: 11px; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase;">
                  Processed
                </div>
              </div>

              <div style="padding: 30px;">

                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 40px;">

                  <div>
                    <div
                      style="color: #64748b; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;">
                      Base Monthly Salary</div>

                    <div id="myBaseSalary" style="font-size: 32px; font-weight: 700; color: #1e293b;">0.00 ETB</div>
                  </div>

                  <div>
                    <div
                      style="color: #64748b; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;">
                      Deductions</div>
                    <div style="color: #475569; font-size: 15px; margin-bottom: 8px; font-weight: 500;">
                    </div>
                    <div id="myDeductions" style="font-size: 32px; font-weight: 700; color: #ef4444;">- 0.00 ETB</div>
                  </div>

                </div>

                <div
                  style="background: #f0fdf4; border: 1px solid #bbf7d0; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
                  <div>
                    <div style="color: #15803d; font-size: 13px; font-weight: 600; margin-bottom: 4px;">NET PAYABLE
                      AMOUNT
                    </div>
                    <div style="color: #166534; font-size: 12px; font-weight: 500;">To be credited to your account</div>
                  </div>
                  <div id="myFinalSalary" style="font-size: 36px; font-weight: 800; color: #16a34a;">0.00 ETB</div>
                </div>

              </div>
            </div>

            <div id="staffStatsCards" style="display: none; flex-direction: column; gap: 20px;">

              <div class="card"
                style="flex: 1; background: rgba(255, 255, 255, 0.98); border-radius: 18px; border-left: 5px solid #64748b; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); padding: 25px; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center;">
                <div
                  style="background: #f1f5f9; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 15px;">
                  <i class="fas fa-building" style="font-size: 24px; color: #64748b;"></i>
                </div>


                <div style="flex: 1; display: grid; grid-template-rows: 1fr 1fr; gap: 20px;">

                  <div class="card"
                    style="background: rgba(255, 255, 255, 0.98); border-radius: 18px; border-left: 5px solid #10b981; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); padding: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; overflow: hidden;">
                    <div
                      style="color: #15803d; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;">
                      Days Present</div>
                    <div style="display: flex; align-items: baseline; gap: 5px;">
                      <span id="myPresent" style="font-size: 32px; font-weight: 800; color: #16a34a;">0</span>
                      <span style="color: #15803d; font-weight: 600; font-size: 14px;">days</span>
                    </div>
                  </div>

                  <div class="card"
                    style="background: rgba(255, 255, 255, 0.98); border-radius: 18px; border-left: 5px solid #ef4444; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); padding: 20px; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; overflow: hidden;">
                    <div
                      style="color: #b91c1c; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 0.5px;">
                      Days Absent</div>
                    <div style="display: flex; align-items: baseline; gap: 5px;">
                      <span id="myAbsent" style="font-size: 32px; font-weight: 800; color: #dc2626;">0</span>
                      <span style="color: #b91c1c; font-weight: 600; font-size: 14px;">days</span>
                    </div>
                  </div>

                </div>

              </div>

            </div>

            <div id="noPersonalReportMsg"
              style="display: none; position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; color: #64748b; background: rgba(255,255,255,0.9); padding: 40px; border-radius: 18px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); width: 80%;">
              <i class="fas fa-folder-open" style="font-size: 40px; margin-bottom: 15px; opacity: 0.5;"></i>
              <h3 style="margin: 0 0 10px 0; color: #334155; font-weight: 600;">No Report Found</h3>
              <p style="margin: 0; font-size: 14px;">Please select a month and click "Fetch Statement"</p>
            </div>

          </div>
        </div>

      </div>


    </div>

    <script>
      const backendURL = "http://127.0.0.1:5000";

      function getAuthToken() {
        return localStorage.getItem("token");
      }

      function showLogin() {
        const loginIds = ["loginPage", "loginSection", "login_container"];
        const otherPages = ["registerPage", "dashboard", "passwordSetupPage"];

        let foundLogin = false;
        loginIds.forEach((id) => {
          const el = document.getElementById(id);
          if (el) {
            el.style.display = "flex";
            foundLogin = true;
          }
        });

        otherPages.forEach((id) => {
          const el = document.getElementById(id);
          if (el) el.style.display = "none";
        });

        if (!foundLogin) {
          console.error(
            "CRITICAL: Could not find any Login Div. Check if your HTML has id='loginPage'",
          );
        }
      }


      function checkAuth() {
        const token = localStorage.getItem("token");
        const role = localStorage.getItem("userRole");

        const regPage = document.getElementById("registerPage");
        const isRegistering = regPage && regPage.style.display === "flex";

        if (token && role) {
          
          showDashboard();

          if (role.toLowerCase() === 'admin') {
            updateAdminNotifications();
          }
          if (role !== 'admin') {
            loadStaffRequestHistory();
          }

        } else if (!isRegistering) {
          showLogin();
        }
      }
      
      function showRegister() {
        document.getElementById("loginPage").style.display = "none";
        document.getElementById("registerPage").style.display = "flex";
        document.getElementById("passwordSetupPage").style.display = "none";
        const regError = document.getElementById("regError");
        if (regError) regError.innerText = "";
        console.log("Navigation: Switched to Register Page");
      }
      function showPasswordSetup() {
        document.getElementById("loginPage").style.display = "none";
        document.getElementById("passwordSetupPage").style.display = "flex";
      }



      function cancelReScan() {
        document.getElementById("directUpdateArea").style.display = "none";

        document.getElementById("reScanFace").checked = false;

        const video = document.getElementById("updateVideo");
        if (video.srcObject) {
          const tracks = video.srcObject.getTracks();
          tracks.forEach(track => track.stop());
          video.srcObject = null;
        }

        console.log("Re-scan cancelled by user.");
      }


      async function loadDailyReport() {
        const dateInput = document.getElementById("reportDate");
        const selectedDate = dateInput ? dateInput.value : "";

        if (!selectedDate) {
          alert("Please select a date first!");
          return;
        }

        const dayBody = document.getElementById("dayReportsTableBody");
        const nightBody = document.getElementById("nightReportsTableBody");

        if (dayBody) dayBody.innerHTML = "<tr><td colspan='6'>Loading...</td></tr>";
        if (nightBody) nightBody.innerHTML = "<tr><td colspan='6'>Loading...</td></tr>";

        try {
          const userRole = (localStorage.getItem("userRole") || "").toLowerCase();
          const userId = localStorage.getItem("user_id");

          let response;
          let data;

          if (userRole === "staff" || userRole === "staff_member") {
            if (!userId) {
              alert("Staff ID not found in session. Please login again.");
              return;
            }
            response = await fetch(`http://127.0.0.1:5000/api/my_attendance_report/${userId}/${selectedDate}`);
            data = await response.json();

            const allMyRecords = Array.isArray(data) ? data : [];

            const dayShift = allMyRecords.filter(r => {
              const time = r.Check_In || r.clock_in || "";
              return getEthiopianShiftType(time) === "Day"; // Reuse your shift helper
            });
            const nightShift = allMyRecords.filter(r => {
              const time = r.Check_In || r.clock_in || "";
              return getEthiopianShiftType(time) !== "Day";
            });

            renderReportTable(dayBody, dayShift);
            renderReportTable(nightBody, nightShift);

          } else {
            // ADMIN / SUPERVISOR: See all records (existing behavior)
            response = await fetch(`http://127.0.0.1:5000/api/attendance_report/${selectedDate}`);
            data = await response.json();

            renderReportTable(dayBody, data.day_shift || []);
            renderReportTable(nightBody, data.night_shift || []);
          }

        } catch (err) {
          console.error("Report Load Error:", err);
          alert("Failed to load report.");
        }
      }

      function renderReportTable(body, records) {
        if (!body) return;
        body.innerHTML = "";

        if (records.length === 0) {
          body.innerHTML = `<tr><td colspan="6" style="text-align:center; color:#666; padding:20px;">No records found</td></tr>`;
          return;
        }

        records.forEach(r => {
          body.innerHTML += `
      <tr>
        <td>${r.id || r.ID || r.staff_id}</td>
        <td>${r.name || r.Name}</td>
        <td>${r.dept || r.Department || 'N/A'}</td>
        <td>${r.date || r.Date}</td>
        <td>${r.clock_in || r.Check_In || '--:--:--'}</td>
        <td>${r.clock_out || r.Check_Out || '-'}</td>
        <td><span style="color:green; font-weight:bold;">${r.status || r.Status || 'Present'}</span></td>
      </tr>`;
        });
      }

      function getEthiopianShiftType(timeStr) {
        try {
          const hour = parseInt(timeStr.split(":")[0]);
          const ethHour = (hour - 6 + 24) % 24;
          return (1 <= ethHour && ethHour <= 12) ? "Day" : "Night";
        } catch {
          return "Night";
        }
      }

      // Auto load report when date is changed safely
      document.addEventListener("DOMContentLoaded", () => {
        const reportDate = document.getElementById("reportDate");
        if (reportDate) {
          reportDate.addEventListener("change", loadDailyReport);

          // Set today's date by default
          const today = new Date().toISOString().split('T')[0];
          reportDate.value = today;

          // --- FIX: Check role before forcing an immediate load ---
          const rawRole = localStorage.getItem("role") || localStorage.getItem("userRole") || "";
          const userRole = rawRole.toLowerCase().trim();

          // Define who is allowed to run the daily admin report
          const isAdminOrSupervisor = ["system administrator", "admin", "shift supervisor", "supervisor"].includes(userRole);

          if (isAdminOrSupervisor) {
            // Only execute automatically if they are authorized to see this admin panel component
            loadDailyReport();
          } else {
            console.log("Skipping automatic daily report load for restricted role:", userRole);
          }
        }
      });


      async function loadDashboardData(role) {
        const normalizedRole = role ? role.toLowerCase() : "";
        // If they are just staff, they don't see these admin metrics
        if (normalizedRole === "staff") return;

        try {
          const response = await fetch(`${backendURL}/api/dashboard_metrics`, {
            headers: { Authorization: `Bearer ${getAuthToken()}` },
          });
          const data = await response.json();

          if (response.ok) {
            // Direct selection prevents the "ReferenceError"
            const staffEl = document.getElementById("totalStaffCount");
            const faceEl = document.getElementById("enrolledFacesCount");
            const presentEl = document.getElementById("presentTodayCount");

            if (staffEl) staffEl.innerText = data.total_staffs || 0;
            if (faceEl) faceEl.innerText = data.total_faces || 0;
            if (presentEl) presentEl.innerText = data.present_today || 0;
          }
        } catch (error) {
          console.error("Dashboard Load Error:", error);
        }

        // Set visibility for Admin-only elements
        if (
          normalizedRole === "admin" ||
          normalizedRole === "system administrator"
        ) {
          const manageBtn = document.getElementById("manageStaffBtn");
          if (manageBtn) manageBtn.style.display = "block";

          const adminCards = document.getElementById("adminTeacherCards");
          if (adminCards) adminCards.style.display = "grid";
        }
      }




      function showSection(sectionId) {
        const rawRole = localStorage.getItem("role") || localStorage.getItem("userRole") || "";
        const userRole = rawRole.toLowerCase().trim();

        const validFinanceRoles = ["finance", "hospital accountant", "accountant", "hospital_accountant"];
        const isAccountant = validFinanceRoles.includes(userRole);
        const isStaff = userRole === "staff" || userRole === "staff_member";

        const restrictedForAccountant = ["reportsSection", "registerStaff", "attendanceSession", "permissionReview", "staffManagement", "myFinancialSection"];
        
        if (isAccountant && restrictedForAccountant.includes(sectionId)) {
          console.warn(`Accountant access restricted for section layout: ${sectionId}`);
          showSection("financialDashboard");
          return;
        }

        const adminOnly = ["registerStaff", "attendanceSession", "permissionReview", "staffManagement", "financialDashboard"];
        if (isStaff && adminOnly.includes(sectionId)) {
          console.warn("Access Denied: Staff restricted from admin tools.");
          return;
        }

        document.querySelectorAll(".content-section").forEach((sec) => {
          sec.style.display = "none";
        });

        // Fallback selector hook for custom containers
        document.querySelectorAll(".section-container").forEach((sec) => {
          sec.style.display = "none";
        });

        // 5. SHOW target section element layout
        if (sectionId !== 'attendanceSession') {
          // Automatically kill camera feed when leaving the attendance page
          stopAttendance();
        }

        const target = document.getElementById(sectionId);
        if (target) {
          target.style.display = "block";
        } else {
          console.warn(`Section element container not found inside DOM: ${sectionId}`);
          return;
        }

        // 6. TRIGGER LOGICAL DATA LOADERS
        if (sectionId === "financialDashboard") {
          if (typeof loadPayroll === "function") loadPayroll();
        }
        if (sectionId === "reportsSection" && typeof setInitialDate === "function") setInitialDate();
        if (sectionId === "permissionReview" && typeof loadPermissionRequests === "function") loadPermissionRequests();
        if (sectionId === "requestPermission" && typeof loadStaffHistory === "function") loadStaffHistory();

        // --- INITIALIZE PERSONAL FINANCE UI FOR ACTIVE STAFF MEMBER ---
        if (sectionId === "myFinancialSection") {
          // Set user name immediately from local storage
          const myName = localStorage.getItem("user_name") || "Staff Member";
          const nameEl = document.getElementById("currentStaffProfileName");
          if (nameEl) nameEl.innerText = myName;

          // Reset results and show initial instruction prompt
          const cardContainer = document.getElementById("personalReportCard");
          const statsContainer = document.getElementById("staffStatsCards");
          const fallbackMsg = document.getElementById("noPersonalReportMsg");

          if (cardContainer) cardContainer.style.display = "none";
          if (statsContainer) statsContainer.style.display = "none";
          if (fallbackMsg) {
            fallbackMsg.style.display = "block";
            fallbackMsg.innerHTML = '<i class="fas fa-calendar-alt" style="font-size: 40px; margin-bottom: 15px; opacity: 0.5;"></i><h3 style="margin: 0 0 10px 0; color: #334155; font-weight: 600;">Financial Records Ready</h3><p style="margin: 0; font-size: 14px;">Select a month above and click "Generate" to view your processed statement.</p>';
          }
        }

      }



      async function enroll_staff(e) {
        if (e) {
          e.preventDefault();
          e.stopPropagation();
        }

        console.log("--- Executing Visual Form Validation ---");

        const msgEl = document.getElementById("enrollMessage");

        // 1. Reset everything to standard styles before validating
        if (msgEl) {
          msgEl.innerHTML = "";
          msgEl.style.display = "none";
        }

        // Define an array of elements to clear their previous error borders
        const inputIds = ["staffIdInput", "staffNameInput", "registerSex", "staffDeptInput", "regBaseSalary", "regOvertimeRate"];
        inputIds.forEach(id => {
          const el = document.getElementById(id);
          if (el) {
            // Revert back to your dashboard template's original slate borders
            el.style.borderColor = "#475569";
            el.style.backgroundColor = "#1e293b";
          }
        });

        // 2. Extract trimmed values
        const staffId = document.getElementById("staffIdInput").value.trim();
        const fullName = document.getElementById("staffNameInput").value.trim();
        const department = document.getElementById("staffDeptInput").value.trim();

        const sexEl = document.getElementById("registerSex");
        const sexValue = sexEl.selectedIndex > 0 ? sexEl.options[sexEl.selectedIndex].value : "";

        const baseSalaryRaw = document.getElementById("regBaseSalary").value.trim();
        const overtimeRateRaw = document.getElementById("regOvertimeRate").value.trim();
        const numCaptures = parseInt(document.getElementById("numCaptures").value) || 5;

        // Helper helper function to inject red feedback container cleanly
        function displayInlineError(errorMessage, targetInputId) {
          if (msgEl) {
            msgEl.style.display = "block";
            msgEl.innerHTML = `
        <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; color: #fca5a5; padding: 12px 16px; border-radius: 10px; display: flex; align-items: center; gap: 10px;">
          <i class="fas fa-exclamation-circle" style="color: #ef4444;"></i>
          <span><strong>Validation Error:</strong> ${errorMessage}</span>
        </div>
      `;
          }

          // Highlight the specific missing input box red
          const targetEl = document.getElementById(targetInputId);
          if (targetEl) {
            targetEl.style.borderColor = "#ef4444";
            targetEl.style.backgroundColor = "rgba(239, 68, 68, 0.05)";
            targetEl.focus();
          }
        }

        // 3. STRICT VISUAL CHECKS: Intercept blanks without annoying alerts
        if (!staffId) {
          displayInlineError("Staff ID field is blank. Please enter a valid ID row.", "staffIdInput");
          return false;
        }

        if (!fullName) {
          displayInlineError("Full Name is required for profile database matching.", "staffNameInput");
          return false;
        }

        if (!sexValue) {
          displayInlineError("Please select a valid Gender option from the selection row dropdown.", "registerSex");
          return false;
        }

        if (!department) {
          displayInlineError("Department field cannot be empty.", "staffDeptInput");
          return false;
        }

        if (!baseSalaryRaw) {
          displayInlineError("Monthly base salary configuration must be assigned.", "regBaseSalary");
          return false;
        }

        if (!overtimeRateRaw) {
          displayInlineError("Daily Overtime tracking rate must be assigned.", "regOvertimeRate");
          return false;
        }

        // 4. Assemble payload now that verification passed perfectly
        const payload = {
          staff_id: staffId,
          full_name: fullName,
          department: department,
          sex: sexValue,
          base_monthly_salary: parseFloat(baseSalaryRaw),
          overtime_rate: parseFloat(overtimeRateRaw),
          num_captures: numCaptures
        };

        // Show processing camera state banner inside the same box container
        if (msgEl) {
          msgEl.style.display = "block";
          msgEl.innerHTML = `
      <div style="background: rgba(234, 179, 8, 0.15); border: 1px solid #eab308; color: #fef08a; padding: 12px 16px; border-radius: 10px; display: flex; align-items: center; gap: 10px;">
        <i class="fas fa-spinner fa-spin" style="color: #eab308;"></i>
        <span>Form verified. Booting hardware camera stream workspace...</span>
      </div>
    `;
        }

        try {
          const response = await fetch('http://127.0.0.1:5000/api/enroll_staff', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
          });

          const result = await response.json();

          if (result.status === "success") {
            if (msgEl) {
              msgEl.innerHTML = `
          <div style="background: rgba(34, 197, 94, 0.15); border: 1px solid #22c55e; color: #bbf7d0; padding: 12px 16px; border-radius: 10px; display: flex; align-items: center; gap: 10px;">
            <i class="fas fa-check-circle" style="color: #22c55e;"></i>
            <span>Staff profile successfully registered into hospital roster!</span>
          </div>
        `;
            }

            // Clear values safely
            document.getElementById("staffIdInput").value = "";
            document.getElementById("staffNameInput").value = "";
            document.getElementById("staffDeptInput").value = "";
            document.getElementById("registerSex").selectedIndex = 0;
            document.getElementById("regBaseSalary").value = "";
            document.getElementById("regOvertimeRate").value = "";
          } else {
            if (msgEl) {
              msgEl.innerHTML = `
          <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; color: #fca5a5; padding: 12px 16px; border-radius: 10px; display: flex; align-items: center; gap: 10px;">
            <i class="fas fa-times-circle" style="color: #ef4444;"></i>
            <span>System Error: ${result.message}</span>
          </div>
        `;
            }
          }
        } catch (error) {
          console.error(error);
          if (msgEl) {
            msgEl.innerHTML = `
        <div style="background: rgba(239, 68, 68, 0.15); border: 1px solid #ef4444; color: #fca5a5; padding: 12px 16px; border-radius: 10px; display: flex; align-items: center; gap: 10px;">
          <i class="fas fa-wifi" style="color: #ef4444;"></i>
          <span>API error: Could not complete connection with backend server threads.</span>
        </div>
      `;
          }
        }
      }


      async function handleRequestAction(requestId, action) {
        let remarks = "";

        if (action === "approved") {
          // Accident Prevention: Ask the admin to confirm before approving
          const confirmApprove = confirm("Are you sure you want to APPROVE this permission request?");
          if (!confirmApprove) return; // If they click 'Cancel', stop here and do nothing
        }
        else if (action === "denied") {
          // Show the prompt for denial reasons
          remarks = prompt("Enter the reason why this request is being DENIED:");

          // If the admin clicks 'Cancel' on the prompt box, abort the operation
          if (remarks === null) return;

          // Optional: Ensure they actually typed a reason for denial
          if (remarks.trim() === "") {
            alert("You must provide a reason for denying this request.");
            return;
          }
        }

        try {
          const response = await fetch("http://127.0.0.1:5000/api/admin/process_request", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              id: parseInt(requestId),
              status: action,
              admin_remarks: remarks.trim()
            })
          });

          const result = await response.json();

          if (response.ok) {
            alert(`Request has been successfully ${action}!`);
            // Reload the table layout and update notification badge counts dynamically
            if (typeof loadPermissionRequests === "function") loadPermissionRequests();
            if (typeof checkPendingRequestsCount === "function") checkPendingRequestsCount();
          } else {
            alert(`Failed to update request state: ${result.error || "Unknown server error."}`);
          }
        } catch (error) {
          console.error("Error committing administrative update action:", error);
          alert("Failed to update request state due to a network connection loss.");
        }
      }

      // Keep the alias function intact to prevent breaking older button bindings
      function processRequestAction(id, action) {
        handleRequestAction(id, action);
      }


      async function logout() {
        console.log("Logging out and clearing all session data...");

        try {
          // 1. Clear ALL storage
          localStorage.clear();
          sessionStorage.clear();

          // 2. Clear Cookies
          document.cookie.split(";").forEach((c) => {
            document.cookie = c
              .replace(/^ +/, "")
              .replace(
                /=.*/,
                "=;expires=" + new Date().toUTCString() + ";path=/",
              );
          });

          // 3. Reset UI Safely (The "Safe" Way)
          const resetValue = (id) => {
            const el = document.getElementById(id);
            if (el) el.value = "";
          };
          const resetText = (id) => {
            const el = document.getElementById(id);
            if (el) el.innerText = "";
          };

          // Inputs
          [
            "loginId",
            "loginPassword",
            "regId",
            "regName",
            "regPassword",
            "staffIdInput",
            "staffNameInput",
          ].forEach(resetValue);

          // Messages
          ["error", "regError", "enrollMessage"].forEach(resetText);

          // 4. NAVIGATION (The critical part)
          const dash = document.getElementById("dashboard");
          const reg = document.getElementById("registerPage");
          const login = document.getElementById("loginPage");

          if (dash) dash.style.display = "none";
          if (reg) reg.style.display = "none";

          if (login) {
            login.style.display = "flex";
            console.log("Logout successful. Returned to Login Page.");
          } else {
            // BACKUP: If loginPage is missing from the DOM, just reload the app
            console.warn("loginPage not found, reloading window...");
            window.location.reload();
          }
        } catch (err) {
          console.error("Logout encountered an error, forcing reload:", err);
          window.location.reload();
        }

        document.title = "FaceAttend System";
        if (window.history && window.history.pushState) {
          // Points back to the root directory safely
          window.history.pushState({}, "Login", "/");
        }
      }


      // --- API Calls (User Management) ---

      async function registerUser() {
        // 1. Get values from the HTML
        const actualId = document.getElementById("regId").value.trim(); // Reads the new box
        const name = document.getElementById("regName").value.trim();
        const password = document.getElementById("regPassword").value.trim();
        const selectedRole = document.getElementById("regRole").value;
        const regError = document.getElementById("regError");

        // 2. Validation: Check if the ID is provided
        if (!actualId || !name || !password || !selectedRole) {
          regError.innerText = "All fields (including ID) are required!";
          return;
        }

        const roleMapping = {
          admin: "Admin", // "admin" (lowercase) from HTML -> "Admin" (Capital) for JSON
          shift_supervisor: "shift_supervisor",
          staff: "staff_member", // "staff" from HTML -> "staff_member" for JSON
        };

        const roleToSend = roleMapping[selectedRole];

        try {
          const response = await fetch(`${backendURL}/api/register_user`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              staff_id: actualId, // Sends 1234 to the backend
              name: name,
              password: password,
              role: roleToSend,
            }),
          });

          const result = await response.json();

          if (response.ok) {
            alert(result.message + "\nYou can now login.");
            showLogin();
            // Clear all fields
            document.getElementById("regId").value = "";
            document.getElementById("regName").value = "";
            document.getElementById("regPassword").value = "";
            document.getElementById("regRole").value = "";
          } else {
            regError.innerText = result.message;
          }
        } catch (err) {
          regError.innerText = "Backend server is not running!";
        }
      }

      async function login() {
        const idEl = document.getElementById("loginId");
        const passEl = document.getElementById("loginPassword");
        const errorEl = document.getElementById("error");

        if (!idEl || !passEl) return;

        const u_id = idEl.value.trim();
        const pass = passEl.value.trim();

        if (errorEl) errorEl.innerText = "";

        if (!u_id || !pass) {
          if (errorEl) errorEl.innerText = "Please enter both ID and Password";
          return;
        }

        try {
          const response = await fetch("http://127.0.0.1:5000/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: u_id, password: pass }),
          });

          const data = await response.json();

          if (response.ok) {
            if (data.is_first_login) {
              document.getElementById("loginPage").style.display = "none";
              const wrapper = document.getElementById("passwordWrapper");
              if (wrapper) wrapper.style.display = "flex";
              document.getElementById("passwordSection").style.display = "block";
              localStorage.setItem("temp_user_id", u_id);
            } else {
              // --- SAVE SESSION DATA ---
              localStorage.setItem("token", "active_session");
              localStorage.setItem("user_id", u_id);
              localStorage.setItem("userRole", data.role); // Important: 'admin' or 'staff'
              localStorage.setItem("user_name", data.user_name);

              showDashboard();

              // Immediately check for notifications if this user is an admin
              updateAdminNotifications();
            }
          } else {
            if (errorEl) errorEl.innerText = data.message;
          }
        } catch (err) {
          if (errorEl) errorEl.innerText = "Error: Could not connect to server.";
          console.error("Login Error:", err);
        }
      }


      async function handleLogin() {
        const id = document.getElementById("loginId").value;
        const password = document.getElementById("loginPassword").value;

        try {
          const response = await fetch("/api/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id, password }),
          });

          const data = await response.json();

          if (data.status === "success") {
            window.currentUserId = data.user.id; // Store ID for the next step

            if (data.user.is_first_login) {
              // 1. Hide the Login Page
              document.getElementById("loginPage").style.display = "none";

              // 2. Target the WRAPPER, not just the section
              const wrapper = document.getElementById("passwordWrapper");

              // 3. Force it to show using Flex (this fixes the white page)
              wrapper.style.setProperty("display", "flex", "important");

              console.log("Password wrapper enabled");
            } else {
              showDashboard(data.user);
            }
          } else {
            alert(data.message);
          }
        } catch (err) {
          console.error("Login Error:", err);
        }
      }

      async function finishSetup() {
        const newPassEl = document.getElementById("newPass");
        const confirmPassEl = document.getElementById("confirmPass");
        const errorEl = document.getElementById("passwordError");

        const newPass = newPassEl.value;
        const confirmPass = confirmPassEl.value;

        // Get the ID we stored during login
        const u_id = localStorage.getItem("temp_user_id");

        // Reset inputs and error banners to initial states before evaluating rules
        errorEl.style.display = "none";
        errorEl.innerHTML = "";
        newPassEl.style.borderColor = "#4b5563";
        confirmPassEl.style.borderColor = "#4b5563";

        // Helper utility function to handle rendering errors inline cleanly
        function triggerPassError(msg, highlightConfirm = false) {
          errorEl.style.display = "block";
          errorEl.innerHTML = `
      <div style="background-color: #fef2f2; border: 1px solid #ef4444; color: #991b1b; padding: 12px; border-radius: 10px; font-size: 13px; font-weight: 500; display: flex; align-items: center; gap: 8px;">
        <i class="fas fa-exclamation-triangle" style="color: #ef4444;"></i>
        <span>${msg}</span>
      </div>
    `;

          if (highlightConfirm) {
            confirmPassEl.style.borderColor = "#ef4444";
            confirmPassEl.focus();
          } else {
            newPassEl.style.borderColor = "#ef4444";
            newPassEl.focus();
          }
        }

        // 1. Check for blank submissions
        if (!newPass) {
          triggerPassError("Password field cannot be left blank.");
          return;
        }
        if (!confirmPass) {
          triggerPassError("Please fill out the Confirm Password confirmation box.", true);
          return;
        }

        // 2. Strict Cybersecurity RegEx Check: Minimum 8 chars, 1 letter, 1 digit, 1 special sign
        const strongPasswordRegex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&+-._~]).{8,}$/;
        if (!strongPasswordRegex.test(newPass)) {
          triggerPassError("Weak Password! Requirements: 8+ characters, including letters, digits, and a special sign.");
          return;
        }

        // 3. Confirm matching rule verification validation
        if (newPass !== confirmPass) {
          triggerPassError("Passwords do not match! Please verify your inputs.", true);
          return;
        }

        // 4. Secure validation payload transport execution via API endpoint
        try {
          const response = await fetch("http://127.0.0.1:5000/api/setup_password", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: u_id,
              new_password: newPass,
            }),
          });

          const result = await response.json();

          if (response.ok) {
            // Use a green notice when everything updates correctly
            errorEl.style.display = "block";
            errorEl.innerHTML = `
        <div style="background-color: #f0fdf4; border: 1px solid #22c55e; color: #166534; padding: 12px; border-radius: 10px; font-size: 13px; font-weight: 500; display: flex; align-items: center; gap: 8px;">
          <i class="fas fa-check-circle" style="color: #22c55e;"></i>
          <span>Password secured! Reloading environment system...</span>
        </div>
      `;

            setTimeout(() => {
              document.getElementById("passwordWrapper").style.display = "none";
              location.reload();
            }, 1500);

          } else {
            triggerPassError("System logic error: " + result.message);
          }
        } catch (err) {
          console.error("Setup Error:", err);
          triggerPassError("Failed to update password. Check if backend Flask server on port 5000 is active.");
        }
      }


      async function checkFirstLogin() {
        const sid = document.getElementById("staffID").value;
        const dp = document.getElementById("defaultPass").value;

        const response = await fetch("http://127.0.0.1:5000/api/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_id: sid, password: dp }),
        });

      }

      async function loadDashboardData(role) {
        const normalizedRole = role ? role.toLowerCase() : "";
        if (normalizedRole === "staff") return;

        try {
          const response = await fetch(`${backendURL}/api/dashboard_metrics`, {
            headers: { Authorization: `Bearer ${getAuthToken()}` },
          });
          const data = await response.json();

          if (response.ok) {
            // Update counts by selecting IDs directly
            const staff = document.getElementById("totalStaffCount");
            const faces = document.getElementById("enrolledFacesCount");
            const present = document.getElementById("presentTodayCount");

            if (staff) staff.innerText = data.total_staffs || 0;
            if (faces) faces.innerText = data.total_faces || 0;
            if (present) present.innerText = data.present_today || 0;
          }
        } catch (error) {
          console.error("Dashboard Load Error:", error);
        }

        // Fix UI Visibility without using 'elements'
        if (
          normalizedRole === "admin" ||
          normalizedRole === "system administrator"
        ) {
          const manageBtn = document.getElementById("manageStaffBtn");
          if (manageBtn) manageBtn.style.display = "block";

          const adminCards = document.getElementById("adminTeacherCards");
          if (adminCards) adminCards.style.display = "grid";
        }
        // IMPORTANT: Removed the line that called loadDashboardData() again!
      }


      async function loadStaffDashboardMetrics() {
        // 1. Get IDs from storage
        const staffId =
          localStorage.getItem("staff_id") || localStorage.getItem("user_id");
        const token = localStorage.getItem("access_token");

        if (!staffId) {
          console.error("Staff ID missing from storage");
          return;
        }

        try {
          const response = await fetch(
            `${backendURL}/api/staff_metrics/${staffId}`,
            {
              headers: { Authorization: `Bearer ${token}` },
            },
          );

          const data = await response.json();

          if (response.ok) {
            // Update the UI - match Backend Key to HTML ID
            // HTML ID: totalClassesAttended  <-- Backend Key: total_attended
            const attendedEl = document.getElementById("totalClassesAttended");
            if (attendedEl) attendedEl.innerText = data.total_attended ?? 0;

            // HTML ID: unexcusedAbsences <-- Backend Key: unexcused_absences
            const unexcusedEl = document.getElementById("unexcusedAbsences");
            if (unexcusedEl)
              unexcusedEl.innerText = data.unexcused_absences ?? 0;

            // HTML ID: approvedLeavesCount <-- Backend Key: approved_leaves
            const approvedEl = document.getElementById("approvedLeavesCount");
            if (approvedEl) approvedEl.innerText = data.approved_leaves ?? 0;
          }
        } catch (error) {
          console.error("Failed to load metrics:", error);
        }
      }

      // --- 1. Dashboard UI Stats Counters Engine ---
      async function updateDashboardCounters() {
        try {
          const response = await fetch("http://127.0.0.1:5000/api/admin_stats");
          const stats = await response.json();

          // Target the specific administrative metrics elements
          const staffEl = document.getElementById("totalStaffCount");
          const faceEl = document.getElementById("enrolledFacesCount");
          const presentEl = document.getElementById("presentTodayCount");

          if (staffEl) staffEl.innerText = stats.total_staff || 0;
          if (faceEl) faceEl.innerText = stats.enrolled_faces || 0;
          if (presentEl) presentEl.innerText = stats.present_today || 0;

          console.log("📊 Global Dashboard UI Counters Sync Complete:", stats);
        } catch (err) {
          console.error("❌ Failed to fetch administrative metrics:", err);
        }
      }

      // 1. Improved Startup with UI Feedback
      async function startAttendance() {
        const statusMsg = document.getElementById("cameraStatus");
        const videoFeed = document.getElementById("cameraFeed");

        if (statusMsg) statusMsg.innerText = "🔍 Checking schedule...";

        try {
          const response = await fetch("http://127.0.0.1:5000/api/check_shift_window");
          const data = await response.json();

          if (!data.success) {
            // Update the screen instead of using an alert box
            if (statusMsg) {
              statusMsg.innerText = "❌ Attendance window is currently closed!";
              statusMsg.style.color = "red";
            }
            return; // Camera will NOT open
          }

          // Proceed to open the camera
          videoFeed.style.display = "block";
          videoFeed.src = `http://127.0.0.1:5000/api/video_feed?t=${Date.now()}`;
          statusMsg.innerText = "✅ Camera Active";
          statusMsg.style.color = "green";

        } catch (err) {
          console.error(err);
          if (statusMsg) statusMsg.innerText = "❌ Server error, cannot check time.";
        }
      }

      // 2. The Auto-Killer (Silent)
      setInterval(async () => {
        const videoFeed = document.getElementById("cameraFeed");
        const statusMsg = document.getElementById("cameraStatus");

        // Only check if camera is active
        if (videoFeed && videoFeed.style.display !== "none") {
          try {
            const response = await fetch("http://127.0.0.1:5000/api/check_shift_window");
            const data = await response.json();

            if (!data.success) {
              console.warn("Shift ended, closing stream...");
              stopAttendance(); // Your cleanup function
              if (statusMsg) {
                statusMsg.innerText = "🛑 Shift ended. Camera disabled.";
                statusMsg.style.color = "orange";
              }
            }
          } catch (e) {
            console.error("Monitor error:", e);
          }
        }
      }, 10000);


      function isCurrentTimeInWindow() {
        const now = new Date();
        const hour = now.getHours();
        const minute = now.getMinutes();

        // === YOUR ATTENDANCE WINDOWS ===
        // Change according to your hospital schedule
        return (
          (hour === 8) ||
          false
        );
      }

      async function stopAttendance() {
        const videoFeedImg = document.getElementById("cameraFeed");
        const statusMsg = document.getElementById("cameraStatus");

        if (videoFeedImg) {
          videoFeedImg.src = "";
          videoFeedImg.style.display = "none";
        }
        if (statusMsg) statusMsg.innerText = "Feed Stopped";

        try {
          await fetch("http://127.0.0.1:5000/api/stop_attendance", { method: "POST" });
        } catch (e) { }
      }

      function setupAutoClose() {
        console.log("⏰ Full Window Auto-Close Monitor Started");

        const checkInterval = setInterval(() => {
          const now = new Date();
          const currentHour = now.getHours();
          const currentMinute = now.getMinutes();

          const isInWindow =
            (currentHour === 8) ||
            false;  // fallback

          if (!isInWindow) {
            console.log("⏰ Window closed by time. Stopping attendance.");
            stopAttendanceSession("Attendance window has ended.");
            clearInterval(checkInterval);
          }

        }, 15000); // Check every 15 seconds (more responsive but not too heavy)
      }

      function stopAttendanceSession(reason) {
        const cameraFeed = document.getElementById("cameraFeed");
        const cameraStatus = document.getElementById("cameraStatus");

        if (cameraFeed) {
          cameraFeed.src = "";
          cameraFeed.style.display = "none";
        }
        if (cameraStatus) {
          cameraStatus.innerText = "❌ Window Closed";
          cameraStatus.style.color = "red";
        }

        // Disable start button
        const startBtn = document.getElementById("startAttendanceBtn");
        if (startBtn) {
          startBtn.disabled = true;
          startBtn.style.opacity = "0.5";
          startBtn.innerText = "Window Closed";
        }

        console.log("🚫 Session closed:", reason);
      }


      // --- 3. Reporting Sync Initializer ---
      function setInitialDate() {
        const dateInput = document.getElementById("reportDate");
        if (!dateInput) return;

        const today = new Date().toISOString().split("T")[0];
        dateInput.value = today;

        if (typeof loadReports === "function") {
          loadReports();
        } else {
          console.warn("⏳ Latency Warning: loadReports execution block hasn't been parsed by the engine yet.");
        }
      }

      // Global tracking array to cache data for the finance bridge transmission
      let currentGeneratedReport = [];

      async function loadMonthlySummary() {
        const month = document.getElementById("summaryMonth").value;
        const tableBody = document.getElementById("summaryTableBody");
        const sendBtn = document.getElementById("btnSendFinance");

        // If the field placeholder text "yyyy-MM" hasn't been changed yet, do not query
        if (!month || month === "yyyy-MM") return;

        tableBody.innerHTML = '<tr><td colspan="6" class="text-center" style="color: black; padding: 20px;">Generating clean records...</td></tr>';

        if (sendBtn) sendBtn.style.display = "none"; // Hide send button initially
        currentGeneratedReport = []; // Reset array cache data

        // Aggressive .trim() and fallback handles to eliminate case spelling issues
        const rawRole = localStorage.getItem("role") || localStorage.getItem("userRole") || "";
        const userRole = rawRole.toLowerCase().trim();

        const rawUserId = localStorage.getItem("user_id") || "";
        const userId = rawUserId.toString().trim();

        // 🔄 Target your active monthly summary route endpoint path
        let url = `${backendURL}/api/monthly_summary/${month}`;

        try {
          const response = await fetch(url);
          if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

          let data = await response.json();

          // Dynamic role matching handle (catches 'staff', 'Staff', 'staff_member')
          if (userRole === "staff" || userRole === "staff_member") {
            if (userId !== "") {
              data = data.filter((item) => {
                const itemStaffId = (item.staff_id || item.ID || "").toString().trim();
                return itemStaffId === userId;
              });
            } else {
              data = []; // Fallback sandbox wipe if user session ID is corrupt
            }
          }

          tableBody.innerHTML = "";

          if (!data || data.length === 0) {
            tableBody.innerHTML = `
        <tr>
          <td colspan="6" class="text-center" style="color: black; padding: 20px; font-style: italic;">
              No attendance logs found for this period.
          </td>
        </tr>`;
            return;
          }

          data.forEach((item) => {
            let performance = "Standard";

            // Map properties based on whatever variation your backend JSON keys use
            const presentDays = parseInt(item.total_present || item.days_present || 0);
            const absentDays = parseInt(item.absent_days || item.absences || 0);
            const approvedLeaves = parseInt(item.approved_leaves || item.leaves || 0);

            if (presentDays >= 25) performance = "⭐ Excellent";
            else if (absentDays > 5) performance = "⚠️ Low Attendance";

            // 🔄 CACHE DATA: Only capture it if the logged-in user is an Admin
            if (userRole === "admin" || userRole === "administrator") {
              currentGeneratedReport.push({
                staff_id: (item.staff_id || "").toString(),
                name: item.name || "Unknown Staff",
                present_days: presentDays,
                absent_days: absentDays
              });
            }

            const row = `
        <tr style="border-bottom: 1px solid #334155; color: black;">
            <td style="padding: 12px; font-weight: bold; color: black;">#${item.staff_id || "N/A"}</td>
            <td style="padding: 12px; font-weight: 500; color: black;">${item.name || "Unknown"}</td>
            <td style="padding: 12px; color: green; font-weight: bold;">${presentDays} Days</td>
            <td style="padding: 12px; color: blue;">${approvedLeaves} Leaves</td>
            <td style="padding: 12px; color: red; font-weight: bold;">${absentDays}</td>
            <td style="padding: 12px; color: black;"><span>${performance}</span></td>
        </tr>
      `;
            tableBody.insertAdjacentHTML("beforeend", row);
          });

          // 🔄 SHOW BUTTON: Reveal the "Send to Finance" button if user is Admin and records exist
          if ((userRole === "admin" || userRole === "administrator") && sendBtn && currentGeneratedReport.length > 0) {
            sendBtn.style.display = "inline-block";
          }

        } catch (error) {
          console.error("Monthly Summary Error:", error);
          tableBody.innerHTML = `
      <tr>
          <td colspan="6" class="text-center" style="color: red; padding: 20px; font-weight: bold;">
              Error loading logs: Failed to communicate with database server.
          </td>
      </tr>`;
        }
      }

      async function sendCompiledReportToFinance() {
        const targetMonth = document.getElementById("summaryMonth").value;
        const sendBtn = document.getElementById("btnSendFinance");

        if (!targetMonth || targetMonth === "yyyy-MM") {
          alert("Please select a valid report month first.");
          return;
        }

        if (!currentGeneratedReport || currentGeneratedReport.length === 0) {
          alert("No active reporting data found to transmit.");
          return;
        }

        // 1. CRITICAL: Force a fresh load of the staff registry to get latest salaries
        await loadStaffRegistry();

        if (sendBtn) {
          sendBtn.disabled = true;
          sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Transmitting...';
        }

        // 2. ENRICH DATA: Map actual salaries from the database to the transient report records
        const enrichedRecords = currentGeneratedReport.map(record => {
          // Find staff by ID in the userList (which is Object.values(users))
          const staffInfo = userList.find(u => String(u.id).trim() === String(record.staff_id).trim());

          const base = staffInfo ? (parseFloat(staffInfo.base_monthly_salary) || 0) : 0;
          // Aligned with core_logic.py: 30 standard working days
          const workingDaysInMonth = 30;
          const dailyRate = base / workingDaysInMonth;
          const calculatedDeduction = record.absent_days * dailyRate;
          const calculatedFinalSalary = base - calculatedDeduction;

          return {
            ...record,
            base_monthly_salary: base,
            deduction: Math.max(0, calculatedDeduction).toFixed(2),
            final_salary: Math.max(0, calculatedFinalSalary).toFixed(2)
          };
        });

        const payload = {
          month: targetMonth,
          generated_at: new Date().toISOString(),
          records: enrichedRecords
        };

        try {
          const response = await fetch(`${backendURL}/api/admin/send_to_finance`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });

          if (response.ok) {
            alert(`🎉 Success! Report for ${targetMonth} transmitted.`);
            if (sendBtn) sendBtn.style.display = "none";
          } else {
            const errorData = await response.json();
            alert(`❌ Failed: ${errorData.message}`);
          }
        } catch (err) {
          alert("⚠️ Network Failure: Unable to connect to server.");
        } finally {
          if (sendBtn) {
            sendBtn.disabled = false;
            sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i> Send to Finance';
          }
        }
      }

      
      let userList = []; // Ensure this is at the top of your JS file

      async function loadStaffRegistry() {
        try {
          const response = await fetch(`${backendURL}/api/get_staff_list`);
          const data = await response.json();

          userList = Array.isArray(data) ? data : Object.values(data);

          console.log("Registry successfully loaded as Array:", userList);
        } catch (err) {
          console.error("Failed to load staff list:", err);
        }
      }


      function showDashboard() {
        const loginPage = document.getElementById("loginPage");
        const dashboard = document.getElementById("dashboard");
        const passwordSection = document.getElementById("passwordSection");

        if (loginPage) loginPage.style.display = "none";
        if (passwordSection) passwordSection.style.display = "none";
        if (dashboard) dashboard.style.display = "flex";

        const rawRole = localStorage.getItem("role") || localStorage.getItem("userRole") || "";
        const userRole = rawRole.toLowerCase().trim();
        const userName = localStorage.getItem("user_name") || "User";

        const nameDisplay = document.getElementById("userNameDisplay");
        if (nameDisplay) nameDisplay.innerText = userName;

        if (window.history && window.history.pushState) {
          window.history.pushState({}, "FaceAttend", "/#FaceAttend");
        }
        document.title = "FaceAttend System";

        const isAdmin = userRole === "admin" || userRole === "system administrator";
        const isSupervisor = userRole === "shift_supervisor" || userRole === "shift supervisor";
        const isFinance = userRole === "finance" || userRole === "hospital accountant" || userRole === "accountant";
        const isStaff = userRole === "staff" || userRole === "staff_member";

        const toggleBtn = (id, show) => {
          const el = document.getElementById(id);
          if (el) el.style.display = show ? "flex" : "none";
        };

        toggleBtn("registerStaffBtn", isAdmin);
        toggleBtn("manageStaffBtn", isAdmin);
        toggleBtn("permissionReviewBtn", isAdmin);
        toggleBtn("attendanceBtn", isAdmin || isSupervisor);
        toggleBtn("requestPermissionBtn", isStaff);
        toggleBtn("myFinancialBtn", isStaff);

        // Sidebar link permissions matrix
        toggleBtn("financialBtn", isFinance);
        toggleBtn("dashBtn", isAdmin || isSupervisor || isStaff || isFinance);
        toggleBtn("reportsBtn", !isFinance && (isAdmin || isSupervisor || isStaff));

        if (isStaff) {
          if (document.getElementById("adminTeacherCards"))
            document.getElementById("adminTeacherCards").style.display = "none";
          if (document.getElementById("staffDashboardInfo"))
            document.getElementById("staffDashboardInfo").style.display = "block";
          if (typeof loadStaffDashboardMetrics === "function") loadStaffDashboardMetrics();

        } else if (isFinance) {
          // Show cards grid layout section wrapper container for Accountant
          if (document.getElementById("adminTeacherCards"))
            document.getElementById("adminTeacherCards").style.display = "grid";
          if (document.getElementById("staffDashboardInfo"))
            document.getElementById("staffDashboardInfo").style.display = "none";

          // 🌟 CRITICAL FIX: Force Financial labels immediately for Accountant role
          // This ensures titles change to "Total Payroll" even before data is loaded.
          updateDashboardLabels(true);

          // Run dynamic live data loader instantly
          if (typeof loadPayroll === "function") {
            loadPayroll();
          }

        } else {
          if (document.getElementById("adminTeacherCards"))
            document.getElementById("adminTeacherCards").style.display = "grid";
          if (document.getElementById("staffDashboardInfo"))
            document.getElementById("staffDashboardInfo").style.display = "none";

          // Revert structural layout labels back to standard Admin tracking text
          updateDashboardLabels(false);
          if (typeof refreshAdminDashboard === "function") refreshAdminDashboard();
        }

        if (typeof currentSection !== "undefined" && currentSection && currentSection !== "loginPage") {
          showSection(currentSection);
        } else {
          showSection("dashboardContent");
        }
      }


      
      function updateDashboardLabels(isAccountantView, values = { payroll: 0, paid: 0, deductions: 0 }) {
        const container = document.getElementById("adminTeacherCards");
        if (!container) return;

        // Locate current data element references across your dynamic system layout variations
        const el1 = document.getElementById("statCardValue1") || document.getElementById("totalRegisteredStaffs") || document.getElementById("totalStaffCount");
        const el2 = document.getElementById("statCardValue2") || document.getElementById("enrolledFaceRecords") || document.getElementById("enrolledFacesCount");
        const el3 = document.getElementById("statCardValue3") || document.getElementById("presentToday") || document.getElementById("presentTodayCount");

        // Premium Sub-Component Formatter Engine
        const formatCard = (valueEl, titleText, valueText, iconClass, iconColor, badgeBg, borderAccent) => {
          if (!valueEl) return;

          // 1. Text Properties Mutation
          valueEl.innerText = valueText;
          valueEl.style.fontWeight = "600";
          valueEl.style.fontSize = "1.85rem";
          valueEl.style.color = "#0f172a";
          valueEl.style.letterSpacing = "-0.5px";

          const parentCard = valueEl.closest('.stat-card') || valueEl.parentElement;
          const titleEl = valueEl.previousElementSibling;

          if (titleEl) {
            titleEl.innerText = titleText;
            titleEl.style.color = "#64748b";
            titleEl.style.fontSize = "0.82rem";
            titleEl.style.textTransform = "uppercase";
            titleEl.style.letterSpacing = "0.8px";
            titleEl.style.fontWeight = "600";
            titleEl.style.marginBottom = "6px";
          }

          // 2. Structural Layout Cards Styling (Fulfilling Higher Thesis Presentation Standouts)
          if (parentCard) {
            parentCard.style.background = "#ffffff";
            parentCard.style.borderRadius = "18px";
            parentCard.style.padding = "24px";
            parentCard.style.border = `1px solid ${borderAccent}`;
            parentCard.style.boxShadow = "0 10px 25px -5px rgba(148, 163, 184, 0.06)";
            parentCard.style.display = "flex";
            parentCard.style.justifyContent = "space-between";
            parentCard.style.alignItems = "center";
            parentCard.style.transition = "transform 0.2s ease, box-shadow 0.2s ease";

            // Dynamically manage/inject contextual icons cleanly
            let iconWrapper = parentCard.querySelector('.card-icon-wrapper');
            if (!iconWrapper) {
              iconWrapper = document.createElement('div');
              iconWrapper.className = 'card-icon-wrapper';
              parentCard.appendChild(iconWrapper);
            }

            iconWrapper.style.background = badgeBg;
            iconWrapper.style.color = iconColor;
            iconWrapper.style.width = "50px";
            iconWrapper.style.height = "50px";
            iconWrapper.style.borderRadius = "14px";
            iconWrapper.style.display = "flex";
            iconWrapper.style.alignItems = "center";
            iconWrapper.style.justifyContent = "center";
            iconWrapper.style.fontSize = "1.3rem";
            iconWrapper.style.boxShadow = "inset 0 -2px 4px rgba(0,0,0,0.02)";
            iconWrapper.innerHTML = `<i class="${iconClass}"></i>`;
          }
        };

        if (isAccountantView) {
          formatCard(el1, "Total Payroll", `${values.payroll.toFixed(2)} ETB`, "fas fa-wallet", "#0d9488", "#e6fbf7", "#e2e8f0");
          formatCard(el2, "Total Staff Paid", values.paid, "fas fa-user-check", "#16a34a", "#f0fdf4", "#e2e8f0");
          formatCard(el3, "Total Deductions", `${values.deductions.toFixed(2)} ETB`, "fas fa-percentage", "#dc2626", "#fef2f2", "#e2e8f0");

        } else {
          // MODE B: ADMIN MODE
          formatCard(el1, "Total Registered Staffs", el1 ? el1.innerText.replace(" ETB", "") : "0", "fas fa-users", "#0284c7", "#f0f9ff", "#e2e8f0");
          formatCard(el2, "Enrolled Face Records", el2 ? el2.innerText : "0", "fas fa-id-card-alt", "#2563eb", "#eff6ff", "#e2e8f0");
          formatCard(el3, "Present Today", el3 ? el3.innerText.replace(" ETB", "") : "0", "fas fa-calendar-check", "#7c3aed", "#f5f3ff", "#e2e8f0");
        }
      }



      async function loadStaffPersonalPayroll() {
        const monthInput = document.getElementById("staffMonthInput");

        // Compute automatic running current month fallback strings if empty
        if (monthInput && !monthInput.value) {
          const now = new Date();
          const year = now.getFullYear();
          const month = String(now.getMonth() + 1).padStart(2, '0');
          monthInput.value = `${year}-${month}`;
        }

        const targetMonth = monthInput ? monthInput.value : new Date().toISOString().slice(0, 7);
        const loggedInStaffId = localStorage.getItem("user_id") || "";

        const cardContainer = document.getElementById("personalReportCard");
        const fallbackMsg = document.getElementById("noPersonalReportMsg");
        const statsContainer = document.getElementById("staffStatsCards");

        if (!loggedInStaffId) {
          if (fallbackMsg) fallbackMsg.innerText = "Error: Active Staff Session ID not tracked. Please re-login.";
          return;
        }

        try {
          if (fallbackMsg) fallbackMsg.style.display = "none";

          // Query pipeline hitting the published payroll table summary logs
          const response = await fetch(`${backendURL}/api/finance/get-report/${targetMonth}`);

          if (!response.ok) {
            if (cardContainer) cardContainer.style.display = "none";
            if (statsContainer) statsContainer.style.display = "none";
            if (fallbackMsg) {
              fallbackMsg.style.display = "block";
              fallbackMsg.innerText = `No processed financial statement reports found for ${targetMonth}`;
            }
            return;
          }

          const data = await response.json();

          // Isolate lines belonging exclusively to the currently active logged-in employee ID
          const myRecord = data.records.find(row => String(row.staff_id).toLowerCase().trim() === loggedInStaffId.toLowerCase().trim());

          if (!myRecord) {
            if (cardContainer) cardContainer.style.display = "none";
            if (statsContainer) statsContainer.style.display = "none";
            if (fallbackMsg) {
              fallbackMsg.style.display = "block";
              fallbackMsg.innerText = `No personalized details matching your Staff ID (${loggedInStaffId}) in the ${targetMonth} report.`;
            }
            return;
          }

          // Render fields out directly inside the DOM interfaces properties mapping elements
          if (fallbackMsg) fallbackMsg.style.display = "none";
          if (cardContainer) cardContainer.style.display = "block";
          if (statsContainer) statsContainer.style.display = "flex";

          const titleText = document.getElementById("myReportTitle");
          const deptText = document.getElementById("myDept");
          const presentText = document.getElementById("myPresent");
          const absentText = document.getElementById("myAbsent");
          const baseText = document.getElementById("myBaseSalary");
          const dedText = document.getElementById("myDeductions");
          const finalText = document.getElementById("myFinalSalary");

          if (titleText) titleText.innerText = `Statement for ${myRecord.name} (${targetMonth})`;
          if (deptText) deptText.innerText = myRecord.department || 'N/A';
          if (presentText) presentText.innerText = myRecord.present_days;
          if (absentText) absentText.innerText = myRecord.absent_days;

          const base = parseFloat(myRecord.base_monthly_salary) || 0;
          const ded = parseFloat(myRecord.deduction) || 0;
          const final = parseFloat(myRecord.final_salary) || 0;

          if (baseText) baseText.innerText = `${base.toFixed(2)} ETB`;
          if (dedText) dedText.innerText = `${ded.toFixed(2)} ETB`;
          if (finalText) finalText.innerText = `${final.toFixed(2)} ETB`;

        } catch (err) {
          console.error("Personal Finance Pipeline Failure Error:", err);
          if (cardContainer) cardContainer.style.display = "none";
          if (statsContainer) statsContainer.style.display = "none";
          if (fallbackMsg) {
            fallbackMsg.style.display = "block";
            fallbackMsg.innerText = "Error establishing database pipeline verification.";
          }
        }
      }



      async function loadPayroll() {
        const monthInput = document.getElementById("financialMonth");

        if (!monthInput.value) {
          const now = new Date();
          const year = now.getFullYear();
          const month = String(now.getMonth() + 1).padStart(2, '0');
          monthInput.value = `${year}-${month}`;
        }

        const targetMonth = monthInput.value;
        const tableBody = document.getElementById("payrollTableBody");

        try {
          const response = await fetch(`${backendURL}/api/finance/get-report/${targetMonth}`);

          if (!response.ok) {
            tableBody.innerHTML = `
        <tr>
          <td colspan="8" style="padding: 50px; text-align: center; color: #94a3b8; background: #ffffff;">
            <div style="display: flex; flex-direction: column; align-items: center; gap: 12px; justify-content: center;">
              <i class="far fa-folder-open" style="font-size: 2.2rem; color: #cbd5e1;"></i>
              <span style="font-size: 0.95rem; font-weight: 500; color: #64748b;">No payroll data report records found for ${targetMonth}</span>
            </div>
          </td>
        </tr>`;
            return;
          }

          const data = await response.json();

          let totalPayroll = 0;
          let totalDeductions = 0;
          let totalStaff = data.records.length;

          const tableHTML = data.records.map(row => {
            const base = parseFloat(row.base_monthly_salary) || 0;
            const deduction = parseFloat(row.deduction) || 0;
            const final = parseFloat(row.final_salary) || 0;

            totalPayroll += final;
            totalDeductions += deduction;

            // Automatically reads the backend-processed dynamic value
            const departmentDisplay = row.department || "Medical Staff";

            return `
        <tr style="border-bottom: 1px solid #f1f5f9; transition: background 0.2s ease;" onmouseover="this.style.background='#f8fafc'" onmouseout="this.style.background='transparent'">
          <td style="padding: 16px; color: #0f172a; font-weight: 600;">${row.staff_id}</td>
          <td style="padding: 16px; color: #334155; font-weight: 500;">${row.name}</td>
          <td style="padding: 16px; color: #64748b;">
            <span style="background: #e0f2fe; color: #0369a1; padding: 6px 12px; border-radius: 8px; font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; display: inline-block;">
              <i class="fas fa-hospital-user" style="font-size: 0.75rem; margin-right: 4px; color: #0284c7;"></i> ${departmentDisplay}
            </span>
          </td>
          <td style="padding: 16px; color: #16a34a; font-weight: 600; text-align: center;">${row.present_days} d</td>
          <td style="padding: 16px; color: #dc2626; font-weight: 600; text-align: center;">${row.absent_days} d</td>
          <td style="padding: 16px; color: #475569; font-weight: 500;">${base.toFixed(2)} Birr</td>
          <td style="padding: 16px; color: #dc2626; font-weight: 500;">-${deduction.toFixed(2)} Birr</td>
          <td style="padding: 16px; color: #0d9488; font-weight: 700; background: rgba(13, 148, 136, 0.01); font-size: 0.95rem;">
            ${final.toFixed(2)} Birr
          </td>
        </tr>`;
          }).join('');

          if (tableBody) tableBody.innerHTML = tableHTML;

          // Sync metrics to top status cards
          const rawRole = localStorage.getItem("role") || localStorage.getItem("userRole") || "";
          if (rawRole.toLowerCase().trim().includes("accountant") || rawRole.toLowerCase().trim() === "finance") {
            updateDashboardLabels(true, {
              payroll: totalPayroll,
              paid: totalStaff,
              deductions: totalDeductions
            });
          }

        } catch (err) {
          console.error("Finance Load Error:", err);
        }
      }



      function downloadFinancialReport() {
        const targetMonth = document.getElementById("financialMonth").value;
        const tbody = document.getElementById("payrollTableBody");

        if (!targetMonth || tbody.rows.length <= 1 || tbody.rows[0].cells.length === 1) {
          alert("Please calculate a valid monthly payroll layout list before exporting.");
          return;
        }

        let csvContent = "data:text/csv;charset=utf-8,";
        csvContent += "Staff ID,Name,Department,Present Days,Absent Days,Base Salary (ETB),Deductions (ETB),Final Net Salary (ETB)\n";

        // Scan row values to build the output matrix cleanly
        const rows = tbody.querySelectorAll("tr");
        rows.forEach(row => {
          const cols = row.querySelectorAll("td");
          if (cols.length === 8) {
            const id = cols[0].innerText.replace("#", "").trim();
            const name = cols[1].innerText.trim();
            const dept = cols[2].innerText.trim(); // Handles the clean textual content within our pill component
            const pres = cols[3].innerText.split(" ")[0].trim();
            const abs = cols[4].innerText.trim();
            const base = cols[5].innerText.split(" ")[0].replace(/,/g, "").trim();
            const ded = cols[6].innerText.replace("-", "").split(" ")[0].replace(/,/g, "").trim();
            const final = cols[7].innerText.split(" ")[0].replace(/,/g, "").trim();

            csvContent += `"${id}","${name}","${dept}",${pres},${abs},${base},${ded},${final}\n`;
          }
        });

        // Create temporary hidden anchor downlinks to execute extraction safely
        const encodedUri = encodeURI(csvContent);
        const link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", `Hospital_Payroll_Report_${targetMonth}.csv`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      }

      function switchReportTab(tabName) {
        // Hide all sections first
        document.getElementById("tabDailyContent").style.display = "none";
        document.getElementById("tabMonthlyContent").style.display = "none";
        document.getElementById("tabYearlyContent").style.display = "none";

        // Reset inactive secondary styles across the group container elements with beautiful smooth bright mode classes
        document.getElementById("tabBtnDaily").className = "btn btn-secondary";
        document.getElementById("tabBtnMonthly").className = "btn btn-secondary";
        document.getElementById("tabBtnYearly").className = "btn btn-secondary";

        // Activate chosen content block view layouts dynamically
        if (tabName === "daily") {
          document.getElementById("tabDailyContent").style.display = "block";
          document.getElementById("tabBtnDaily").className = "btn btn-primary";
        } else if (tabName === "monthly") {
          document.getElementById("tabMonthlyContent").style.display = "block";
          document.getElementById("tabBtnMonthly").className = "btn btn-primary";
        } else if (tabName === "yearly") {
          document.getElementById("tabYearlyContent").style.display = "block";
          document.getElementById("tabBtnYearly").className = "btn btn-primary";

          // TRIGGER AUTOMATION: Runs calculation tracking engine instantly on click!
          if (typeof loadYearlySummary === "function") {
            loadYearlySummary();
          }
        }
      }




      async function loadYearlySummary() {
        const selectedYear = document.getElementById("summaryYear").value;
        const tableBody = document.getElementById("yearlyTableBody");

        if (!selectedYear) return;

        tableBody.innerHTML = '<tr><td colspan="5" class="text-center" style="color: black; padding: 20px;">Compiling leave records...</td></tr>';

        try {
          const userRole = (localStorage.getItem("userRole") || "").toLowerCase().trim();
          const userId = localStorage.getItem("user_id");

          let allRequests = [];

          // Fetch all leave requests
          const response = await fetch("http://127.0.0.1:5000/api/admin/all_requests");
          if (response.ok) {
            allRequests = await response.json();
          }

          // Filter by role
          let filteredRequests = allRequests;

          if (userRole === "staff" || userRole === "staff_member") {
            if (!userId) {
              tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center; color:red;">Staff ID not found. Please re-login.</td></tr>`;
              return;
            }
            // Staff only sees their own records
            filteredRequests = allRequests.filter(req =>
              String(req.staff_id || req.id) === String(userId)
            );
          }
          // Admins see everything (current behavior)

          // Build ledger
          const staffLedger = {};

          filteredRequests.forEach(req => {
            const statusClean = String(req.status || "").toLowerCase().trim();

            if (statusClean === "approved" && req.start_date && req.start_date.startsWith(selectedYear)) {
              // Skip emergency leaves for yearly balance calculation
              if (req.leave_type === "emergency_leave" || (req.reason && req.reason.includes("[EMERGENCY]"))) {
                return;
              }

              const sID = String(req.staff_id || req.id || "Unknown");

              if (!staffLedger[sID]) {
                staffLedger[sID] = {
                  id: sID,
                  name: req.name || "Unknown Staff",
                  daysTaken: 0
                };
              }

              staffLedger[sID].daysTaken += parseInt(req.duration || 1);
            }
          });

          const staffProfilesList = Object.values(staffLedger);

          if (staffProfilesList.length === 0) {
            tableBody.innerHTML = `<tr><td colspan="5" class="text-center" style="color: #64748b; padding: 20px;">No approved yearly leave records found for ${selectedYear}.</td></tr>`;
            return;
          }

          tableBody.innerHTML = "";

          staffProfilesList.forEach(staff => {
            const baseline = 30;
            let remaining = baseline - staff.daysTaken;
            if (remaining < 0) remaining = 0;

            let badge = `<span style="background: rgba(46, 204, 113, 0.2); color: #2ecc71; padding: 4px 8px; border-radius: 4px; font-weight: bold;">HEALTHY BALANCE</span>`;
            if (remaining <= 5) {
              badge = `<span style="background: rgba(231, 76, 60, 0.2); color: #e74c3c; padding: 4px 8px; border-radius: 4px; font-weight: bold;">CRITICAL LOW</span>`;
            } else if (remaining <= 15) {
              badge = `<span style="background: rgba(230, 126, 34, 0.2); color: #e67e22; padding: 4px 8px; border-radius: 4px; font-weight: bold;">MODERATE USE</span>`;
            }

            tableBody.innerHTML += `
        <tr style="border-bottom: 1px solid #334155; color: black;">
          <td style="padding: 12px; font-weight: bold; color: black;">#${staff.id}</td>
          <td style="padding: 12px; font-weight: 500; color: black;">${staff.name}</td>
          <td style="padding: 12px; font-weight: bold; color: black">${staff.daysTaken} Days Taken</td>
          <td style="padding: 12px; font-weight: 900; color: black; font-size: 15px;">${remaining} Days Remaining</td>
          <td style="padding: 12px; color: black;">${badge}</td>
        </tr>`;
          });

        } catch (error) {
          console.error("Yearly Report Error:", error);
          tableBody.innerHTML = `<tr><td colspan="5" class="text-center" style="color: red; padding: 20px;">Failed to load yearly report.</td></tr>`;
        }
      }


      const accountingBackendURL = typeof backendURL !== 'undefined' ? backendURL : "http://127.0.0.1:5000";

      function switchInnerTab(targetTab) {
        const formView = document.getElementById("inner-view-new-request");
        const historyView = document.getElementById("inner-view-request-history");

        const btnForm = document.getElementById("tab-new-request");
        const btnHistory = document.getElementById("tab-request-history");

        if (targetTab === 'new-request') {
          if (formView) formView.style.display = "block";
          if (historyView) historyView.style.display = "none";

          // Active Form Styling
          btnForm.style.background = "#2563eb";
          btnForm.style.color = "white";
          btnHistory.style.background = "#1e293b";
          btnHistory.style.color = "#94a3b8";
        } else if (targetTab === 'request-history') {
          if (formView) formView.style.display = "none";
          if (historyView) historyView.style.display = "block";

          // Active History Styling
          btnForm.style.background = "#1e293b";
          btnForm.style.color = "#94a3b8";
          btnHistory.style.background = "#2563eb";
          btnHistory.style.color = "white";

          // Fetch logs directly when switching to history tab
          if (typeof loadStaffRequestHistory === "function") {
            loadStaffRequestHistory();
          }
        }
      }

      function toggleLeaveTypeNotice() {
        const typeValue = document.getElementById("leaveType").value;
        const noticeSpan = document.getElementById("leaveTypeNotice");

        if (typeValue === "yearly_leave") {
          noticeSpan.innerHTML = "⚠️ This will deduct active days from your 30-day Yearly Balance upon approval.";
          noticeSpan.style.color = "#dc2626";
        } else if (typeValue === "emergency_leave") {
          noticeSpan.innerHTML = "ℹ️ Emergency request category. This will bypass annual metrics deductions.";
          noticeSpan.style.color = "#d97706";
        } else {
          noticeSpan.innerHTML = "Standard single day permission.";
          noticeSpan.style.color = "#475569";
        }
      }


      async function loadStaffList(query = "") {
        const response = await fetch(
          `${backendURL}/api/admin/staff_list?search=${query}`,
        );
        const staff = await response.json();
        const tbody = document.getElementById("staffTableBody");
        tbody.innerHTML = "";

        staff.forEach((person) => {
          // Escape single quotes in names/departments to avoid JS syntax errors
          const name = person.name.replace(/'/g, "\\'");
          const dept = person.department.replace(/'/g, "\\'");

          const salary = person.base_monthly_salary || 0;
          const overtime = person.overtime_rate || 0;

          tbody.innerHTML += `
        <tr style="border-bottom: 1px solid #cbd5e1;">
            <td style="padding: 10px;">${person.id}</td>
            <td>${person.name}</td>
            <td>${person.department}</td>
            <td>
                <button onclick="openEditModal('${person.id}', '${name}', '${dept}', ${salary}, ${overtime})" 
                        style="background:#f59e0b; color:white; border:none; padding:5px 10px; border-radius:4px; cursor:pointer;">
                    <i class="fas fa-edit"></i>
                </button>
                <button onclick="deleteStaff('${person.id}')" 
                        style="background:#ef4444; color:white; border:none; padding:5px 10px; border-radius:4px; cursor:pointer;">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>`;
        });
      }



      function filterStaffTable() {
        const input = document.getElementById("staffSearchInput");
        const filter = input.value.toLowerCase();
        const tbody = document.getElementById("staffTableBody");
        const rows = tbody.getElementsByTagName("tr");

        for (let i = 0; i < rows.length; i++) {
          // Get all cells in the current row
          const cells = rows[i].getElementsByTagName("td");
          let rowMatches = false;

          // Loop through cells (ID is index 0, Name is index 1, Dept is index 2)
          for (let j = 0; j < cells.length; j++) {
            const cellValue = cells[j].textContent || cells[j].innerText;

            // Convert everything to string and lowercase for a fair comparison
            if (cellValue.toLowerCase().includes(filter)) {
              rowMatches = true;
              break; // Stop looking at cells for this row if we found a match
            }
          }

          // Show/Hide the row based on the match
          rows[i].style.display = rowMatches ? "" : "none";
        }
      }

      function openEditModal(id, name, dept, salary = 0, overtime = 0) {
        document.getElementById("editOldId").value = id;
        document.getElementById("editNewId").value = id;
        document.getElementById("editName").value = name;
        document.getElementById("editDept").value = dept;

        // Fill the salary/overtime fields
        document.getElementById("editSalary").value = salary;
        document.getElementById("editOvertime").value = overtime;

        // Reset the re-scan checkbox
        document.getElementById("reScanFace").checked = false;
        document.getElementById("directUpdateArea").style.display = "none";

        document.getElementById("editModal").style.display = "block";
      }

      function closeEditModal() {
        // 1. Hide the modal
        document.getElementById("editModal").style.display = "none";

        // 2. IMPORTANT: Also hide the camera area so it's fresh for next time
        document.getElementById("directUpdateArea").style.display = "none";

        // 3. Reset the checkbox
        document.getElementById("reScanFace").checked = false;

        // 4. Stop the camera if it was left running
        const video = document.getElementById("updateVideo");
        if (video.srcObject) {
          video.srcObject.getTracks().forEach(track => track.stop());
          video.srcObject = null;
        }
      }

      async function deleteStaff(staffId) {
        if (confirm(`Are you sure you want to delete Staff ID: ${staffId}?`)) {
          try {
            const response = await fetch(
              `${backendURL}/api/admin/delete_staff/${staffId}`,
              {
                method: "DELETE",
              },
            );
            const result = await response.json();
            if (result.success) {
              alert("Staff deleted successfully");
              loadStaffList(); // Refresh the table
            }
          } catch (err) {
            console.error("Delete failed:", err);
          }
        }
      }
     async function saveEdit() {

        const isReScan = document.getElementById('reScanFace').checked;
        const oldId = document.getElementById('editOldId').value.trim();
        const newId = document.getElementById('editNewId').value.trim();
        const newName = document.getElementById('editName').value.trim();
        const newDept = document.getElementById('editDept').value.trim();
        const newSalary = document.getElementById('editSalary').value.trim();
        const newOvertime = document.getElementById('editOvertime').value.trim();

        const saveBtn = document.querySelector("#editModal button[onclick*='saveEdit']");
        const originalBtnText = saveBtn ? saveBtn.innerHTML : 'Save Changes';

        if (!oldId || !newId || !newName || !newDept) {
          alert('Please fill in all required fields.');
          return;
        }

        try {
          if (saveBtn) {
            saveBtn.disabled = true;
            saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
          }

          const response = await fetch(`${backendURL}/api/admin/update_staff`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              old_id: oldId,
              new_id: newId,
              name: newName,
              dept: newDept,
              salary: parseFloat(newSalary) || 0,
              overtime: parseFloat(newOvertime) || 0,
              delete_face: isReScan
            })
          });

          const result = await response.json();

          if (result.success) {
            await loadStaffList();        // Refresh table only
            closeEditModal();
            showSection('staffManagement'); // Show immediately to prevent glitch
            console.log('✅ Staff updated and stayed on Manage Staffs page.');
          } else {
            alert('Update failed: ' + (result.message || 'Unknown error'));
          }
        } catch (err) {
          console.error('Save Error:', err);
          alert('Unable to connect to the server.');
        } finally {
          if (saveBtn) {
            saveBtn.disabled = false;
            saveBtn.innerHTML = originalBtnText;
          }
        }
      }

      let updateStream = null;
      window.updateStream = updateStream;



      async function openUpdateCamera() {
        try {
          if (updateStream) {
            updateStream.getTracks().forEach(track => track.stop());
            updateStream = null;
            window.updateStream = updateStream;
          }

          updateStream = await navigator.mediaDevices.getUserMedia({
            video: {
              width: { ideal: 640 },
              height: { ideal: 480 },
              facingMode: "user"
            }
          });

          window.updateStream = updateStream;

          const video = document.getElementById("updateVideo");
          if (!video) return;

          video.srcObject = updateStream;

          video.onloadedmetadata = () => {
            video.play();
            const area = document.getElementById("directUpdateArea");
            const progress = document.getElementById("captureProgress");
            if (area) area.style.display = "block";
            if (progress) progress.innerText = "Camera Ready. Click Capture.";
          };
        } catch (err) {
          alert("Cannot access camera. Please allow permissions.");
          console.error(err);
        }
      }



      function cancelReScan() {
        if (window.updateStream) {
          window.updateStream.getTracks().forEach(track => track.stop());
          window.updateStream = null;
        }

        const area = document.getElementById('directUpdateArea');
        const progress = document.getElementById('captureProgress');
        const video = document.getElementById('updateVideo');
        const box = document.getElementById('reScanFace');

        if (area) area.style.display = 'none';
        if (progress) progress.innerText = '';
        if (box) box.checked = false;
        if (video) video.srcObject = null;
      }


      async function captureMultipleFaces() {
        const video = document.getElementById("updateVideo");
        const canvas = document.getElementById("updateCanvas");
        const progress = document.getElementById("captureProgress");
        const ctx = canvas.getContext("2d");

        let capturedImages = [];
        const TOTAL_CAPTURES = 5;

        // Check if video is playing and has valid dimensions
        if (!video.srcObject || video.paused || video.ended) {
          alert("Camera is not active or ready. Please open the camera first.");
          return;
        }

        // Critical check: ensure we have real frame dimensions
        if (!video.videoWidth || !video.videoHeight || video.videoWidth === 0 || video.videoHeight === 0) {
          alert("Camera frame is not ready yet. Please wait 2-3 seconds after opening the camera, then try again.");
          return;
        }

        // Helper to wait
        const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

        for (let i = 0; i < TOTAL_CAPTURES; i++) {

          // STEP A: COUNTDOWN so user can position their face
          for (let countdown = 3; countdown > 0; countdown--) {
            progress.innerText = `📷 Photo ${i + 1}/${TOTAL_CAPTURES} — Hold still... ${countdown}`;
            progress.style.color = "#f59e0b"; // Orange
            await wait(1000);
          }

          // STEP B: CAPTURE
          progress.innerText = `📸 Capturing ${i + 1}/${TOTAL_CAPTURES}...`;
          progress.style.color = "#2563eb"; // Blue

          // Validate dimensions again before each capture
          if (video.videoWidth === 0 || video.videoHeight === 0) {
            progress.innerText = "⚠️ Frame lost. Skipping...";
            continue;
          }

          // Set canvas size to actual video dimensions
          canvas.width = video.videoWidth;
          canvas.height = video.videoHeight;

          // Draw current video frame to canvas
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

          // Convert to Base64 JPEG at high quality for better face detection
          const imageData = canvas.toDataURL("image/jpeg", 0.95);

          // Validate the captured image is not trivially small (blank frame guard)
          if (imageData.length < 5000) {
            progress.innerText = `⚠️ Blank frame detected, retrying...`;
            i--; // retry this capture
            await wait(1000);
            continue;
          }

          capturedImages.push(imageData);

          // STEP C: CONFIRM
          progress.innerText = `✅ Captured ${i + 1}/${TOTAL_CAPTURES}`;
          progress.style.color = "#10b981"; // Green
          await wait(800);
        }

        if (capturedImages.length === 0) {
          progress.innerText = "❌ No valid frames captured. Please try again.";
          progress.style.color = "red";
          return;
        }

        progress.innerText = `Uploading ${capturedImages.length} image(s) to server...`;
        progress.style.color = "#333";

        // Send to backend
        await uploadUpdatedBiometrics(capturedImages);
      }

      async function uploadUpdatedBiometrics(images) {
        const staffId = document.getElementById("editOldId").value;
        const progress = document.getElementById("captureProgress");

        if (progress) {
          progress.innerHTML = `
      <div style="background: rgba(37, 99, 235, 0.1); border: 1px solid #2563eb; color: #1e40af; padding: 12px; border-radius: 8px; margin-top: 10px;">
        <i class="fas fa-spinner fa-spin"></i> Uploading ${images.length} frames... Processing model embed weights.
      </div>
    `;
        }

        try {
          const response = await fetch("http://127.0.0.1:5000/api/update_face_biometrics", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ staff_id: staffId, images: images }),
          });

          const result = await response.json();

          if (response.ok && result.status === "success") {
            if (progress) {
              progress.innerHTML = `
          <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10b981; color: #065f46; padding: 12px; border-radius: 8px; margin-top: 10px;">
            <i class="fas fa-check-circle"></i> <strong>Biometrics Saved Successfully!</strong>
          </div>
        `;
            }

            // Hold message visibility for 2.5 seconds
            await new Promise(resolve => setTimeout(resolve, 2500));
            cancelReScan();
            closeEditModal();
            showSection("staffManagement");
          } else {
            if (progress) {
              progress.innerHTML = `<div style="color: red; padding: 10px;">Failed: ${result.message}</div>`;
            }
          }
        } catch (err) {
          console.error(err);
          if (progress) {
            progress.innerHTML = `<div style="color: red; padding: 10px;">Network Upload Error.</div>`;
          }
        }
      }


      async function submitLeaveRequest() {
        const formMessage = document.getElementById("leaveFormMessage");
        if (formMessage) formMessage.innerText = "";

        const leaveType = document.getElementById("leaveType").value;
        const startDate = document.getElementById("leaveDateRange").value;
        const duration = document.getElementById("leaveDuration").value;
        const reasonText = document.getElementById("reasonText").value.trim();
        const fileSelector = document.getElementById("supportingFile");

        if (!startDate || !reasonText || !duration) {
          alert("Please completely satisfy all required input fields (*).");
          return;
        }

        // Map into Multipart data payload format
        const packageData = new FormData();
        packageData.append("staff_id", localStorage.getItem("user_id") || "");
        packageData.append("start_date", startDate);
        packageData.append("duration", duration);
        packageData.append("leave_type", leaveType);

        // Apply explicit categorizations to reason strings so reporting loops parse them accurately
        if (leaveType === "yearly_leave") {
          packageData.append("reason", `[YEARLY LEAVE] ${reasonText}`);
        } else if (leaveType === "emergency_leave") {
          packageData.append("reason", `[EMERGENCY] ${reasonText}`);
        } else {
          packageData.append("reason", reasonText);
        }

        if (fileSelector && fileSelector.files[0]) {
          packageData.append("file", fileSelector.files[0]);
        }

        try {
          const apiCall = await fetch(`${backendURL}/api/permission_requests`, {
            method: "POST",
            body: packageData
          });

          const output = await apiCall.json();
          if (apiCall.ok) {
            if (formMessage) {
              formMessage.innerHTML = `<span style="color: #16a34a; font-weight: bold;">✔️ Request successfully dispatched! Current state: Pending administrative review.</span>`;
            }

            // -----------------------------------------------------------------
            // 🔄 UPDATED RESET BLOCK: No more forcing fixed values
            // -----------------------------------------------------------------
            document.getElementById("reasonText").value = "";
            document.getElementById("leaveDateRange").value = "";

            // Option A: Clear it completely so it's empty for the next custom entry
            document.getElementById("leaveDuration").value = "";

            // (Alternative Option B: If you prefer it to reset to empty placeholder text, 
            // you can use the line above. It leaves it open for whatever number they type.)

            if (fileSelector) fileSelector.value = "";

            // Refresh matching history outputs instantly if defined
            if (typeof loadStaffLeaveHistory === "function") loadStaffLeaveHistory();
          } else {
            if (formMessage) formMessage.innerHTML = `<span style="color: #dc2626;">❌ Rejected: ${output.message || "Execution exception"}</span>`;
          }
        } catch (err) {
          console.error("Transmission Error:", err);
          if (formMessage) formMessage.innerHTML = `<span style="color: #dc2626;">❌ Communication failure. Verification engine unavailable.</span>`;
        }
      }


      async function loadPermissionRequests() {
        const tbody = document.getElementById("requestsTableBody");
        if (!tbody) {
          console.error("CRITICAL: Could not find HTML element with id='requestsTableBody'");
          return;
        }

        try {
          // Fetches cleanly from the explicit localhost Flask server address
          const response = await fetch("http://127.0.0.1:5000/api/admin/all_requests");

          if (!response.ok) {
            throw new Error(`HTTP error! Server responded with status: ${response.status}`);
          }

          const requests = await response.json();
          tbody.innerHTML = ""; // Clear hardcoded placeholder rows

          // Filter using .trim() to normalize invisible spaces/tabs from strings
          const pendingRequests = requests.filter(req => {
            return req.status && req.status.toLowerCase().trim() === "pending";
          });

          if (pendingRequests.length === 0) {
            // Updated colspan to 8 to handle the new duration column smoothly
            tbody.innerHTML = `
        <tr>
          <td colspan="8" class="text-center" style="padding: 20px; color: #64748b; font-style: italic; text-align: center;">
            No pending absence requests found.
          </td>
        </tr>`;
            return;
          }

          // Render the table records matching your exact column sequence
          pendingRequests.reverse().forEach(req => {
            let actionButtons = `
        <button onclick="handleRequestAction(${req.id}, 'approved')" 
                style="background: #2ecc71; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-weight: bold; margin-right: 5px;">
            Approve
        </button>
        <button onclick="handleRequestAction(${req.id}, 'denied')" 
                style="background: #ff4757; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-weight: bold;">
            Deny
        </button>
      `;

            // Added the duration <td> matching the structural sequence
            tbody.innerHTML += `
        <tr style="border-bottom: 1px solid #334155; color: #f8fafc;">
          <td style="padding: 12px; font-weight: bold; color: black;">#${req.id}</td>
          <td style="padding: 12px; color: black;">${req.staff_id}</td>
          <td style="padding: 12px; font-weight: 500; color: black;">${req.name}</td>
          <td style="padding: 12px; color: black;">${req.start_date}</td>
          <td style="padding: 12px; font-weight: bold; color: #e67e22;">${req.duration || 1} Days</td> <td style="padding: 12px; max-width: 200px; word-wrap: break-word; color: black;">${req.reason}</td>
          <td style="padding: 12px;">
            <span style="background: rgba(241, 196, 15, 0.2); color: #f1c40f; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; text-transform: uppercase;">
              ${req.status}
            </span>
          </td>
          <td style="padding: 12px;">${actionButtons}</td>
        </tr>
      `;
          });
        } catch (error) {
          console.error("DEBUG ENGINE LOG:", error);
          // Updated fallback message colspan to 8
          tbody.innerHTML = `<tr><td colspan="8" class="text-center" style="color: #ff4757; padding: 20px; text-align: center; font-weight: bold;">Failed to load requests from server. (${error.message})</td></tr>`;
        }
      }

      async function reviewPermission(requestId, newStatus) {
        if (
          !confirm(`Are you sure you want to set this request to ${newStatus}?`)
        )
          return;

        try {
          const response = await fetch(`${backendURL}/api/permission_review`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              request_id: requestId,
              status: newStatus,
            }),
          });

          if (response.ok) {
            alert(`Request successfully ${newStatus}`);
            loadPermissionRequests(); // Refresh the table immediately
          } else {
            const err = await response.json();
            alert("Error: " + err.message);
          }
        } catch (error) {
          console.error("Review Error:", error);
        }
      }
      function loadProcessedRequests() {
        console.log(
          "Note: In a full implementation, loadProcessedRequests() would fetch Approved/Denied history.",
        );
        // This function would fetch /api/permission_requests?status=processed or similar
      }

      async function processRequestAction(requestId, action) {
        let adminRemarks = "";

        if (action === "denied") {
          adminRemarks = prompt("Reason for Denial (e.g., 'Today is a busy day, you must come to the hospital'):");
          if (adminRemarks === null) return;
          if (adminRemarks.trim() === "") {
            alert("You must provide a reason to deny this request.");
            return;
          }
        } else {
          adminRemarks = "Approved by Administration";
        }

        const payload = {
          id: Number(requestId), // FORCE cast to a true Number type
          status: action,
          admin_remarks: adminRemarks.trim()
        };

        try {
          const response = await fetch(`http://127.0.0.1:5000/api/admin/process_request`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });

          if (response.ok) {
            alert(`Request status updated to ${action}!`);
            // Use this custom function instead of location.reload() if available
            // to keep the Admin inside their active tab view smoothly
            if (typeof loadAdminRequests === "function") {
              loadAdminRequests();
            } else {
              location.reload();
            }
          } else {
            alert("Error updating decision state.");
          }
        } catch (error) {
          console.error("Network Error:", error);
        }
      }
      // Add or append this data rendering block inside your existing loadPayroll() function
      // right after you calculate or fetch your total payroll, total deductions, and count values:

      function updateAccountantDashboardMetrics(totalPayroll, totalStaff, totalDeductions) {
        const rawRole = localStorage.getItem("role") || localStorage.getItem("userRole") || "";
        if (rawRole.toLowerCase().trim().includes("accountant") || rawRole.toLowerCase().trim() === "finance") {

          // 1. Target the cards situated inside "dashboardContent" to mirror clean figures
          // Safely mappings into your existing admin indicator cards text containers:
          const card1 = document.getElementById("totalStaffCount") || document.getElementById("totalRegisteredStaffs");
          const card2 = document.getElementById("enrolledFacesCount") || document.getElementById("enrolledFaceRecords");
          const card3 = document.getElementById("presentTodayCount") || document.getElementById("presentToday");

          if (card1) card1.innerText = `${totalPayroll.toFixed(2)} ETB`;
          if (card2) card2.innerText = totalStaff;
          if (card3) card3.innerText = `${totalDeductions.toFixed(2)} ETB`;

          // Update the layout labels directly above those values dynamically if they exist
          // to give them perfect financial context titles
          const label1 = document.querySelector("#totalStaffCount")?.previousElementSibling;
          if (label1) label1.innerText = "Total Payroll";

          const label2 = document.querySelector("#enrolledFacesCount")?.previousElementSibling;
          if (label2) label2.innerText = "Total Staff Paid";

          const label3 = document.querySelector("#presentTodayCount")?.previousElementSibling;
          if (label3) label3.innerText = "Total Deductions";
        }
      }


      async function loadStaffRequestHistory() {
        const staffId = localStorage.getItem("user_id");
        const tbody = document.getElementById("staffRequestHistory");
        if (!tbody || !staffId) return;

        try {
          const response = await fetch(`http://127.0.0.1:5000/api/my_requests/${staffId}`);
          const data = await response.json();

          tbody.innerHTML = "";

          // Safety check if the database array comes back completely empty
          if (data.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" class="text-center" style="padding: 20px; color: #64748b;">No requests found.</td></tr>`;
            return;
          }

          data.reverse().forEach(req => {
            // 1. Compute dynamic status color configurations
            let statusColor = req.status === "approved" ? "#2ecc71" : (req.status === "denied" ? "#ff4757" : "#f1c40f");

            // 2. Handle Admin Remarks or fallback gracefully
            let remarks = req.admin_remarks ? req.admin_remarks : `<span style="color: #64748b;">—</span>`;

            // 3. Render cells with explicit color styles for perfect contrast
            tbody.innerHTML += `
    <tr style="border-bottom: 1px solid #334155;">
      <td style="padding: 12px; color: #0c0c0c; font-weight: 500;">${req.start_date}</td>
      
      <td style="padding: 12px; color: #0c0c0c; max-width: 250px; word-wrap: break-word;">${req.reason}</td>
      
      <td style="padding: 12px; color: ${statusColor}; font-weight: bold; text-transform: capitalize;">${req.status}</td>
      
      <td style="padding: 12px; font-style: italic; color: ${req.admin_remarks ? '#ff793f' : '#64748b'};">${remarks}</td>
    </tr>
  `;
          });

        } catch (error) {
          console.error("Error loading request history:", error);
        }
      }


      async function updateAdminNotifications() {
        // 1. Check who is logged in
        const userRole = localStorage.getItem("userRole");

        const banner = document.getElementById('admin-notification-banner');
        const navBadge = document.getElementById('nav-notification-badge');

        // 2. FIREWALL: If not admin, hide everything and QUIT
        if (!userRole || userRole.toLowerCase() !== 'admin') {
          if (banner) banner.style.display = 'none';
          if (navBadge) navBadge.style.display = 'none';
          return;
        }

        // 3. ONLY ADMINS REACH THIS PART
        try {
          const response = await fetch(`http://127.0.0.1:5000/api/admin_notifications`);
          const data = await response.json();
          const countSpan = document.getElementById('pending-request-count');

          if (data.pending_count > 0) {
            if (countSpan) countSpan.innerText = data.pending_count;
            if (banner) banner.style.display = 'flex';
            if (navBadge) {
              navBadge.innerText = data.pending_count;
              navBadge.style.display = 'inline-block';
            }
          } else {
            if (banner) banner.style.display = 'none';
            if (navBadge) navBadge.style.display = 'none';
          }
        } catch (error) {
          console.error("Notification check failed:", error);
        }
      }

      async function refreshAdminDashboard() {
        // --- CRITICAL ACCOUNTANT POLICING GUARD ---
        const rawRole = localStorage.getItem("role") || localStorage.getItem("userRole") || "";
        const currentRole = rawRole.toLowerCase().trim();

        // If the user is an accountant, exit immediately so the financial values aren't overwritten
        if (currentRole.includes("accountant") || currentRole === "finance") {
          console.log("Poller Blocked: Hospital Accountant active. Preserving payroll display metrics.");
          return;
        }

        try {
          const response = await fetch(`${backendURL || 'http://127.0.0.1:5000'}/api/admin_stats`, {
            headers: typeof getAuthToken === "function" ? { Authorization: `Bearer ${getAuthToken()}` } : {}
          });

          if (response.ok) {
            const data = await response.json();
            console.log("BACKEND ADMIN DATA RECEIVED:", data);

            // Map matching targets by checking all fallback template element IDs
            const staffEl = document.getElementById("totalStaffCount") || document.getElementById("statCardValue1") || document.getElementById("totalRegisteredStaffs");
            const facesEl = document.getElementById("enrolledFacesCount") || document.getElementById("statCardValue2") || document.getElementById("enrolledFaceRecords");
            const presentEl = document.getElementById("presentTodayCount") || document.getElementById("statCardValue3") || document.getElementById("presentToday");

            // Update the standard system administration values
            if (staffEl) staffEl.innerText = data.total_staff || 0;
            if (facesEl) facesEl.innerText = data.enrolled_faces || 0;
            if (presentEl) presentEl.innerText = data.present_today || 0;

            console.log("UI Admin Stats Updated successfully.");
          }
        } catch (error) {
          console.error("Dashboard failed to fetch admin status data stream:", error);
        }
      }

      // Global recurring polling loop definitions
      setInterval(() => {
        const dashContent = document.getElementById("dashboardContent");
        if (dashContent && dashContent.style.display === "block") {
          refreshAdminDashboard();
        }
      }, 5000);

      async function loadStaffHistory() {
        const staffId = localStorage.getItem("user_id");
        const tbody = document.getElementById("staffRequestHistory");

        if (!tbody) return;

        try {
          const response = await fetch(`http://127.0.0.1:5000/api/my_requests/${staffId}`);
          const requests = await response.json();

          tbody.innerHTML = ""; // Clear fallback row safely

          if (requests.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center" style="padding: 20px; color: #64748b;">No requests submitted yet.</td></tr>';
            return;
          }

          requests.reverse().forEach(req => {
            let statusColor = "#f1c40f"; // Pending
            if (req.status === "approved") statusColor = "#2ecc71"; // Approved
            if (req.status === "denied") statusColor = "#ff4757";   // Denied

            // If admin_remarks exists, use it. Otherwise fall back to a clean placeholder dash
            let remarks = req.admin_remarks ? req.admin_remarks : `<span style="color: #64748b;">—</span>`;

            tbody.innerHTML += `
        <tr style="border-bottom: 1px solid #334155;">
            <td style="padding: 12px; color: #f8fafc; font-weight: 500;">${req.start_date}</td>
            <td style="padding: 12px; color: #cbd5e1; max-width: 250px; word-wrap: break-word;">${req.reason}</td>
            <td style="padding: 12px; color: ${statusColor}; font-weight: bold; text-transform: uppercase;">
                ${req.status}
            </td>
            <td style="padding: 12px; font-style: italic; color: ${req.admin_remarks ? '#ff793f' : '#64748b'};">
                ${remarks}
            </td>
        </tr>
         `;
          });
        } catch (error) {
          console.error("Error loading history:", error);
        }
      }

      async function loadAdminRequests() {
        const tbody = document.getElementById("adminRequestTableBody"); // Double check this ID matches your admin HTML <tbody>
        if (!tbody) return;

        try {
          // 1. Fetch all requests from your admin endpoint
          const response = await fetch("http://127.0.0.1:5000/api/admin/all_requests"); // Change to your actual admin fetch route
          const requests = await response.json();

          tbody.innerHTML = ""; // Clear old rows

          if (requests.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center" style="color: #64748b; padding: 20px;">No requests to review.</td></tr>';
            return;
          }

          requests.reverse().forEach(req => {
            let actionButtons = "";

            // 2. ONLY give choices if the request status is still pending
            if (req.status === "pending") {
              actionButtons = `
          <button onclick="processRequestAction(${req.id}, 'approved')" style="background: #2ecc71; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-weight: bold; margin-right: 5px;">Approve</button>
          <button onclick="processRequestAction(${req.id}, 'denied')" style="background: #ff4757; color: white; border: none; padding: 6px 12px; border-radius: 4px; cursor: pointer; font-weight: bold;">Deny</button>
        `;
            } else {
              let statusColor = req.status === "approved" ? "#2ecc71" : "#ff4757";
              actionButtons = `<span style="color: ${statusColor}; font-weight: bold; text-transform: uppercase;">${req.status}</span>`;
            }

            let remarks = req.admin_remarks ? req.admin_remarks : `<span style="color: #64748b; font-style: italic;">None</span>`;

            // 3. Render rows out matching the admin panel's 5 columns
            tbody.innerHTML += `
        <tr style="border-bottom: 1px solid #334155; color: white;">
          <td style="padding: 12px;">${req.name} (ID: ${req.staff_id})</td>
          <td style="padding: 12px;">${req.start_date}</td>
          <td style="padding: 12px;">${req.reason}</td>
          <td style="padding: 12px; color: #cbd5e1; font-style: italic;">${remarks}</td>
          <td style="padding: 12px;">${actionButtons}</td>
        </tr>
      `;
          });
        } catch (error) {
          console.error("Error loading admin request layout:", error);
        }
      }

    </script>
</body>

</html>
