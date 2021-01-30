import React, { FunctionComponent } from 'react';
import data from '../data.json';
import PCTimeTable from './PCTimeTable';
import MobileTimeTable from './MobileTimeTable';

const TimeTable: FunctionComponent = () => {
  const date = new Date();
  const weekNumber = ((getWeekNumber(date) + 1) % 2) as 0 | 1;
  const dayNumber = ((date.getDay() + 6) % 7) as 0 | 1 | 2 | 3 | 4 | 5 | 6;
  const pair = selectPair(weekNumber, dayNumber, getNumberOfPair(date), data);

  return (
    <div>
      <h2 className="text-center">Перший тиждень</h2>

      <MobileTimeTable
        data={data[0]}
        activeDay={dayNumber}
        activePair={pair}
        activeWeek={weekNumber}
        weekNumber={0}
      />
      <h2 className="text-center">Другий тиждень</h2>

      <MobileTimeTable
        data={data[1]}
        activeDay={dayNumber}
        activePair={pair}
        activeWeek={weekNumber}
        weekNumber={1}
      />
    </div>
  );
};

function getWeekNumber(d: Date) {
  // Copy date so don't modify original
  d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  // Set to nearest Thursday: current date + 4 - current day number
  // Make Sunday's day number 7
  d.setUTCDate(d.getUTCDate() + 4 - (d.getUTCDay() || 7));
  // Get first day of year
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  // Calculate full weeks to nearest Thursday
  // Return array of year and week number
  return Math.ceil(((Number(d) - Number(yearStart)) / 86400000 + 1) / 7);
}

function getNumberOfPair(date: Date): 0 | 1 | 2 | 3 | 4 | 5 | 6 {
  const endOfPair = [1000, 1200, 1355, 1550, 1745, 2005];
  let time = date.getHours() * 100 + date.getMinutes();
  for (let i = 0; i < endOfPair.length; i++) {
    if (time < endOfPair[i]) return i as 0 | 1 | 2 | 3 | 4 | 5;
  }
  return endOfPair.length as 6;
}

function selectPair(
  weekNumber: 0 | 1,
  dayNumber: 0 | 1 | 2 | 3 | 4 | 5 | 6,
  pairNumber: 0 | 1 | 2 | 3 | 4 | 5 | 6,
  data: string[][][][]
): [0 | 1, number, number] {
  while (true) {
    try {
      let pair = data[weekNumber][pairNumber + 1][dayNumber + 1];
      if (pair.length) {
        return [weekNumber, dayNumber, pairNumber];
      }
    } catch (error) {}

    pairNumber++;
    if (pairNumber > 5) {
      pairNumber = 0;
      dayNumber++;
      if (dayNumber > 5) {
        dayNumber = 0;
        weekNumber = ((weekNumber + 1) % 2) as 0 | 1;
      }
    }
  }
}
export default TimeTable;
