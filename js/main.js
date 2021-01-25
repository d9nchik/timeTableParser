function selectDayOfWeek(weekNumber, dayNumber, classStyle = 'table-info') {
    if (dayNumber === 0)
        return;
    document.querySelectorAll('table:nth-child(' + weekNumber * 2 + ') td:nth-child(' + (dayNumber + 1) + ')')
        .forEach((e) => e.setAttribute('class', classStyle));
}

function getWeekNumber(d) {
    // Copy date so don't modify original
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    // Set to nearest Thursday: current date + 4 - current day number
    // Make Sunday's day number 7
    d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
    // Get first day of year
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    // Calculate full weeks to nearest Thursday
    // Return array of year and week number
    return Math.ceil((((d - yearStart) / 86400000) + 1) / 7);
}

function selectPair(weekNumber, dayNumber, pairNumber, classStyle = 'table-warning') {
    if (dayNumber === 0) {
        pairNumber = 1;
        dayNumber = 1;
        weekNumber = weekNumber % 2 + 1;
    }
    while (true) {
        let node =
            document.querySelector("table:nth-child(" + weekNumber * 2 + ") tbody tr:nth-child(" + pairNumber
                + ") td:nth-child(" + (dayNumber + 1) + ")");
        //node can be null in case if getNumbersOfPair return size + 1 value
        if (node && node.innerText) {
            node.setAttribute('class', classStyle);
            break;
        }
        pairNumber++;
        if (pairNumber > 5) {
            pairNumber = 1;
            dayNumber++;
            if (dayNumber > 5) {
                dayNumber = 1;
                weekNumber = weekNumber % 2 + 1;
            }
        }
    }
}

function getNumberOfPair(date) {
    const endOfPair = [1000, 1200, 1355, 1550, 1745];
    let time = date.getHours() * 100 + date.getMinutes();
    for (let i = 0; i < endOfPair.length; i++) {
        if (time < endOfPair[i])
            return i + 1;
    }
    return endOfPair.length + 1;
}

(function refresh() {
    let date = new Date();
    let weekNumber = (getWeekNumber(date) + 1) % 2 + 1
    selectDayOfWeek(weekNumber, date.getDay());
    selectPair(weekNumber, date.getDay(), getNumberOfPair(date));
    setTimeout(() => {
        selectDayOfWeek(weekNumber, date.getDay(), '');
        selectPair(weekNumber, date.getDay(), getNumberOfPair(date), '');
        refresh();
    }, 1_000 * 10)
})();