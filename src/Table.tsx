import React, { FunctionComponent } from 'react';

import { Table as Table } from 'react-bootstrap';
// import './Table.css';

interface IProps {
  data: string[][][];
}

const MyTable: FunctionComponent<IProps> = ({ data }) => {
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
        {body.map(row => (
          <tr key={String(row)}>
            {row.map((data, index) => (
              <td key={String(data) + index}>{String(data)}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default MyTable;
