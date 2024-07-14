import React from 'react';

function generateTableData(data) {
  if (!data || !Array.isArray(data)) return null;

  // Extracting headers from the first object assuming all objects have the same structure
  const headers = Object.keys(data[0]);

  return (
    <table className="border-collapse border border-gray-200">
      <thead>
        <tr className="bg-gray-100">
          {headers.map((header, index) => (
            <th key={index} className="border border-gray-300 p-2">{header}</th>
          ))}
        </tr>
      </thead>
      <tbody>
        {data.map((item, index) => (
          <tr key={index} className="bg-white">
            {headers.map((header, hIndex) => (
              <td key={hIndex} className="border border-gray-300 p-2">{item[header]}</td>
            ))}
          </tr>
        ))}
      </tbody>
    </table>
  );
}

export default function TransactionTable({ transactions }) {
  return (
    <div className="overflow-x-auto">
      {generateTableData(transactions)}
    </div>
  );
}
