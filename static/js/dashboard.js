// ======================================
// SMARTDESK ADMIN DASHBOARD
// dashboard.js
// ======================================


// -------------------------------
// Sidebar Active Menu
// -------------------------------

const menuItems=document.querySelectorAll(".menu li");

menuItems.forEach(item=>{

item.addEventListener("click",()=>{

menuItems.forEach(i=>i.classList.remove("active"));

item.classList.add("active");

});

});




// -------------------------------
// Notification Click
// -------------------------------

// const notification=document.querySelector(".notification");

// if(notification){

// notification.addEventListener("click",()=>{

// alert("No new notifications.");

// });

// }

// ===============================
// NOTIFICATION
// ===============================

const notificationBtn =
document.getElementById("notificationBtn");

const notificationDropdown =
document.getElementById("notificationDropdown");

if(notificationBtn && notificationDropdown){

    notificationBtn.addEventListener("click",(e)=>{

        e.stopPropagation();

        notificationDropdown.classList.toggle("show");

    });

    document.addEventListener("click",(e)=>{

        if(!notificationDropdown.contains(e.target) &&
           !notificationBtn.contains(e.target)){

            notificationDropdown.classList.remove("show");

        }

    });

}




// -------------------------------
// Profile Click
// -------------------------------

const profile=document.querySelector(".profile");

if(profile){

profile.addEventListener("click",()=>{

alert("Admin Profile");

});

}




// -------------------------------
// Search
// -------------------------------

const search=document.querySelector(".search-box input");

if(search){

search.addEventListener("keyup",()=>{

console.log("Searching:",search.value);

});

}

// -------------------------------
// Card Hover Animation
// -------------------------------

const cards=document.querySelectorAll(".dashboard-card");

cards.forEach(card=>{

card.addEventListener("mouseenter",()=>{

card.style.transform="translateY(-10px) scale(1.02)";

});

card.addEventListener("mouseleave",()=>{

card.style.transform="translateY(0)";

});

});


// admin attendance
/* =====================================================
   ADMIN ATTENDANCE MODULE
   Part 1 - View & Edit Modal
===================================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ============================
       View Attendance
    ============================ */

    const viewButtons = document.querySelectorAll(".view-btn");

    viewButtons.forEach(button => {

        button.addEventListener("click", function () {

            document.getElementById("viewEmployeeName").textContent =
                this.dataset.name;

            document.getElementById("viewDepartment").textContent =
                this.dataset.department;

            document.getElementById("viewEmail").textContent =
                this.dataset.email;

            document.getElementById("viewEmployeeId").textContent =
                "EMP" + String(this.dataset.id).padStart(3, "0");

            document.getElementById("viewDate").textContent =
                this.dataset.date;

            document.getElementById("viewCheckIn").textContent =
                this.dataset.checkin || "-";

            document.getElementById("viewCheckOut").textContent =
                this.dataset.checkout || "-";

            document.getElementById("viewWorkingHours").textContent =
                this.dataset.hours || "-";

            const statusBadge =
                document.getElementById("viewStatus");

            statusBadge.textContent = this.dataset.status;

            statusBadge.className = "badge";

            if (this.dataset.status === "Present") {

                statusBadge.classList.add("bg-success");

            }

            else if (this.dataset.status === "Absent") {

                statusBadge.classList.add("bg-danger");

            }

            else {

                statusBadge.classList.add("bg-warning", "text-dark");

            }

        });

    });


/* ============================
   Working Hours Calculation
============================ */

const checkInInput =
    document.getElementById("editCheckIn");

const checkOutInput =
    document.getElementById("editCheckOut");

const workingHoursInput =
    document.getElementById("editWorkingHours");

function calculateWorkingHours() {

    if (!checkInInput ||
        !checkOutInput ||
        !workingHoursInput) {

        return;
    }

    const checkIn = checkInInput.value;
    const checkOut = checkOutInput.value;

    if (checkIn === "" || checkOut === "") {

        workingHoursInput.value = "";

        return;
    }

    const inTime = checkIn.split(":");
    const outTime = checkOut.split(":");

    const inDate = new Date();
    inDate.setHours(inTime[0], inTime[1], 0);

    const outDate = new Date();
    outDate.setHours(outTime[0], outTime[1], 0);

    let diff =
        (outDate - inDate) / (1000 * 60);

    if (diff < 0) {

        alert("Check Out time cannot be earlier than Check In time.");

        checkOutInput.value = "";

        workingHoursInput.value = "";

        return;

    }

    const hours =
        Math.floor(diff / 60);

    const minutes =
        diff % 60;

    workingHoursInput.value =
        hours + " hrs " + minutes + " mins";

}

if (checkInInput && checkOutInput) {

    checkInInput.addEventListener(
        "change",
        calculateWorkingHours
    );

    checkOutInput.addEventListener(
        "change",
        calculateWorkingHours
    );

}

/* ============================
   Status Handling
============================ */

const statusSelect =
    document.getElementById("editStatus");

if (statusSelect) {

    statusSelect.addEventListener(
        "change",
        function () {

            if (this.value === "Absent" ||
                this.value === "Leave") {

                checkInInput.value = "";

                checkOutInput.value = "";

                workingHoursInput.value = "";

            }

        }
    );

}
/* ============================
   Employee Attendance Search
============================ */

const searchInput =
    document.getElementById("searchEmployee");

if (searchInput) {

    searchInput.addEventListener("keyup", function () {

        const value =
            this.value.toLowerCase().trim();

        const rows =
            document.querySelectorAll(".attendance-card tbody tr");

        rows.forEach(row => {

            const text =
                row.innerText.toLowerCase();

            if (text.includes(value)) {

                row.style.display = "";

            }

            else {

                row.style.display = "none";

            }

        });

    });

}


/* ============================
   Highlight Current Row
============================ */

const attendanceRows =
    document.querySelectorAll(".attendance-card tbody tr");

attendanceRows.forEach(row => {

    row.addEventListener("click", function () {

        attendanceRows.forEach(r => {

            r.classList.remove("table-active");

        });

        this.classList.add("table-active");

    });

});


/* ============================
   Tooltip Initialization
============================ */

const tooltipTriggerList =
    [].slice.call(
        document.querySelectorAll(
            '[data-bs-toggle="tooltip"]'
        )
    );

tooltipTriggerList.map(function (tooltipTriggerEl) {

    return new bootstrap.Tooltip(
        tooltipTriggerEl
    );

});


/* ============================
   Auto Focus Search
============================ */

window.addEventListener("load", function () {

    if (searchInput) {

        searchInput.focus();

    }

});


/* ============================
   Monthly Report Button
============================ */

// const reportButton =
//     document.getElementById("generateReport");

// if (reportButton) {

//     reportButton.addEventListener("click", function () {

//         alert(
//             "Monthly report integration will be connected with Flask database."
//         );

//     });

// }


/* =====================================================
   MONTHLY ATTENDANCE REPORT
===================================================== */

const reportButton = document.getElementById("generateReport");

if (reportButton) {

    reportButton.addEventListener("click", async function () {

        const employee = document.getElementById("reportEmployee");
        const month = document.getElementById("reportMonth");

        const employeeId = employee.value;
        const selectedMonth = month.value;

        if (!employeeId || employeeId === "Select Employee") {

            alert("Please select an employee.");
            return;

        }

        if (!selectedMonth) {

            alert("Please select a month.");
            return;

        }

        reportButton.disabled = true;

        reportButton.innerHTML = `
            <span class="spinner-border spinner-border-sm me-2"></span>
            Generating...
        `;

        try {

            const response = await fetch(
                `/monthly_attendance_report?employee_id=${encodeURIComponent(employeeId)}&month=${encodeURIComponent(selectedMonth)}`
            );

            const data = await response.json();

            if (!response.ok || !data.success) {

                throw new Error(
                    data.message || "Unable to generate report."
                );

            }

            /* =========================
               UPDATE SUMMARY
            ========================= */

            document.getElementById("totalDays").textContent =
                data.total_days || 0;

            document.getElementById("presentDays").textContent =
                data.present || 0;

            document.getElementById("absentDays").textContent =
                data.absent || 0;

            document.getElementById("leaveDays").textContent =
                data.leave || 0;


            /* =========================
               UPDATE TABLE
            ========================= */

            const tableBody =
                document.getElementById("monthlyReportTable");

            tableBody.innerHTML = "";


            if (!data.records || data.records.length === 0) {

                tableBody.innerHTML = `
                    <tr>
                        <td colspan="5"
                            class="text-center text-muted py-4">

                            No attendance records found
                            for the selected month.

                        </td>
                    </tr>
                `;

                return;
            }


            data.records.forEach(function (row) {

                let statusBadge = "";

                if (row.status === "Present") {

                    statusBadge = `
                        <span class="badge bg-success">
                            Present
                        </span>
                    `;

                } else if (row.status === "Absent") {

                    statusBadge = `
                        <span class="badge bg-danger">
                            Absent
                        </span>
                    `;

                } else {

                    statusBadge = `
                        <span class="badge bg-warning text-dark">
                            Leave
                        </span>
                    `;
                }


                const tableRow = `
                    <tr>

                        <td>
                            ${row.attendance_date || "-"}
                        </td>

                        <td>
                            ${row.check_in || "-"}
                        </td>

                        <td>
                            ${row.check_out || "-"}
                        </td>

                        <td>
                            ${row.working_hours || "-"}
                        </td>

                        <td>
                            ${statusBadge}
                        </td>

                    </tr>
                `;

                tableBody.insertAdjacentHTML(
                    "beforeend",
                    tableRow
                );

            });

        }

        catch (error) {

            console.error(
                "Monthly report error:",
                error
            );

            alert(
                "Unable to generate the monthly report."
            );

        }

        finally {

            reportButton.disabled = false;

            reportButton.innerHTML = `
                <i class="bi bi-search me-2"></i>
                Generate Report
            `;

        }

    });

}

/* =====================================================
   Monthly Report Helpers
===================================================== */

function updateMonthlySummary(data) {

    if (!data) return;

    const totalDays = document.getElementById("totalDays");
    const presentDays = document.getElementById("presentDays");
    const absentDays = document.getElementById("absentDays");
    const leaveDays = document.getElementById("leaveDays");

    if (totalDays) totalDays.textContent = data.total_days || 0;
    if (presentDays) presentDays.textContent = data.present || 0;
    if (absentDays) absentDays.textContent = data.absent || 0;
    if (leaveDays) leaveDays.textContent = data.leave || 0;

}

/* =====================================================
   Reset Edit Modal
===================================================== */

const editForm =
    document.getElementById("editAttendanceForm");

if (editForm) {

    editForm.addEventListener("reset", function () {

        if (workingHoursInput) {

            workingHoursInput.value = "";

        }

    });

}

/* =====================================================
   End of DOMContentLoaded
===================================================== */

});