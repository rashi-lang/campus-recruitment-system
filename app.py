from flask import Flask, request, redirect, session, send_from_directory
import sqlite3
import os

app = Flask(__name__)

app.secret_key = "campus123"

DATABASE = "campus.db"

# Resume upload folder
UPLOAD_FOLDER = "uploads"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


# =====================================================
# DATABASE CONNECTION
# =====================================================

def database():

    conn = sqlite3.connect(DATABASE)

    conn.row_factory = sqlite3.Row

    return conn


# =====================================================
# CREATE DATABASE
# =====================================================

def create_database():

    conn = database()

    # STUDENTS TABLE
    conn.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT,
            percentage REAL,
            resume TEXT
        )
    """)

    # If old database exists without resume column,
    # add the column automatically
    try:
        conn.execute("SELECT resume FROM students LIMIT 1")
    except sqlite3.OperationalError:
        conn.execute("""
            ALTER TABLE students
            ADD COLUMN resume TEXT
        """)

    # COMPANIES TABLE
    conn.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT UNIQUE,
            password TEXT
        )
    """)

    # JOBS TABLE
    conn.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER,
            title TEXT,
            description TEXT,
            minimum_percentage REAL
        )
    """)

    # APPLICATIONS TABLE
    conn.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            job_id INTEGER,
            status TEXT
        )
    """)

    # CREATE DEMO COMPANY
    company = conn.execute(
        "SELECT * FROM companies WHERE email=?",
        ("company@gmail.com",)
    ).fetchone()

    if company is None:

        conn.execute("""
            INSERT INTO companies
            (name, email, password)
            VALUES (?, ?, ?)
        """, (
            "ABC Technologies",
            "company@gmail.com",
            "1234"
        ))

    # CREATE DEMO JOBS
    company = conn.execute(
        "SELECT id FROM companies WHERE email=?",
        ("company@gmail.com",)
    ).fetchone()

    job = conn.execute(
        "SELECT * FROM jobs LIMIT 1"
    ).fetchone()

    if job is None:

        conn.execute("""
            INSERT INTO jobs
            (company_id, title, description, minimum_percentage)
            VALUES (?, ?, ?, ?)
        """, (
            company["id"],
            "Python Developer",
            "Python and Flask development internship.",
            60
        ))

        conn.execute("""
            INSERT INTO jobs
            (company_id, title, description, minimum_percentage)
            VALUES (?, ?, ?, ?)
        """, (
            company["id"],
            "Web Developer",
            "HTML CSS and basic web development internship.",
            50
        ))

    conn.commit()

    conn.close()


# =====================================================
# HOME PAGE
# =====================================================

@app.route("/")
def home():

    return """
<!DOCTYPE html>

<html>

<head>

<title>Campus Recruitment System</title>

<style>

body {
    font-family: Arial;
    margin: 0;
    background: #f2f5f9;
}

nav {
    background: #172554;
    color: white;
    padding: 20px;
}

nav a {
    color: white;
    text-decoration: none;
    margin: 15px;
}

.container {
    text-align: center;
    padding: 70px 20px;
}

h1 {
    color: #172554;
    font-size: 42px;
}

p {
    font-size: 18px;
}

.button {
    display: inline-block;
    padding: 14px 22px;
    margin: 8px;
    background: #2563eb;
    color: white;
    text-decoration: none;
    border-radius: 7px;
}

.green {
    background: #16a34a;
}

.card {
    background: white;
    padding: 25px;
    margin: 30px auto;
    max-width: 700px;
    border-radius: 10px;
}

</style>

</head>

<body>

<nav>

<b>Campus Recruitment System</b>

<a href="/">Home</a>

<a href="/jobs">Jobs</a>

<a href="/student/login">Student Login</a>

<a href="/company/login">Company Login</a>

</nav>


<div class="container">

<h1>Campus Recruitment System</h1>

<p>
A simple platform connecting students and companies.
</p>


<a class="button"
href="/student/register">

Student Registration

</a>


<a class="button"
href="/student/login">

Student Login

</a>


<a class="button green"
href="/company/register">

Company Registration

</a>


<a class="button green"
href="/company/login">

Company Login

</a>


<div class="card">

<h2>System Features</h2>

<p>Student Registration</p>

<p>Student Login</p>

<p>Resume Upload</p>

<p>Company Registration</p>

<p>Company Login</p>

<p>Job Opportunities</p>

<p>Automatic Eligibility Checking</p>

<p>Online Job Application</p>

<p>Application Status</p>

<p>Company Job Posting</p>

</div>

</div>

</body>

</html>
"""


# =====================================================
# STUDENT REGISTRATION
# =====================================================

@app.route("/student/register", methods=["GET", "POST"])
def student_register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        password = request.form["password"]

        percentage = request.form["percentage"]

        conn = database()

        try:

            conn.execute("""
                INSERT INTO students
                (name, email, password, percentage, resume)
                VALUES (?, ?, ?, ?, ?)
            """, (
                name,
                email,
                password,
                percentage,
                None
            ))

            conn.commit()

            conn.close()

            return """
            <h2>Student Registration Successful!</h2>

            <p>Your account has been created.</p>

            <a href="/student/login">
            Login Now
            </a>
            """

        except:

            conn.close()

            return """
            <h2>Email already registered.</h2>

            <a href="/student/register">
            Try Again
            </a>
            """

    return """

<!DOCTYPE html>

<html>

<head>

<title>Student Registration</title>

<style>

body {
    font-family: Arial;
    background: #f2f5f9;
}

.box {
    background: white;
    width: 400px;
    margin: 70px auto;
    padding: 30px;
    border-radius: 10px;
}

input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    box-sizing: border-box;
}

button {
    width: 100%;
    padding: 12px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 5px;
}

a {
    text-decoration: none;
}

</style>

</head>

<body>

<div class="box">

<h2>Student Registration</h2>

<form method="POST">

<input
name="name"
placeholder="Full Name"
required
>

<input
type="email"
name="email"
placeholder="Email"
required
>

<input
type="password"
name="password"
placeholder="Password"
required
>

<input
type="number"
name="percentage"
placeholder="Percentage"
min="0"
max="100"
required
>

<button>
Register
</button>

</form>

<br>

<a href="/student/login">
Already have account? Login
</a>

<br><br>

<a href="/">
Back to Home
</a>

</div>

</body>

</html>

"""


# =====================================================
# STUDENT LOGIN
# =====================================================

@app.route("/student/login", methods=["GET", "POST"])
def student_login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        conn = database()

        student = conn.execute("""
            SELECT * FROM students
            WHERE email=? AND password=?
        """, (
            email,
            password
        )).fetchone()

        conn.close()

        if student:

            session["student_id"] = student["id"]

            return redirect("/student/dashboard")

        return """
        <h2>Invalid email or password.</h2>

        <a href="/student/login">
        Try Again
        </a>
        """

    return """

<!DOCTYPE html>

<html>

<head>

<title>Student Login</title>

<style>

body {
    font-family: Arial;
    background: #f2f5f9;
}

.box {
    background: white;
    width: 400px;
    margin: 100px auto;
    padding: 30px;
    border-radius: 10px;
}

input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    box-sizing: border-box;
}

button {
    width: 100%;
    padding: 12px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 5px;
}

</style>

</head>

<body>

<div class="box">

<h2>Student Login</h2>

<form method="POST">

<input
type="email"
name="email"
placeholder="Email"
required
>

<input
type="password"
name="password"
placeholder="Password"
required
>

<button>
Login
</button>

</form>

<br>

<a href="/student/register">
Create New Account
</a>

<br><br>

<a href="/">
Back to Home
</a>

</div>

</body>

</html>

"""


# =====================================================
# STUDENT DASHBOARD
# =====================================================

@app.route("/student/dashboard")
def student_dashboard():

    if "student_id" not in session:

        return redirect("/student/login")

    conn = database()

    student = conn.execute("""
        SELECT * FROM students
        WHERE id=?
    """, (
        session["student_id"],
    )).fetchone()

    jobs = conn.execute("""
        SELECT jobs.*, companies.name AS company_name
        FROM jobs
        JOIN companies
        ON jobs.company_id = companies.id
    """).fetchall()

    applications = conn.execute("""
        SELECT applications.*, jobs.title
        FROM applications
        JOIN jobs
        ON applications.job_id = jobs.id
        WHERE applications.student_id=?
    """, (
        session["student_id"],
    )).fetchall()

    conn.close()


    # Resume section

    if student["resume"]:

        resume_section = f"""
        <p>
        Resume uploaded successfully.
        </p>

        <a href="/resume/{student['resume']}"
        target="_blank">

        View Resume

        </a>
        """

    else:

        resume_section = """
        <p>
        No resume uploaded yet.
        </p>
        """


    # Job section

    job_html = ""

    for job in jobs:

        if student["percentage"] >= job["minimum_percentage"]:

            eligibility = "Eligible"

            button = f"""
            <form method="POST"
            action="/apply/{job['id']}">

            <button>
            Apply
            </button>

            </form>
            """

        else:

            eligibility = "Not Eligible"

            button = """
            <button disabled>
            Not Eligible
            </button>
            """

        job_html += f"""

        <div class="job">

        <h3>{job['title']}</h3>

        <p>
        Company: {job['company_name']}
        </p>

        <p>
        {job['description']}
        </p>

        <p>
        Minimum Percentage:
        {job['minimum_percentage']}%
        </p>

        <p>
        Your Percentage:
        {student['percentage']}%
        </p>

        <b>{eligibility}</b>

        <br><br>

        {button}

        </div>

        """


    # Application section

    application_html = ""

    for application in applications:

        application_html += f"""

        <tr>

        <td>
        {application['title']}
        </td>

        <td>
        {application['status']}
        </td>

        </tr>

        """


    return f"""

<!DOCTYPE html>

<html>

<head>

<title>Student Dashboard</title>

<style>

body {{
    font-family: Arial;
    background: #f2f5f9;
    margin: 0;
}}

nav {{
    background: #172554;
    color: white;
    padding: 20px;
}}

nav a {{
    color: white;
    float: right;
}}

.container {{
    max-width: 1000px;
    margin: auto;
    padding: 30px;
}}

.box {{
    background: white;
    padding: 25px;
    margin-bottom: 20px;
    border-radius: 10px;
}}

.job {{
    border: 1px solid #ddd;
    padding: 20px;
    margin: 15px 0;
    border-radius: 8px;
}}

input[type=file] {{
    padding: 10px;
    width: 100%;
    box-sizing: border-box;
}}

button {{
    padding: 10px 20px;
    background: #2563eb;
    color: white;
    border: none;
    border-radius: 5px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

td, th {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}}

a {{
    color: #2563eb;
}}

</style>

</head>

<body>

<nav>

<b>Student Dashboard</b>

<a href="/logout">
Logout
</a>

</nav>


<div class="container">


<!-- STUDENT DETAILS -->

<div class="box">

<h2>
Welcome, {student['name']}
</h2>

<p>
Email: {student['email']}
</p>

<p>
Percentage: {student['percentage']}%
</p>

</div>


<!-- RESUME -->

<div class="box">

<h2>My Resume</h2>

<form method="POST"
action="/student/upload-resume"
enctype="multipart/form-data">

<input
type="file"
name="resume"
accept=".pdf,.doc,.docx"
required
>

<br><br>

<button>
Upload Resume
</button>

</form>

<br>

{resume_section}

</div>


<!-- JOBS -->

<div class="box">

<h2>Available Jobs</h2>

{job_html}

</div>


<!-- APPLICATIONS -->

<div class="box">

<h2>My Applications</h2>

<table>

<tr>

<th>Job</th>

<th>Status</th>

</tr>

{application_html}

</table>

</div>


</div>

</body>

</html>

"""


# =====================================================
# RESUME UPLOAD
# =====================================================

@app.route("/student/upload-resume", methods=["POST"])
def upload_resume():

    if "student_id" not in session:

        return redirect("/student/login")

    if "resume" not in request.files:

        return """
        <h2>Please select a resume.</h2>

        <a href="/student/dashboard">
        Back
        </a>
        """

    file = request.files["resume"]

    if file.filename == "":

        return """
        <h2>Please select a resume.</h2>

        <a href="/student/dashboard">
        Back
        </a>
        """

    allowed = [".pdf", ".doc", ".docx"]

    extension = os.path.splitext(
        file.filename
    )[1].lower()

    if extension not in allowed:

        return """
        <h2>
        Only PDF, DOC and DOCX files are allowed.
        </h2>

        <a href="/student/dashboard">
        Back
        </a>
        """

    filename = (
        "student_"
        + str(session["student_id"])
        + extension
    )

    filepath = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    file.save(filepath)

    conn = database()

    conn.execute("""
        UPDATE students
        SET resume=?
        WHERE id=?
    """, (
        filename,
        session["student_id"]
    ))

    conn.commit()

    conn.close()

    return redirect("/student/dashboard")


# =====================================================
# VIEW RESUME
# =====================================================

@app.route("/resume/<filename>")
def view_resume(filename):

    return send_from_directory(
        UPLOAD_FOLDER,
        filename
    )


# =====================================================
# APPLY FOR JOB
# =====================================================

@app.route("/apply/<int:job_id>", methods=["POST"])
def apply_job(job_id):

    if "student_id" not in session:

        return redirect("/student/login")

    conn = database()

    student = conn.execute("""
        SELECT * FROM students
        WHERE id=?
    """, (
        session["student_id"],
    )).fetchone()

    job = conn.execute("""
        SELECT * FROM jobs
        WHERE id=?
    """, (
        job_id,
    )).fetchone()

    if student["percentage"] < job["minimum_percentage"]:

        conn.close()

        return """
        <h2>
        You are not eligible for this job.
        </h2>

        <a href="/student/dashboard">
        Back
        </a>
        """

    existing = conn.execute("""
        SELECT * FROM applications
        WHERE student_id=? AND job_id=?
    """, (
        student["id"],
        job_id
    )).fetchone()

    if existing:

        conn.close()

        return """
        <h2>
        You already applied for this job.
        </h2>

        <a href="/student/dashboard">
        Back to Dashboard
        </a>
        """

    conn.execute("""
        INSERT INTO applications
        (student_id, job_id, status)
        VALUES (?, ?, ?)
    """, (
        student["id"],
        job_id,
        "Applied"
    ))

    conn.commit()

    conn.close()

    return redirect("/student/dashboard")


# =====================================================
# JOBS PAGE
# =====================================================

@app.route("/jobs")
def jobs():

    conn = database()

    jobs = conn.execute("""
        SELECT jobs.*, companies.name AS company_name
        FROM jobs
        JOIN companies
        ON jobs.company_id = companies.id
    """).fetchall()

    conn.close()

    html = """

<!DOCTYPE html>

<html>

<head>

<title>Available Jobs</title>

<style>

body {
    font-family: Arial;
    background: #f2f5f9;
}

.container {
    max-width: 900px;
    margin: auto;
    padding: 40px;
}

.job {
    background: white;
    padding: 25px;
    margin: 20px 0;
    border-radius: 10px;
}

a {
    color: #2563eb;
}

</style>

</head>

<body>

<div class="container">

<h1>Available Jobs</h1>

"""

    for job in jobs:

        html += f"""

        <div class="job">

        <h2>
        {job['title']}
        </h2>

        <p>
        Company: {job['company_name']}
        </p>

        <p>
        {job['description']}
        </p>

        <p>
        Minimum Percentage:
        {job['minimum_percentage']}%
        </p>

        <a href="/student/login">
        Login to Apply
        </a>

        </div>

        """

    html += """

<a href="/">
Back to Home
</a>

</div>

</body>

</html>

"""

    return html


# =====================================================
# COMPANY REGISTRATION
# =====================================================

@app.route("/company/register", methods=["GET", "POST"])
def company_register():

    if request.method == "POST":

        name = request.form["name"]

        email = request.form["email"]

        password = request.form["password"]

        conn = database()

        try:

            conn.execute("""
                INSERT INTO companies
                (name, email, password)
                VALUES (?, ?, ?)
            """, (
                name,
                email,
                password
            ))

            conn.commit()

            conn.close()

            return """
            <h2>
            Company Registration Successful!
            </h2>

            <p>
            Your company account has been created.
            </p>

            <a href="/company/login">
            Login Now
            </a>
            """

        except:

            conn.close()

            return """
            <h2>
            Email already registered.
            </h2>

            <a href="/company/register">
            Try Again
            </a>
            """

    return """

<!DOCTYPE html>

<html>

<head>

<title>Company Registration</title>

<style>

body {
    font-family: Arial;
    background: #f2f5f9;
}

.box {
    background: white;
    width: 400px;
    margin: 70px auto;
    padding: 30px;
    border-radius: 10px;
}

input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    box-sizing: border-box;
}

button {
    width: 100%;
    padding: 12px;
    background: #16a34a;
    color: white;
    border: none;
    border-radius: 5px;
}

a {
    text-decoration: none;
}

</style>

</head>

<body>

<div class="box">

<h2>
Company Registration
</h2>

<form method="POST">

<input
name="name"
placeholder="Company Name"
required
>

<input
type="email"
name="email"
placeholder="Company Email"
required
>

<input
type="password"
name="password"
placeholder="Password"
required
>

<button>
Register Company
</button>

</form>

<br>

<a href="/company/login">
Already registered? Login
</a>

<br><br>

<a href="/">
Back to Home
</a>

</div>

</body>

</html>

"""


# =====================================================
# COMPANY LOGIN
# =====================================================

@app.route("/company/login", methods=["GET", "POST"])
def company_login():

    if request.method == "POST":

        email = request.form["email"]

        password = request.form["password"]

        conn = database()

        company = conn.execute("""
            SELECT * FROM companies
            WHERE email=? AND password=?
        """, (
            email,
            password
        )).fetchone()

        conn.close()

        if company:

            session["company_id"] = company["id"]

            return redirect("/company/dashboard")

        return """
        <h2>
        Invalid company email or password.
        </h2>

        <a href="/company/login">
        Try Again
        </a>
        """

    return """

<!DOCTYPE html>

<html>

<head>

<title>Company Login</title>

<style>

body {
    font-family: Arial;
    background: #f2f5f9;
}

.box {
    background: white;
    width: 400px;
    margin: 80px auto;
    padding: 30px;
    border-radius: 10px;
}

input {
    width: 100%;
    padding: 12px;
    margin: 10px 0;
    box-sizing: border-box;
}

button {
    width: 100%;
    padding: 12px;
    background: #16a34a;
    color: white;
    border: none;
    border-radius: 5px;
}

</style>

</head>

<body>

<div class="box">

<h2>
Company Login
</h2>

<p>

Demo Login:

<br>

Email:
company@gmail.com

<br>

Password:
1234

</p>

<form method="POST">

<input
type="email"
name="email"
placeholder="Email"
required
>

<input
type="password"
name="password"
placeholder="Password"
required
>

<button>
Login
</button>

</form>

<br>

<a href="/company/register">
Create New Company Account
</a>

<br><br>

<a href="/">
Back to Home
</a>

</div>

</body>

</html>

"""


# =====================================================
# COMPANY DASHBOARD
# =====================================================

@app.route("/company/dashboard")
def company_dashboard():

    if "company_id" not in session:

        return redirect("/company/login")

    conn = database()

    company = conn.execute("""
        SELECT * FROM companies
        WHERE id=?
    """, (
        session["company_id"],
    )).fetchone()

    jobs = conn.execute("""
        SELECT * FROM jobs
        WHERE company_id=?
    """, (
        company["id"],
    )).fetchall()

    applications = conn.execute("""
        SELECT
        applications.*,
        students.name AS student_name,
        students.email,
        students.percentage,
        students.resume,
        jobs.title

        FROM applications

        JOIN students
        ON applications.student_id = students.id

        JOIN jobs
        ON applications.job_id = jobs.id

        WHERE jobs.company_id=?
    """, (
        company["id"],
    )).fetchall()

    conn.close()


    # COMPANY JOBS

    jobs_html = ""

    for job in jobs:

        jobs_html += f"""

        <li>

        {job['title']}

        -

        Minimum Percentage:
        {job['minimum_percentage']}%

        </li>

        """


    # STUDENT APPLICATIONS

    applications_html = ""

    for application in applications:

        if application["resume"]:

            resume_link = f"""
            <a href="/resume/{application['resume']}"
            target="_blank">
            View Resume
            </a>
            """

        else:

            resume_link = "Not Uploaded"


        applications_html += f"""

        <tr>

        <td>
        {application['student_name']}
        </td>

        <td>
        {application['email']}
        </td>

        <td>
        {application['percentage']}%
        </td>

        <td>
        {application['title']}
        </td>

        <td>
        {resume_link}
        </td>

        <td>
        {application['status']}
        </td>

        </tr>

        """


    return f"""

<!DOCTYPE html>

<html>

<head>

<title>Company Dashboard</title>

<style>

body {{
    font-family: Arial;
    background: #f2f5f9;
    margin: 0;
}}

nav {{
    background: #172554;
    color: white;
    padding: 20px;
}}

nav a {{
    color: white;
    float: right;
}}

.container {{
    max-width: 1100px;
    margin: auto;
    padding: 30px;
}}

.box {{
    background: white;
    padding: 25px;
    margin-bottom: 20px;
    border-radius: 10px;
}}

input, textarea {{
    width: 100%;
    padding: 10px;
    margin: 8px 0;
    box-sizing: border-box;
}}

button {{
    padding: 10px 20px;
    background: #16a34a;
    color: white;
    border: none;
    border-radius: 5px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
}}

td, th {{
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: left;
}}

a {{
    color: #2563eb;
}}

</style>

</head>

<body>

<nav>

<b>
Company Dashboard
</b>

<a href="/logout">
Logout
</a>

</nav>


<div class="container">


<!-- COMPANY INFORMATION -->

<div class="box">

<h2>
Welcome {company['name']}
</h2>

<p>
Email: {company['email']}
</p>

</div>


<!-- POST JOB -->

<div class="box">

<h2>
Post New Job
</h2>

<form method="POST"
action="/company/add-job">

<input
name="title"
placeholder="Job Title"
required
>

<textarea
name="description"
placeholder="Job Description"
required
></textarea>

<input
type="number"
name="percentage"
placeholder="Minimum Percentage"
min="0"
max="100"
required
>

<button>
Post Job
</button>

</form>

</div>


<!-- MY JOBS -->

<div class="box">

<h2>
My Jobs
</h2>

<ul>

{jobs_html}

</ul>

</div>


<!-- STUDENT APPLICATIONS -->

<div class="box">

<h2>
Student Applications
</h2>

<table>

<tr>

<th>
Student
</th>

<th>
Email
</th>

<th>
Percentage
</th>

<th>
Job
</th>

<th>
Resume
</th>

<th>
Status
</th>

</tr>

{applications_html}

</table>

</div>


</div>

</body>

</html>

"""


# =====================================================
# COMPANY ADD JOB
# =====================================================

@app.route("/company/add-job", methods=["POST"])
def add_job():

    if "company_id" not in session:

        return redirect("/company/login")

    title = request.form["title"]

    description = request.form["description"]

    percentage = request.form["percentage"]

    conn = database()

    conn.execute("""
        INSERT INTO jobs
        (company_id, title, description, minimum_percentage)
        VALUES (?, ?, ?, ?)
    """, (
        session["company_id"],
        title,
        description,
        percentage
    ))

    conn.commit()

    conn.close()

    return redirect("/company/dashboard")


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")


# =====================================================
# START APPLICATION
# =====================================================

if __name__ == "__main__":

    create_database()

    app.run(host="0.0.0.0", port=5000, debug=True)