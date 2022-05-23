if (Cookies.get("session_token") != undefined) {
  document.getElementById("login").style.display = "none";
  document.getElementById("logout").style.display = "flex";
} else {
  document.getElementById("login").style.display = "block";
  document.getElementById("logout").style.display = "none";
}

setTimeout(loadNotificationLocation, 1500);
window.onresize = loadNotificationLocation;

function loadNotificationLocation(){
  var not_center = document.getElementById("not-center");
  var not_icon = document.getElementById("not-icon");

  var rect = not_icon.getBoundingClientRect();

  not_center.style.left = rect.left - not_center.getBoundingClientRect().width + "px";
  not_center.style.top = rect.bottom + "px";
}
