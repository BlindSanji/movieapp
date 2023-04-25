const filterContainer = document.querySelector('.filter-container');
const icon = document.getElementById("filter-icon");

filterContainer.addEventListener("click", function() {
  if (icon.textContent.trim() === "expand_more") {
    icon.textContent = "expand_less";
  } else {
    icon.textContent = "expand_more";
  }
});