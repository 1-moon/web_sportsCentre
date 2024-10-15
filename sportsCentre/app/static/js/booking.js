const daysTag = document.querySelector(".days"),
currentDate = document.querySelector(".current-date"),
prevNextIcon = document.querySelectorAll(".icons span");

// getting new date, current year and month
let date = new Date(),
    currYear = date.getFullYear(),
    currMonth = date.getMonth();

// storing full name of all months in array
const months = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"];

const renderCalendar = () => {
    let firstDayofMonth = new Date(currYear, currMonth, 1).getDay(), // getting first day of month
    lastDateofMonth = new Date(currYear, currMonth + 1, 0).getDate(), // getting last date of month
    lastDayofMonth = new Date(currYear, currMonth, lastDateofMonth).getDay(), // getting last day of month
    lastDateofLastMonth = new Date(currYear, currMonth, 0).getDate(); // getting last date of previous month

    let liTag = "";

    for (let i = firstDayofMonth; i > 0; i--) { // creating li of previous month last days
        liTag += `<li class="inactive">${lastDateofLastMonth - i + 1}</li>`;
    }

    for (let i = 1; i <= lastDateofMonth; i++) { // creating li of all days of current month
        // adding active class to li if the current day, month, and year matched
        let isToday = i === date.getDate() && currMonth === new Date().getMonth() 
                     && currYear === new Date().getFullYear() ? "active" : "";
        liTag += `<li class="${isToday}"><a href="#" data-day="${i}" data-month="${currMonth}" data-year="${currYear}" class="calendar-day">${i}</a></li>`;
    }

    for (let i = lastDayofMonth; i < 6; i++) { // creating li of next month first days
        liTag += `<li class="inactive">${i - lastDayofMonth + 1}</li>`;
    }

    currentDate.innerText = `${months[currMonth]} ${currYear}`; // passing current mon and yr as currentDate text
    daysTag.innerHTML = liTag;

    // Add click event listener to each calendar day
    const calendarDays = document.querySelectorAll('.calendar-day');
    calendarDays.forEach(day => {
      day.addEventListener('click', (event) => {
        event.preventDefault();
        const day = event.target.getAttribute('data-day');
        const month = event.target.getAttribute('data-month');
        const year = event.target.getAttribute('data-year');
        const url = `/activity_events?day=${day}&month=${month}&year=${year}`;
        window.location.href = url;
      });
    });
};

renderCalendar();

// Adding click event listeners to prev and next icons
prevNextIcon.forEach(icon => {
    icon.addEventListener("click", () => {
        if (icon.id === "prev") {
            currMonth--;
            if (currMonth < 0) {
                currYear--;
                currMonth = 11;
            }
        } else {
            currMonth++;
            if (currMonth > 11) {
                currYear++;
                currMonth = 0;
            }
        }
        renderCalendar();
    });
});

const activitySelect = document.getElementById('activity');
activitySelect.addEventListener('change', async () => {
  const activityId = activitySelect.value;
  const response = await fetch(`/timetable/${activityId}`);
  const timetableData = await response.json();
  populateTimetable(timetableData);
});


