// static/js/custom.js

document.addEventListener("DOMContentLoaded", function () {
    console.log("سامانه طرح توجیهی: Frontend loaded!");
  
    // فعال‌سازی Tooltipها
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-mdb-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new mdb.Tooltip(tooltipTriggerEl);
    });
  });
  