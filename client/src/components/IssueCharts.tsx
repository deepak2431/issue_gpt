import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
} from "recharts";

export interface chartData {
  Duplicate: number
  Open: number
  name: string
  total: number
}

interface IProps {
  chartsData: chartData []
}


const IssueCharts:React.FC<IProps> = ({ chartsData }) => {
  return (
    <BarChart
      width={800}
      height={300}
      data={chartsData}
      margin={{
        top: 5,
        right: 30,
        left: 20,
        bottom: 5,
      }}
    >
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Bar dataKey="Open" fill="#8884d8" />
      <Bar dataKey="Duplicate" fill="#82ca9d" />
    </BarChart>
  );
};

export default IssueCharts;
