

// ===============================
// CARD ANIMATION
// ===============================

const cards = document.querySelectorAll(
    ".dashboard-card, .card-box"
);

cards.forEach((card,index)=>{

    card.style.opacity="0";
    card.style.transform="translateY(30px)";

    setTimeout(()=>{

        card.style.transition=".6s ease";

        card.style.opacity="1";
        card.style.transform="translateY(0)";

    },index*120);

});


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


// ===============================
// TABLE HOVER
// ===============================

const rows = document.querySelectorAll(".report-table tbody tr");

rows.forEach(row=>{

    row.addEventListener("mouseenter",()=>{

        row.style.transform="scale(1.01)";

    });

    row.addEventListener("mouseleave",()=>{

        row.style.transform="scale(1)";

    });

});

// ===============================
// PAGE LOADED
// ===============================

window.addEventListener("DOMContentLoaded", () => {
    updateClock();
})

/* ==================================================
            EMPLOYEE LEAVE MANAGEMENT
================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const leaveForm = document.querySelector("form[action*='apply_leave']");

    if (!leaveForm) return;

    const fromDate = document.querySelector("input[name='from_date']");
    const toDate = document.querySelector("input[name='to_date']");

    // Today's date
    const today = new Date().toISOString().split("T")[0];

    fromDate.min = today;
    toDate.min = today;

    // To Date cannot be before From Date
    fromDate.addEventListener("change", function () {

        toDate.min = this.value;

        if (toDate.value < this.value) {
            toDate.value = this.value;
        }

    });

    // Form Validation
    leaveForm.addEventListener("submit", function(e){

        if(fromDate.value==""){

            alert("Please select From Date.");

            e.preventDefault();

            return;

        }

        if(toDate.value==""){

            alert("Please select To Date.");

            e.preventDefault();

            return;

        }

        if(toDate.value<fromDate.value){

            alert("To Date cannot be before From Date.");

            e.preventDefault();

            return;

        }

        const reason=document.querySelector("textarea[name='reason']");

        if(reason.value.trim().length<10){

            alert("Please enter a proper reason.");

            e.preventDefault();

            return;

        }

        if(!confirm("Submit this leave request?")){

            e.preventDefault();

        }

    });

});

/* ==========================================
        REPORTS VALIDATION
========================================== */

// ---------- Task Report ----------

const taskForm = document.querySelector('form[action*="submit_task_report"]');

if(taskForm){

taskForm.addEventListener("submit",function(e){

    const task=document.querySelector('select[name="task_id"]');

    const hours=document.querySelector('input[name="hours"]');

    const work=document.querySelector('textarea[name="work_done"]');

    if(task.value==""){

        alert("Please select a task.");

        e.preventDefault();

        return;

    }

    if(hours.value=="" || Number(hours.value)<=0){

        alert("Please enter valid working hours.");

        e.preventDefault();

        return;

    }

    if(work.value.trim().length<10){

        alert("Please describe your work properly.");

        e.preventDefault();

        return;

    }

    if(!confirm("Submit Task Report?")){

        e.preventDefault();

    }

});

}

// ---------- Weekly Report ----------

const weeklyForm=document.querySelector('form[action*="submit_weekly_report"]');

if(weeklyForm){

weeklyForm.addEventListener("submit",function(e){

    const start=document.querySelector('input[name="week_start"]');

    const end=document.querySelector('input[name="week_end"]');

    const tasks=document.querySelector('textarea[name="work_summary"]');

    const plan=document.querySelector('textarea[name="next_week_plan"]');

    if(start.value==""){

        alert("Please select week start date.");

        e.preventDefault();

        return;

    }

    if(end.value==""){

        alert("Please select week end date.");

        e.preventDefault();

        return;

    }

    if(end.value<start.value){

        alert("Week End cannot be before Week Start.");

        e.preventDefault();

        return;

    }

    if(tasks.value.trim().length<10){

        alert("Please enter completed tasks.");

        e.preventDefault();

        return;

    }

    if(!confirm("Submit Weekly Report?")){

        e.preventDefault();

    }

});

}

// ===============================
// PAGE LOAD ANIMATION
// ===============================

window.addEventListener("load", () => {

    const tableBox = document.querySelector(".table-box");

    if (!tableBox) return;

    tableBox.style.opacity = "0";
    tableBox.style.transform = "translateY(30px)";

    setTimeout(() => {

        tableBox.style.transition = ".6s ease";

        tableBox.style.opacity = "1";

        tableBox.style.transform = "translateY(0)";

    }, 150);

});


// ===============================
// TABLE ROW HOVER
// ===============================

const tableRows = document.querySelectorAll("tbody tr");

rows.forEach(row => {

    row.addEventListener("mouseenter", () => {

        row.style.transition = ".25s";

        row.style.transform = "scale(1.01)";

    });

    row.addEventListener("mouseleave", () => {

        row.style.transform = "scale(1)";

    });

});


// ===============================
// MONTH FILTER (Frontend Only)
// ===============================

const monthFilter = document.querySelector(".filter-box select");

if(monthFilter){

    monthFilter.addEventListener("change", function(){

        console.log("Selected Month :", this.value);

        // Flask + MySQL filtering will be added later

    });

}


// ===============================
// ACTIVE MENU
// ===============================

document.querySelectorAll(".menu li").forEach(item=>{

    item.addEventListener("click",function(){

        document.querySelectorAll(".menu li")
        .forEach(li=>li.classList.remove("active"));

        this.classList.add("active");

    });

});


// ===============================
// RECORD COUNT ANIMATION
// ===============================

const record = document.querySelector(".record-count");

if(record){

    record.style.opacity="0";

    setTimeout(()=>{

        record.style.transition=".8s";

        record.style.opacity="1";

    },400);

}


// ===============================
// PAGE READY
// ===============================

console.log("Employee Attendance Page Loaded Successfully.");