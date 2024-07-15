var isOpen = false;

function toggleSideBar() {
  if (!isOpen) openNav();
  else closeNav();
}

//function for opening the sidebar
function openNav() {
  isOpen = true;
  document.getElementById("sidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

//function for closing the sidebar
function closeNav() {
  isOpen = false;
  console.log(isOpen);
  document.getElementById("sidebar").style.width = "0";
  document.getElementById("main").style.marginLeft = "0";
}
