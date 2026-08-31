# second

# =====================================
# SMARTDESK APPLICATION
# app.py PART 1
# =====================================


from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

from db import conn,get_connection

from functools import wraps



# =====================================
# APP CONFIGURATION
# =====================================

app = Flask(__name__)

app.config["SECRET_KEY"] = "smartdesk123"



# =====================================
# LOGIN DECORATOR
# =====================================

def login_required(function):

    @wraps(function)

    def wrapper(*args, **kwargs):

        if "employee_id" not in session:

            flash("Please login first", "warning")

            return redirect(url_for("employee_login"))

        return function(*args, **kwargs)

    return wrapper





# =====================================
# HOME
# =====================================


@app.route("/")
def home():

    return render_template("index.html")





# =====================================
# LOGIN PAGE
# =====================================


@app.route("/login")
def login():

    return render_template("login.html")





# =====================================
# EMPLOYEE LOGIN
# =====================================


@app.route("/employee_login", methods=["GET","POST"])
def employee_login():


    if request.method == "POST":


        email = request.form["email"]

        password = request.form["password"]



        cursor = conn.cursor(dictionary=True)


        cursor.execute(
            """
            SELECT *
            FROM employees
            WHERE email=%s
            AND password=%s
            """,
            (
                email,
                password
            )
        )


        employee = cursor.fetchone()


        cursor.close()



        if employee:


            session["employee_id"] = employee["employee_id"]

            session["employee_name"] = employee["name"]


            flash(
                "Login Successful",
                "success"
            )


            return redirect(
                url_for("employee_dashboard")
            )


        else:


            flash(
                "Invalid Email or Password",
                "danger"
            )


    return render_template(
        "employee_login.html"
    )







# =====================================
# ADMIN LOGIN
# =====================================


@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT *
            FROM admins
            WHERE username=%s
            AND password=%s
        """, (username, password))

        admin = cursor.fetchone()

        cursor.close()

        if admin:

            session["admin_id"] = admin["id"]
            session["admin_name"] = admin["name"]

            flash("Login Successful", "success")

            return redirect(url_for("admin_dashboard"))

        else:

            flash("Invalid Admin Credentials", "danger")

    return render_template("admin_login.html")





# =====================================
# ADMIN DASHBOARD
# =====================================

@app.route("/admin_dashboard")
def admin_dashboard():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    connection = get_connection()

    if not connection:
        return "Database connection failed"

    cursor = connection.cursor(dictionary=True)

    # -------------------------------------
    # TOTAL EMPLOYEES
    # -------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM employees
    """)

    total_employees = cursor.fetchone()["total"]


    # -------------------------------------
    # PRESENT TODAY
    # -------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance
        WHERE attendance_date = CURDATE()
        AND status = 'Present'
    """)

    present_today = cursor.fetchone()["total"]


    # -------------------------------------
    # PENDING LEAVE REQUESTS
    # -------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM leave_requests
        WHERE status = 'Pending'
    """)

    pending_leave = cursor.fetchone()["total"]


    # -------------------------------------
    # PENDING TASKS
    # -------------------------------------

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tasks
        WHERE status != 'Completed'
    """)

    pending_tasks = cursor.fetchone()["total"]


    # -------------------------------------
    # EMPLOYEE RECORDS
    # -------------------------------------

    cursor.execute("""
        SELECT
            id,
            employee_id,
            name,
            department,
            designation
        FROM employees
        ORDER BY name ASC
    """)

    employees = cursor.fetchall()


    # -------------------------------------
    # DEPARTMENTS FROM ACTUAL EMPLOYEE DATA
    # -------------------------------------

    cursor.execute("""
        SELECT
            department,
            COUNT(*) AS employee_count
        FROM employees
        WHERE department IS NOT NULL
        AND department != ''
        GROUP BY department
        ORDER BY department ASC
    """)

    departments = cursor.fetchall()


    # -------------------------------------
    # RECENT TASKS
    # -------------------------------------

    cursor.execute("""
        SELECT
            id,
            employee_id,
            title,
            priority,
            status,
            due_date
        FROM tasks
        ORDER BY id DESC
        LIMIT 5
    """)

    tasks = cursor.fetchall()


    cursor.close()


    return render_template(
        "admin_dashboard.html",

        total_employees=total_employees,

        present_today=present_today,

        pending_leave=pending_leave,

        pending_tasks=pending_tasks,

        employees=employees,

        departments=departments,

        tasks=tasks,

        reports=[],

        admin_name=session.get("admin_name", "Admin")
    )


@app.route("/employees")
def employees():

    cursor = conn.cursor(dictionary=True)

    # Employee List
    cursor.execute("""
        SELECT *
        FROM employees
        ORDER BY id DESC
    """)
    employees = cursor.fetchall()

    # Total Employees
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM employees
    """)
    total_employees = cursor.fetchone()["total"]

    # Active Employees
    total_active = total_employees

    # Employees On Leave
    cursor.execute("""
        SELECT COUNT(DISTINCT employee_id) AS total
        FROM leave_requests
        WHERE status='Pending'
    """)
    leave_count = cursor.fetchone()["total"]

    # New Employees (Current Month)
    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM employees
        WHERE MONTH(joining_date)=MONTH(CURDATE())
        AND YEAR(joining_date)=YEAR(CURDATE())
    """)
    new_employees = cursor.fetchone()["total"]

    cursor.close()

    return render_template(
        "employees.html",
        employees=employees,
        total_employees=total_employees,
        active_employees=total_active,
        leave_count=leave_count,
        new_employees=new_employees
    )




# =====================================
# ADD EMPLOYEE
# =====================================

@app.route("/add_employee", methods=["POST"])
def add_employee():

    employee_id = request.form["employee_id"]
    name = request.form["name"]
    email = request.form["email"]
    password = request.form["password"]
    phone = request.form["phone"]
    department = request.form["department"]
    designation = request.form["designation"]

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO employees
        (
            employee_id,
            name,
            email,
            password,
            phone,
            department,
            designation
        )

        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s
        )
    """,(
        employee_id,
        name,
        email,
        password,
        phone,
        department,
        designation
    ))

    conn.commit()

    cursor.close()

    flash("Employee Added Successfully","success")

    return redirect(url_for("employees"))


@app.route("/edit_employee/<int:id>", methods=["GET","POST"])
def edit_employee(id):

    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        employee_id = request.form["employee_id"]
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        department = request.form["department"]
        designation = request.form["designation"]
        joining_date = request.form["joining_date"]

        cursor.execute("""
            UPDATE employees

            SET

            employee_id=%s,
            name=%s,
            email=%s,
            phone=%s,
            department=%s,
            designation=%s,
            joining_date=%s

            WHERE id=%s
        """,(
            employee_id,
            name,
            email,
            phone,
            department,
            designation,
            joining_date,
            id
        ))

        conn.commit()

        cursor.close()

        flash("Employee Updated Successfully","success")

        return redirect(url_for("employees"))

    cursor.execute("""
        SELECT *
        FROM employees
        WHERE id=%s
    """,(id,))

    employee = cursor.fetchone()

    cursor.close()

    return render_template(
        "edit_employee.html",
        employee=employee
    )



# =====================================
# DELETE employee
# =====================================

@app.route("/delete_employee/<int:id>")
def delete_employee(id):

    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT employee_id FROM employees WHERE id=%s",
            (id,)
        )

        employee = cursor.fetchone()

        if employee:
            employee_id = employee[0]

            cursor.execute(
                "DELETE FROM attendance WHERE employee_id=%s",
                (employee_id,)
            )

            cursor.execute(
                "DELETE FROM employees WHERE id=%s",
                (id,)
            )

            conn.commit()

            flash("Employee Deleted Successfully", "success")

        else:
            flash("Employee not found", "danger")

    except Exception as e:
        conn.rollback()
        print("Delete Error:", e)
        flash("Employee could not be deleted", "danger")

    finally:
        cursor.close()

    return redirect(url_for("employees"))


# =====================================
# LOGOUT
# =====================================


@app.route("/logout")
def logout():


    session.clear()


    # flash(
    #     "Logged out successfully",
    #     "login"
    # )


    return redirect(
        url_for("home")
    )


# =====================================
# EMPLOYEE DASHBOARD
# =====================================

@app.route("/employee_dashboard")
@login_required
def employee_dashboard():

    employee_id = session["employee_id"]

    cursor = conn.cursor(dictionary=True)

    # =====================================
    # EMPLOYEE DETAILS
    # =====================================

    cursor.execute("""
        SELECT
            employee_id,
            name,
            department,
            designation,
            joining_date,
            profile_image
        FROM employees
        WHERE employee_id=%s
    """, (employee_id,))

    employee = cursor.fetchone()


# =====================================
# TODAY'S TASKS
# =====================================

    cursor.execute("""
        SELECT
            id,
            employee_id,
            title,
            description,
            priority,
            status,
            due_date,
            assigned_by,
            created_at,
            completed_on
        FROM tasks
        WHERE employee_id=%s
        AND DATE(due_date)=CURDATE()
        ORDER BY due_date ASC
    """, (employee_id,))

    today_tasks = cursor.fetchall()


    # =====================================
    # TODAY'S ATTENDANCE
    # =====================================

    cursor.execute("""
        SELECT
            status,
            TIME_FORMAT(check_in, '%h:%i %p') AS check_in,
            TIME_FORMAT(check_out, '%h:%i %p') AS check_out,
            working_hours
        FROM attendance
        WHERE employee_id=%s
        AND attendance_date=CURDATE()
    """, (employee_id,))

    attendance = cursor.fetchone()

    if attendance is None:
        attendance = {
            "status": "Not Marked",
            "check_in": "-",
            "check_out": "-",
            "working_hours": "-"
        }


    # =====================================
    # PENDING TASKS COUNT
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tasks
        WHERE employee_id=%s
        AND status != 'Completed'
    """, (employee_id,))

    pending_tasks = cursor.fetchone()["total"]


    # =====================================
    # PENDING LEAVE REQUESTS
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM leave_requests
        WHERE employee_id=%s
        AND status='Pending'
    """, (employee_id,))

    pending_leave = cursor.fetchone()["total"]


    # =====================================
    # REPORTS COUNT
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM task_reports
        WHERE employee_id=%s
        AND MONTH(submitted_on)=MONTH(CURDATE())
        AND YEAR(submitted_on)=YEAR(CURDATE())
    """, (employee_id,))

    reports_count = cursor.fetchone()["total"]


    # =====================================
    # TODAY'S TASKS
    # =====================================

    cursor.execute("""
        SELECT
            id,
            title,
            due_date,
            status
        FROM tasks
        WHERE employee_id=%s
        AND due_date=CURDATE()
        ORDER BY id DESC
        LIMIT 4
    """, (employee_id,))

    today_tasks = cursor.fetchall()


    # =====================================
    # RECENT REPORTS
    # =====================================

    cursor.execute("""
        SELECT
            tr.id,
            tr.submitted_on,
            tr.status,
            t.title
        FROM task_reports tr
        LEFT JOIN tasks t
            ON tr.task_id=t.id
        WHERE tr.employee_id=%s
        ORDER BY tr.submitted_on DESC
        LIMIT 3
    """, (employee_id,))

    recent_reports = cursor.fetchall()


    # =====================================
    # MONTHLY ATTENDANCE
    # =====================================

    cursor.execute("""
        SELECT
            COUNT(*) AS total_days,
            SUM(CASE WHEN status='Present' THEN 1 ELSE 0 END) AS present_days
        FROM attendance
        WHERE employee_id=%s
        AND MONTH(attendance_date)=MONTH(CURDATE())
        AND YEAR(attendance_date)=YEAR(CURDATE())
    """, (employee_id,))

    monthly_attendance = cursor.fetchone()

    total_attendance_days = monthly_attendance["total_days"] or 0
    present_days = monthly_attendance["present_days"] or 0

    if total_attendance_days > 0:
        attendance_percentage = round(
            (present_days / total_attendance_days) * 100
        )
    else:
        attendance_percentage = 0


    # =====================================
    # COMPLETED TASKS THIS MONTH
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tasks
        WHERE employee_id=%s
        AND status='Completed'
        AND (
            completed_on IS NOT NULL
            AND MONTH(completed_on)=MONTH(CURDATE())
            AND YEAR(completed_on)=YEAR(CURDATE())
        )
    """, (employee_id,))

    completed_tasks = cursor.fetchone()["total"]


    # =====================================
    # REPORTS SUBMITTED THIS MONTH
    # =====================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM task_reports
        WHERE employee_id=%s
        AND MONTH(submitted_on)=MONTH(CURDATE())
        AND YEAR(submitted_on)=YEAR(CURDATE())
    """, (employee_id,))

    monthly_reports = cursor.fetchone()["total"]


    # =====================================
    # APPROVED LEAVES THIS MONTH
    # =====================================

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(
                    DATEDIFF(
                        LEAST(to_date, LAST_DAY(CURDATE())),
                        GREATEST(from_date, DATE_FORMAT(CURDATE(), '%Y-%m-01'))
                    ) + 1
                ),
                0
            ) AS total
        FROM leave_requests
        WHERE employee_id=%s
        AND status='Approved'
        AND from_date <= LAST_DAY(CURDATE())
        AND to_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
    """, (employee_id,))

    leaves_taken = cursor.fetchone()["total"]


    cursor.close()


    # =====================================
    # RENDER DASHBOARD
    # =====================================

    return render_template(
        "employee_dashboard.html",

        employee=employee,

        attendance=attendance,

        pending_tasks=pending_tasks,

        pending_leave=pending_leave,

        reports_count=reports_count,

        today_tasks=today_tasks,

        recent_reports=recent_reports,

        present_days=present_days,

        completed_tasks=completed_tasks,

        monthly_reports=monthly_reports,

        leaves_taken=leaves_taken,

        attendance_percentage=attendance_percentage,

        unread_notifications=3,

        last_login="Today"
    )



# =====================================
# EMPLOYEE ATTENDANCE
# =====================================


@app.route("/employee_attendance")
@login_required
def employee_attendance():


    employee_id = session["employee_id"]


    cursor = conn.cursor(dictionary=True)




    # Employee Details

    cursor.execute(
        """
        SELECT
        employee_id,
        name,
        department,
        designation

        FROM employees

        WHERE employee_id=%s

        """,
        (employee_id,)
    )


    employee = cursor.fetchone()





    # Attendance History

    cursor.execute(
        """
        SELECT

        attendance_date,

        check_in,

        check_out,

        working_hours,

        status


        FROM attendance


        WHERE employee_id=%s


        ORDER BY attendance_date DESC

        """,
        (employee_id,)
    )


    attendance_list = cursor.fetchall()





    # Today's Attendance

    cursor.execute(
        """
        SELECT *

        FROM attendance

        WHERE employee_id=%s

        AND attendance_date=CURDATE()

        """,
        (employee_id,)
    )


    attendance_today = cursor.fetchone()



    cursor.close()



    return render_template(

        "employee_attendance.html",

        employee=employee,

        attendance_list=attendance_list,

        attendance_today=attendance_today

    )









# =====================================
# MARK ATTENDANCE
# =====================================


@app.route("/mark_attendance", methods=["POST"])
@login_required
def mark_attendance():


    employee_id = session["employee_id"]


    cursor = conn.cursor(dictionary=True)



    # Check today's attendance

    cursor.execute(
        """
        SELECT *

        FROM attendance

        WHERE employee_id=%s

        AND attendance_date=CURDATE()

        """,
        (employee_id,)
    )


    attendance = cursor.fetchone()





    # CHECK IN

    if attendance is None:



        cursor.execute(
            """
            INSERT INTO attendance
            (
            employee_id,
            attendance_date,
            check_in,
            status
            )

            VALUES
            (
            %s,
            CURDATE(),
            CURTIME(),
            'Present'
            )

            """,
            (employee_id,)
        )



        flash(
            "Check-in marked successfully",
            "success"
        )





    # CHECK OUT

    elif attendance["check_out"] is None:



        cursor.execute(
            """
            UPDATE attendance

            SET

            check_out=CURTIME(),

            working_hours=
            TIMEDIFF(
            CURTIME(),
            check_in
            )


            WHERE employee_id=%s

            AND attendance_date=CURDATE()

            """,
            (employee_id,)
        )



        flash(
            "Check-out marked successfully",
            "success"
        )





    else:


        flash(
            "Today's attendance already completed",
            "warning"
        )



    conn.commit()

    cursor.close()



    return redirect(
        url_for("employee_attendance")
    )









# =====================================
# EMPLOYEE LEAVE PAGE
# =====================================


@app.route("/employee_leave")
@login_required
def employee_leave():


    employee_id=session["employee_id"]


    cursor=conn.cursor(dictionary=True)




    cursor.execute(
        """
        SELECT

        employee_id,

        name

        FROM employees

        WHERE employee_id=%s

        """,
        (employee_id,)
    )


    employee=cursor.fetchone()





    cursor.execute(
        """
        SELECT

        id,

        leave_type,

        from_date,

        to_date,

        reason,

        status,

        applied_on


        FROM leave_requests


        WHERE employee_id=%s


        ORDER BY applied_on DESC

        """,
        (employee_id,)
    )


    leave_list=cursor.fetchall()



    cursor.close()



    return render_template(

        "employee_leave.html",

        employee=employee,

        leave_list=leave_list

    )









# =====================================
# APPLY LEAVE
# =====================================


@app.route("/apply_leave", methods=["POST"])
@login_required
def apply_leave():


    employee_id=session["employee_id"]



    leave_type=request.form["leave_type"]

    from_date=request.form["from_date"]

    to_date=request.form["to_date"]

    reason=request.form["reason"]



    cursor=conn.cursor()



    cursor.execute(
        """
        INSERT INTO leave_requests

        (
        employee_id,
        leave_type,
        from_date,
        to_date,
        reason,
        status
        )


        VALUES

        (%s,%s,%s,%s,%s,%s)

        """,

        (

        employee_id,

        leave_type,

        from_date,

        to_date,

        reason,

        "Pending"

        )
    )



    conn.commit()


    cursor.close()



    flash(
        "Leave applied successfully!", "leave"
    )



    return redirect(
        url_for("employee_leave")
    )

# =====================================
# EMPLOYEE TASKS
# =====================================


@app.route("/employee_tasks")
@login_required
def employee_tasks():


    employee_id = session["employee_id"]


    cursor = conn.cursor(dictionary=True)



    # Employee Details

    cursor.execute(
        """
        SELECT

        employee_id,
        name

        FROM employees

        WHERE employee_id=%s

        """,
        (employee_id,)
    )


    employee = cursor.fetchone()





    # Assigned Tasks

    cursor.execute(
        """
        SELECT *

        FROM tasks

        WHERE employee_id=%s

        ORDER BY due_date ASC

        """,
        (employee_id,)
    )


    tasks = cursor.fetchall()






    # Task Report History

    cursor.execute(
        """
        SELECT

        tr.*,

        t.title


        FROM task_reports tr


        JOIN tasks t

        ON tr.task_id=t.id


        WHERE tr.employee_id=%s


        ORDER BY tr.submitted_on DESC

        """,
        (employee_id,)
    )


    task_reports = cursor.fetchall()



    cursor.close()



    return render_template(

        "employee_tasks.html",

        employee=employee,

        tasks=tasks,

        task_reports=task_reports

    )




# =====================================
# UPDATE TASK STATUS
# =====================================


@app.route(
    "/update_task_status/<int:task_id>",
    methods=["POST"]
)

@login_required

def update_task_status(task_id):


    status=request.form["status"]


    cursor=conn.cursor()



    if status=="Completed":


        cursor.execute(
            """
            UPDATE tasks

            SET

            status=%s,

            completed_on=CURDATE()


            WHERE id=%s

            """,
            (
                status,
                task_id
            )
        )



    else:


        cursor.execute(
            """
            UPDATE tasks

            SET status=%s


            WHERE id=%s

            """,
            (
                status,
                task_id
            )
        )



    conn.commit()

    cursor.close()



    flash(
        "Task status updated",
        "success"
    )


    return redirect(
        url_for("employee_tasks")
    )









# =====================================
# EMPLOYEE REPORTS PAGE
# =====================================


@app.route("/employee_reports")
@login_required
def employee_reports():


    employee_id=session["employee_id"]


    cursor=conn.cursor(dictionary=True)



    # Employee

    cursor.execute(
        """
        SELECT

        employee_id,
        name,
        department,
        designation


        FROM employees


        WHERE employee_id=%s

        """,
        (employee_id,)
    )


    employee=cursor.fetchone()





    # Tasks for dropdown

    cursor.execute(
        """
        SELECT

        id,

        title


        FROM tasks


        WHERE employee_id=%s


        ORDER BY due_date ASC

        """,
        (employee_id,)
    )


    tasks=cursor.fetchall()





    # Weekly Reports History

    cursor.execute(
        """
        SELECT *


        FROM weekly_reports


        WHERE employee_id=%s


        ORDER BY submitted_on DESC

        """,
        (employee_id,)
    )


    weekly_reports=cursor.fetchall()



    cursor.close()



    return render_template(

        "employee_reports.html",

        employee=employee,

        tasks=tasks,

        weekly_reports=weekly_reports

    )









# =====================================
# SUBMIT TASK REPORT
# =====================================


@app.route(
    "/submit_task_report",
    methods=["POST"]
)

@login_required

def submit_task_report():


    employee_id=session["employee_id"]



    task_id=request.form["task_id"]

    work_done=request.form["work_done"]

    hours=request.form["hours"]



    cursor=conn.cursor()



    cursor.execute(
        """
        INSERT INTO task_reports

        (
        employee_id,
        task_id,
        work_done,
        hours_worked
        )


        VALUES

        (%s,%s,%s,%s)

        """,

        (

        employee_id,

        task_id,

        work_done,

        hours

        )

    )



    conn.commit()

    cursor.close()



    flash(
        "Task report submitted successfully!",
        "success"
    )


    return redirect(
        url_for("employee_reports")
    )









# =====================================
# SUBMIT WEEKLY REPORT
# =====================================


@app.route(
    "/submit_weekly_report",
    methods=["POST"]
)

@login_required

def submit_weekly_report():


    employee_id=session["employee_id"]



    week_start=request.form["week_start"]

    week_end=request.form["week_end"]

    work_summary=request.form["work_summary"]



    cursor=conn.cursor()



    cursor.execute(
        """
        INSERT INTO weekly_reports

        (
        employee_id,
        week_start,
        week_end,
        work_summary,
        status
        )


        VALUES

        (%s,%s,%s,%s,%s)

        """,

        (

        employee_id,

        week_start,

        week_end,

        work_summary,

        "Pending"

        )

    )



    conn.commit()

    cursor.close()



    flash(
        "Weekly report submitted successfully!",
        "success"
    )



    return redirect(
        url_for("employee_reports")
    )









# =====================================
# VIEW TASK REPORT
# =====================================


@app.route(
    "/view_task_report/<int:report_id>"
)

@login_required

def view_task_report(report_id):


    employee_id=session["employee_id"]



    cursor=conn.cursor(dictionary=True)



    cursor.execute(
        """
        SELECT

        tr.*,

        t.title


        FROM task_reports tr


        JOIN tasks t

        ON tr.task_id=t.id


        WHERE tr.id=%s

        AND tr.employee_id=%s

        """,

        (
            report_id,

            employee_id
        )
    )


    report=cursor.fetchone()



    cursor.close()



    if not report:


        flash(
            "Report not found",
            "danger"
        )


        return redirect(
            url_for("employee_reports")
        )



    return render_template(

        "view_task_report.html",

        report=report

    )

# =====================================
# VIEW WEEKLY REPORT
# =====================================


@app.route(
    "/view_weekly_report/<int:report_id>"
)

@login_required

def view_weekly_report(report_id):


    employee_id=session["employee_id"]



    cursor=conn.cursor(dictionary=True)



    cursor.execute(
        """
        SELECT *


        FROM weekly_reports


        WHERE id=%s

        AND employee_id=%s

        """,

        (
            report_id,

            employee_id
        )
    )


    report=cursor.fetchone()



    cursor.close()



    if not report:


        flash(
            "Report not found",
            "danger"
        )


        return redirect(
            url_for("employee_reports")
        )



    return render_template(

        "view_weekly_report.html",

        report=report

    )


# =====================================
# ADMIN ATTENDANCE
# =====================================

@app.route("/admin_attendance")
def admin_attendance():

    if "admin_id" not in session:

        return redirect(url_for("admin_login"))

    cursor = conn.cursor(dictionary=True)

    # Attendance Records

    cursor.execute("""

        SELECT

        a.id,

        e.employee_id,

        e.name,

        e.email,

        e.department,

        a.attendance_date,

        TIME_FORMAT(a.check_in,'%H:%i') AS check_in,

        TIME_FORMAT(a.check_out,'%H:%i') AS check_out,

        a.working_hours,

        a.status

        FROM attendance a

        JOIN employees e

        ON a.employee_id = e.employee_id

        ORDER BY a.attendance_date DESC

    """)

    records = cursor.fetchall()


    # Employee Dropdown

    cursor.execute("""

        SELECT

        employee_id,

        name

        FROM employees

        ORDER BY name

    """)

    employees = cursor.fetchall()


    cursor.close()

    return render_template(

        "admin_attendance.html",

        admin_name=session["admin_name"],

        records=records,

        employees=employees,

        monthly_records=[],

        report=None

    )


# =====================================
# MONTHLY ATTENDANCE REPORT API
# =====================================

@app.route("/monthly_attendance_report")
def monthly_attendance_report():

    if "admin_id" not in session:
        return jsonify({
            "success": False,
            "message": "Unauthorized"
        }), 401

    employee_id = request.args.get("employee_id")
    month = request.args.get("month")

    if not employee_id or not month:
        return jsonify({
            "success": False,
            "message": "Employee and month are required."
        }), 400

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            a.attendance_date,
            TIME_FORMAT(a.check_in, '%H:%i') AS check_in,
            TIME_FORMAT(a.check_out, '%H:%i') AS check_out,
            a.working_hours,
            a.status
        FROM attendance a
        WHERE a.employee_id = %s
        AND DATE_FORMAT(a.attendance_date, '%Y-%m') = %s
        ORDER BY a.attendance_date ASC
    """, (employee_id, month))

    records = cursor.fetchall()

    cursor.close()

    total_days = len(records)

    present_days = sum(
        1 for row in records
        if row["status"] == "Present"
    )

    absent_days = sum(
        1 for row in records
        if row["status"] == "Absent"
    )

    leave_days = sum(
        1 for row in records
        if row["status"] == "Leave"
    )

    return jsonify({
        "success": True,
        "total_days": total_days,
        "present": present_days,
        "absent": absent_days,
        "leave": leave_days,
        "records": records
    })


# =====================================
# ADMIN LEAVE MANAGEMENT
# =====================================

@app.route("/admin_leave")
def admin_leave():

    if "admin_id" not in session:

        return redirect(url_for("admin_login"))


    cursor = conn.cursor(dictionary=True)


    # All Leave Requests

    cursor.execute("""
        SELECT

        lr.id,

        e.employee_id,

        e.name,

        e.department,

        lr.leave_type,

        lr.from_date,

        lr.to_date,

        lr.reason,

        lr.status,

        lr.applied_on


        FROM leave_requests lr


        JOIN employees e

        ON lr.employee_id = e.employee_id


        ORDER BY lr.applied_on DESC

    """)


    leave_requests = cursor.fetchall()



    # Pending Count

    cursor.execute("""
        SELECT COUNT(*) AS total

        FROM leave_requests

        WHERE status='Pending'
    """)


    pending = cursor.fetchone()["total"]



    # Approved Count

    cursor.execute("""
        SELECT COUNT(*) AS total

        FROM leave_requests

        WHERE status='Approved'
    """)


    approved = cursor.fetchone()["total"]



    # Rejected Count

    cursor.execute("""
        SELECT COUNT(*) AS total

        FROM leave_requests

        WHERE status='Rejected'
    """)


    rejected = cursor.fetchone()["total"]



    cursor.close()



    return render_template(

        "admin_leave.html",

        leave_requests=leave_requests,

        pending=pending,

        approved=approved,

        rejected=rejected,

        admin_name=session["admin_name"]

    )


# =====================================
# APPROVE LEAVE
# =====================================

@app.route("/approve_leave/<int:id>")
def approve_leave(id):

    if "admin_id" not in session:

        return redirect(url_for("admin_login"))


    cursor = conn.cursor()


    cursor.execute("""
        UPDATE leave_requests

        SET status='Approved'

        WHERE id=%s

    """,(id,))


    conn.commit()

    cursor.close()


    flash(
        "Leave request approved successfully",
        "success"
    )


    return redirect(
        url_for("admin_leave")
    )
# =====================================
# REJECT LEAVE
# =====================================

@app.route("/reject_leave/<int:id>")
def reject_leave(id):

    if "admin_id" not in session:

        return redirect(url_for("admin_login"))


    cursor = conn.cursor()
    cursor.execute("""
        UPDATE leave_requests

        SET status='Rejected'

        WHERE id=%s

    """,(id,))


    conn.commit()
    cursor.close()

    flash(
        "Leave request rejected",
        "danger"
    )


    return redirect(
        url_for("admin_leave")
    )

# =====================================
# Admin Tasks
# =====================================

@app.route("/admin_tasks")
def admin_tasks():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))


    cursor = conn.cursor(dictionary=True)


    cursor.execute("""
        SELECT

        t.*,

        e.name AS employee_name

        FROM tasks t

        JOIN employees e

        ON t.employee_id=e.employee_id

        ORDER BY t.created_at DESC

    """)


    tasks = cursor.fetchall()


    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tasks
    """)
    total = cursor.fetchone()["total"]


    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tasks
        WHERE status='Pending'
    """)
    pending = cursor.fetchone()["total"]


    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tasks
        WHERE status='In Progress'
    """)
    progress = cursor.fetchone()["total"]


    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM tasks
        WHERE status='Completed'
    """)
    completed = cursor.fetchone()["total"]


    cursor.close()


    return render_template(
        "admin_tasks.html",
        tasks=tasks,
        pending_tasks=pending,
        progress_tasks=progress,
        completed_tasks=completed
    )

#=========================================
# Add Task
# ========================================

@app.route("/add_task", methods=["POST"])
def add_task():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))


    employee_id=request.form["employee_id"]
    title=request.form["title"]
    description=request.form["description"]
    priority=request.form["priority"]
    due_date=request.form["due_date"]


    cursor=conn.cursor()


    cursor.execute("""
        INSERT INTO tasks
        (
        employee_id,
        title,
        description,
        priority,
        status,
        due_date,
        assigned_by
        )

        VALUES
        (%s,%s,%s,%s,%s,%s,%s)

    """,
    (
        employee_id,
        title,
        description,
        priority,
        "Pending",
        due_date,
        session["admin_name"]
    ))


    conn.commit()

    cursor.close()


    flash(
        "Task assigned successfully",
        "success"
    )


    return redirect(
        url_for("admin_tasks")
    )

# =====================================
# Delete Yask
# =====================================

@app.route("/delete_task/<int:id>")
def delete_task(id):
    cursor = conn.cursor()
    cursor.execute(""" DELETE FROM tasks WHERE id=%s""",(id,))
    conn.commit()
    cursor.close()
    flash("Task Deleted Successfully","success")
    return redirect(url_for("admin_tasks"))

# =====================================
# Admin Reports
# =====================================

@app.route("/admin_reports")
def admin_reports():

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            tr.*,
            e.name,
            t.title
        FROM task_reports tr
        JOIN employees e
            ON tr.employee_id = e.employee_id
        JOIN tasks t
            ON tr.task_id = t.id
        ORDER BY tr.submitted_on DESC
    """)
    task_reports = cursor.fetchall()

    cursor.execute("""
        SELECT
            wr.*,
            e.name
        FROM weekly_reports wr
        JOIN employees e
            ON wr.employee_id = e.employee_id
        ORDER BY wr.submitted_on DESC
    """)
    weekly_reports = cursor.fetchall()

    cursor.close()

    return render_template(
        "admin_reports.html",
        task_reports=task_reports,
        weekly_reports=weekly_reports
    )

# =======================================
# Approve weekly report
# =======================================
@app.route("/approve_weekly_report/<int:id>")
def approve_weekly_report(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE weekly_reports
        SET status='Approved'
        WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()

    flash("Weekly Report Approved", "success")

    return redirect(url_for("admin_reports"))

# =========================================
# reject weekly report
# =========================================
    
@app.route("/reject_weekly_report/<int:id>")
def reject_weekly_report(id):

    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    cursor = conn.cursor()

    cursor.execute("""
        UPDATE weekly_reports
        SET status='Rejected'
        WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()

    flash("Weekly Report Rejected", "warning")

    return redirect(url_for("admin_reports"))

# =====================================
# PROFILE
# =====================================


@app.route("/employee_profile")
@login_required
def employee_profile():


    employee_id=session["employee_id"]


    cursor=conn.cursor(dictionary=True)



    cursor.execute(
        """
        SELECT *

        FROM employees

        WHERE employee_id=%s

        """,
        (employee_id,)
    )


    employee=cursor.fetchone()



    cursor.close()



    return render_template(

        "employee_profile.html",

        employee=employee

    )


# =====================================
# CHANGE PASSWORD
# =====================================

@app.route("/change_password", methods=["POST"])
@login_required
def change_password():

    employee_id = session["employee_id"]

    current_password = request.form["current_password"]
    new_password = request.form["new_password"]
    confirm_password = request.form["confirm_password"]

    if new_password != confirm_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for("employee_profile"))

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT password
        FROM employees
        WHERE employee_id=%s
        """,
        (employee_id,)
    )

    employee = cursor.fetchone()

    if not employee:
        cursor.close()
        flash("Employee not found.", "danger")
        return redirect(url_for("employee_profile"))

    if employee["password"] != current_password:
        cursor.close()
        flash("Current password is incorrect.", "danger")
        return redirect(url_for("employee_profile"))

    cursor.execute(
        """
        UPDATE employees
        SET password=%s
        WHERE employee_id=%s
        """,
        (new_password, employee_id)
    )

    conn.commit()
    cursor.close()

    flash("Password changed successfully.", "success")

    return redirect(url_for("employee_profile"))

# =====================================
# UPDATE PROFILE
# =====================================

@app.route("/update_profile", methods=["POST"])
@login_required
def update_profile():

    employee_id = session["employee_id"]

    phone = request.form["phone"]
    address = request.form["address"]

    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE employees
        SET
            phone=%s,
            address=%s
        WHERE employee_id=%s
        """,
        (phone, address, employee_id)
    )

    conn.commit()
    cursor.close()

    flash("Profile updated successfully.", "success")

    return redirect(url_for("employee_profile"))


# =======================================
# Admin Profile
# =======================================

@app.route("/admin_profile", methods=["GET", "POST"])
def admin_profile():

    connection = get_connection()

    if not connection:
        return "Database connection failed"

    cursor = connection.cursor(dictionary=True)

    admin_id = session.get("admin_id", 1)

    # ==========================================
    # POST REQUEST
    # ==========================================

    if request.method == "POST":

        # ======================================
        # CHANGE PASSWORD
        # ======================================

        if request.form.get("change_password") == "1":

            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")

            cursor.execute("""
                SELECT password
                FROM admins
                WHERE id = %s
            """, (admin_id,))

            admin_data = cursor.fetchone()

            if not admin_data:

                flash("Admin account not found.", "danger")

                cursor.close()

                return redirect(url_for("admin_profile"))

            # Check current password

            if admin_data["password"] != current_password:

                flash("Current password is incorrect.", "danger")

                cursor.close()

                return redirect(url_for("admin_profile"))

            # Check new password confirmation

            if new_password != confirm_password:

                flash("New passwords do not match.", "danger")

                cursor.close()

                return redirect(url_for("admin_profile"))

            # Check empty password

            if not new_password:

                flash("New password cannot be empty.", "danger")

                cursor.close()

                return redirect(url_for("admin_profile"))

            # Update password

            cursor.execute("""
                UPDATE admins
                SET password = %s
                WHERE id = %s
            """, (new_password, admin_id))

            connection.commit()

            cursor.close()

            # Logout admin after password change

            session.clear()

            flash(
                "Password changed successfully. Please login again.",
                "success"
            )

            return redirect(url_for("admin_login"))


        # ======================================
        # EDIT PROFILE
        # ======================================

        else:

            name = request.form.get("name")
            username = request.form.get("username")
            email = request.form.get("email")
            phone = request.form.get("phone")

            cursor.execute("""
                UPDATE admins
                SET name = %s,
                    username = %s,
                    email = %s,
                    phone = %s
                WHERE id = %s
            """, (
                name,
                username,
                email,
                phone,
                admin_id
            ))

            connection.commit()

            session["admin_name"] = name

            flash("Profile updated successfully.", "success")

            cursor.close()

            return redirect(url_for("admin_profile"))


    # ==========================================
    # GET ADMIN DETAILS
    # ==========================================

    cursor.execute("""
        SELECT id, username, name, email, phone
        FROM admins
        WHERE id = %s
    """, (admin_id,))

    admin = cursor.fetchone()

    cursor.close()

    if not admin:
        return "Admin account not found"

    return render_template(
        "admin_profile.html",
        admin=admin
    )


@app.route("/admin_edit_profile")
def admin_edit_profile():
    connection = get_connection()

    if connection:
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT id, username, name FROM admins LIMIT 1")
        admin = cursor.fetchone()

        cursor.close()

        return render_template("admin_edit_profile.html", admin=admin)

    return "Database connection failed"

# =====================================
# RUN APPLICATION
# =====================================


if __name__=="__main__":


    app.run(
        debug=True
    )

