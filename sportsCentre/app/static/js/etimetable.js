const daysTag = document.querySelector(".days");
const currentDate = document.querySelector(".current-date");
const prevNextIcon = document.querySelectorAll(".icons span");

let date = new Date();
let currYear = date.getFullYear();
let currMonth = date.getMonth();

const months = [
  "January",
  "February",
  "March",
  "April",
  "May",
  "June",
  "July",
  "August",
  "September",
  "October",
  "November",
  "December",
];

const renderCalendar = () => {
  const firstDayOfMonth = new Date(currYear, currMonth, 1).getDay();
  const lastDateOfMonth = new Date(currYear, currMonth + 1, 0).getDate();
  const lastDayOfMonth = new Date(currYear, currMonth, lastDateOfMonth).getDay();
  const lastDateOfLastMonth = new Date(currYear, currMonth, 0).getDate();
  let liTag = "";

  // Generate inactive days for last month
  for (let i = firstDayOfMonth; i > 0; i--) {
    liTag += `<li class="inactive">${lastDateOfLastMonth - i + 1}</li>`;
  }

  // Generate days for current month
  for (let i = 1; i <= lastDateOfMonth; i++) {
    const isToday =
      i === date.getDate() &&
      currMonth === new Date().getMonth() &&
      currYear === new Date().getFullYear()
        ? "active"
        : "";

    // Query the database for work details for the current day
    fetch(`/work/${currYear}-${currMonth + 1}-${i}`)
      .then((response) => response.json())
      .then((data) => {
        let workDetails = "";
        if (data.length > 0) {
          data.forEach((work) => {
            workDetails += `<p>${work.position} at ${work.facility} from ${work.start_time} to ${work.end_time}</p>`;
          });
        }
        liTag += `<li class="${isToday}">${i}${workDetails}</li>`;
        daysTag.innerHTML = liTag;
      })
      .catch((error) => console.error(error));
  }

  // Generate inactive days for next month
  for (let i = lastDayOfMonth; i < 6; i++) {
    liTag += `<li class="inactive">${i - lastDayOfMonth + 1}</li>`;
  }

  // Update current date label
  currentDate.innerText = `${months[currMonth]} ${currYear}`;
};

renderCalendar();

// Add event listeners for navigation buttons
prevNextIcon.forEach((icon) => {
  icon.addEventListener("click", () => {
    currMonth = icon.id === "prev" ? currMonth - 1 : currMonth + 1;

    if (currMonth < 0 || currMonth > 11) {
      date = new Date(currYear, currMonth, new Date().getDate());
      currYear = date.getFullYear();
      currMonth = date.getMonth();
    } else {
      date = new Date();
    }

    renderCalendar();
  });
});
