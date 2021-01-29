import React, { FunctionComponent } from 'react';

import { Table } from 'react-bootstrap';

interface IProps {
  data: string[][][];
  activeDay: 0 | 1 | 2 | 3 | 4 | 5 | 6;
  activePair: [0 | 1, number, number];
  activeWeek: number;
  weekNumber: 0 | 1;
}

const MyTable: FunctionComponent<IProps> = ({
  data,
  activeDay,
  activePair: [pairWeekNumber, pairActiveDay, pairActiveNumber],
  weekNumber,
  activeWeek,
}) => {
  const [head, ...body] = data;
  return (
    <Table striped bordered hover>
      <thead className="thead-dark">
        <tr>
          {head.map((item, index) => (
            <th key={item[0] + index}>{item[0]}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {body.map((row, rowIndex) => (
          <tr key={String(row)}>
            {row.map((data, index) => (
              <td
                className={
                  pairWeekNumber === weekNumber &&
                  index - 1 === pairActiveDay &&
                  pairActiveNumber === rowIndex
                    ? 'table-warning'
                    : weekNumber === activeWeek && activeDay === index - 1
                    ? 'table-info'
                    : ''
                }
                key={String(data) + index}
              >
                {String(data)}
              </td>
            ))}
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default MyTable;
