import React, { FunctionComponent } from 'react';

import { Table } from 'react-bootstrap';

interface IProps {
  data: string[][][];
  activeDay: 0 | 1 | 2 | 3 | 4 | 5 | 6;
  activePair: [0 | 1, number, number];
  activeWeek: number;
  weekNumber: 0 | 1;
}

const MobileTable: FunctionComponent<IProps> = ({
  data,
  activeDay,
  activePair: [pairWeekNumber, pairActiveDay, pairActiveNumber],
  weekNumber,
  activeWeek,
}) => {
  data = transponeData(data);
  const [head, ...body] = data;
  const modifiedBody = body.map(day =>
    day
      .map((info, infoIndex) => ({
        info: String(info),
        headInfo: String(head[infoIndex]),
        infoIndex,
      }))
      .filter(({ info }) => info.length)
  );
  return (
    <div>
      {modifiedBody.map((day, dayIndex) => {
        const [head, ...body] = day;
        return (
          <Table striped bordered hover>
            <thead className="thead-dark">
              <tr>
                <th>{head.headInfo}</th>
                <th>{head.info}</th>
              </tr>
            </thead>
            <tbody>
              {body.map(({ info, headInfo, infoIndex }) => (
                <tr>
                  <td>{headInfo}</td>
                  <td>{info}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        );
      })}
    </div>
  );
};

function transponeData<E>(data: E[][]): E[][] {
  const transponed: E[][] = [];

  for (let i = 0; i < data[0].length; i++) {
    const tempArray: E[] = [];
    for (let j = 0; j < data.length; j++) {
      tempArray.push(data[j][i]);
    }
    transponed.push(tempArray);
  }
  return transponed;
}

export default MobileTable;
