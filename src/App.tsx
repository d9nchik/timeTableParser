import React from 'react';
import './App.css';
import data from './data.json';
import MyTable from './Table';

function App() {
  return (
    <div>
      <h1 className="text-center">Розклад занять</h1>
      <h2 className="text-center">Перший тиждень</h2>
      <MyTable data={data[0]} />
      <h2 className="text-center">Другий тиждень</h2>
      <MyTable data={data[1]} />
    </div>
  );
}

export default App;
