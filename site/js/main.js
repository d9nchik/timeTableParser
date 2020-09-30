function selectDayOfWeek(weekNumber, dayNumber) {
    document.querySelectorAll('table:nth-child(' + weekNumber * 2 + ') td:nth-child(' + (dayNumber + 1) + ')').forEach(
        (e) => e.setAttribute('class', 'table-info'));
}

function getWeekNumber(d) {
    // Copy date so don't modify original
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    // Set to nearest Thursday: current date + 4 - current day number
    // Make Sunday's day number 7
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
    // Get first day of year
    var yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    // Calculate full weeks to nearest Thursday
    var weekNo = Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
    // Return array of year and week number
    return weekNo;
}

let date = new Date();

selectDayOfWeek(getWeekNumber(date) % 2 + 1, date.getDay());