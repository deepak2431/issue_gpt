import React, { useEffect, useState } from "react";
import { useSelector } from "react-redux";
import { RootState } from "../redux";
import { CONFIG } from "../config";
import IssueCharts, {chartData} from "../components/IssueCharts";

const metricsTitle = ["Repository", "Total tracked issues", "Duplicate issues"];
const SERVER_URL = CONFIG.SERVER_URL;
const ORG_NAME = CONFIG.ORG_NAME;

interface metricsInfo {
  repository_count: string;
  tracked_issues: string;
  duplicate_issues: string;
}

const Overview = () => {
  const orgName = useSelector((state: RootState) => state.settings.orgName);
  const [metricsData, setMetricsData] = useState<metricsInfo>({
    repository_count: '',
    tracked_issues: '',
    duplicate_issues: '' 
  });  
  const [recentDuplicates, setRecentDuplicates] = useState([]);
  const [recentOpen, setRecentOpen] = useState([]);
  const [chartsDataset, setChartsDataset] = useState<chartData[]>([])

  const getMetricsData = () => {
    const metricsUrl = `${SERVER_URL}/metrics?org_name=${ORG_NAME}`;

    fetch(metricsUrl)
      .then((res) => {
        if (res.status !== 200) {
          throw new Error("Error while fetching the data");
        }
        return res.json();
      })
      .then((res) => {
        setMetricsData(res.metrics);
      })
      .catch((err) => console.log(err));
  };

  const getRecentDuplicates = async () => {
    const requestUrl = `${SERVER_URL}/issues?org_name=${ORG_NAME}&recent=recent_duplicate`;

    fetch(requestUrl)
      .then((res) => {
        if (res.status !== 200) {
          throw new Error("Request failed");
        }
        return res.json();
      })
      .then((res) => setRecentDuplicates(res.issues))
      .catch((err) => console.log(err));
  };

  const getRecentOpen = async () => {
    const requestUrl = `${SERVER_URL}/issues?org_name=${ORG_NAME}&recent=recent_open`;

    fetch(requestUrl)
      .then((res) => {
        if (res.status !== 200) {
          throw new Error("Request failed");
        }
        return res.json();
      })
      .then((res) => setRecentOpen(res.issues))
      .catch((err) => console.log(err));
  };

  const getChartsData = async () => {
    const requestUrl = `${SERVER_URL}/issues?org_name=${ORG_NAME}&recent=recent_week`;

    fetch(requestUrl)
      .then((res) => {
        if (res.status !== 200) {
          throw new Error("Request failed");
        }
        return res.json();
      })
      .then((res) => setChartsDataset(res.issues))
      .catch((err) => console.log(err));
  };

  useEffect(() => {
    getMetricsData();
    getRecentDuplicates();
    getRecentOpen();
    getChartsData();
  }, [orgName]);

  return (
    <div className="overview_info">
      <div className="overview_header">
        <p>Welcome, {orgName} </p>
      </div>
      <div className="overview_metrics">
        <div className="metrics_number">
          {metricsData &&
            Object.values(metricsData).map((val) => <h3>{val}</h3>)}
        </div>
        <div className="metrics_title">
          {metricsTitle.map((title) => (
            <p>{title}</p>
          ))}
        </div>
      </div>
      <div className="overview_metrics_info">
        <div className="overview_section_1">
          <h4 style={{ textAlign: "center", margin: "5px" }}>
            Recent duplicate issues
          </h4>
          {recentDuplicates &&
            recentDuplicates.map(
              ({ repository_name, created_issue_id, duplicate_issue_id }) => (
                <li>{`Found #${duplicate_issue_id} duplicate with #${created_issue_id} for the repository ${repository_name}`}</li>
              )
            )}
        </div>
        <div className="overview_section_2">
          <h4 style={{ textAlign: "center", margin: "5px" }}>
            Recent opened issues
          </h4>
          {recentOpen &&
            recentOpen.map(({ repository_name, created_issue_id }) => (
              <li>{`Opened issue ${created_issue_id} in the ${repository_name} repository.`}</li>
            ))}
        </div>
      </div>
      <div className="overview_metrics">
        <h4 style={{ marginBottom: "20px" }}>Last 7 days stats</h4>
        <IssueCharts chartsData={chartsDataset} />
      </div>
    </div>
  );
};

export default Overview;
