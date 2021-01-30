import React, { FunctionComponent, useState, useEffect } from 'react';
import PCTimeTable from './PCTimeTable';
import MobileTimeTable from './MobileTimeTable';

interface IProps {
  data: string[][][];
  activeDay: 0 | 1 | 2 | 3 | 4 | 5 | 6;
  activePair: [0 | 1, number, number];
  activeWeek: number;
  weekNumber: 0 | 1;
}

const AdaptiveTable: FunctionComponent<IProps> = ({
  data,
  activeDay,
  activePair,
  activeWeek,
  weekNumber,
}) => {
  const [isDesktop, setDesktop] = useState(window.innerWidth >= 768);

  useEffect(() => {
    window.addEventListener('resize', updateOnResize);

    return () => window.removeEventListener('resize', updateOnResize);

    function updateOnResize() {
      setDesktop(window.innerWidth >= 768);
    }
  }, []);

  return (
    <div>
      {isDesktop ? (
        <PCTimeTable
          data={data}
          activeDay={activeDay}
          activePair={activePair}
          activeWeek={activeWeek}
          weekNumber={weekNumber}
        />
      ) : (
        <MobileTimeTable
          data={data}
          activeDay={activeDay}
          activePair={activePair}
          activeWeek={activeWeek}
          weekNumber={weekNumber}
        />
      )}
    </div>
  );
};

export default AdaptiveTable;
