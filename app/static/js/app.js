// app.js

document.addEventListener("DOMContentLoaded", () => {
  console.log("Custom JS loaded");

  const alerts = document.querySelectorAll(".alert");
  if (alerts.length > 0) {
    setTimeout(() => {
      alerts.forEach(alert => {
        alert.style.display = "none";
      });
    }, 4000); // auto-hide alerts after 4 seconds
  }
});
