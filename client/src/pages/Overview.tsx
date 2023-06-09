import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { RootState } from "../redux";
import { CONFIG } from "../config";

const metricsTitle = [
  "Repository",
  "Total issues",
  "Open issues",
  "Duplicate issues",
];
const SERVER_URL = CONFIG.SERVER_URL;

const Overview = () => {
  const [metricsData, setMetricsData] = useState([]);

  const getMetricsData = () => {
    const metricsUrl = `${SERVER_URL}/metrics?org_name=deepak2431`;

    fetch(metricsUrl)
      .then((res) => {
        if (res.status !== 200) {
          throw new Error("Error while fetching the data");
        }
        return res.json();
      })
      .then((res) => setMetricsData(res.metrics))
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    getMetricsData();
  }, []);

  const metricsNumber = [12, 89, 839, 10];

  const orgName = useSelector((state: RootState) => state.settings.orgName);
  return (
    <div className="overview_info">
      <div className="overview_header">
        <p>Welcome, {orgName} </p>
      </div>
      <div className="overview_metrics">
        <div className="metrics_number">
          {metricsNumber.map((val) => (
            <h2>{val}</h2>
          ))}
        </div>
        <div className="metrics_title">
          {metricsTitle.map((title) => (
            <p>{title}</p>
          ))}
        </div>
      </div>
      <div className="overview_metrics_info">
        <div className="overview_section_1">
          <p>Recent duplicate issues</p>
        </div>
        <div className="overview_section_2">
          <p>Issues opened in last 24 hrs</p>
        </div>
      </div>
    </div>
  );
};

export default Overview;
