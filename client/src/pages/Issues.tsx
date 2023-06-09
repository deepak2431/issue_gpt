import React, { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";

import TableCard from "../components/TableCard";
import InputForm from "../components/InputForm";
import Button from "../components/Button";
import { CONFIG } from "../config";

const tableHeadings = [
  {
    headingTitle: "Organization Name",
  },
  {
    headingTitle: "Repository Name",
  },
  {
    headingTitle: "Open issue ID",
  },
  {
    headingTitle: "Duplicate issue ID",
  },
];

const SERVER_URL = CONFIG.SERVER_URL;

const Issues = () => {
  const [repo, setRepo] = useState<string>("");
  const [error, setError] = useState<boolean>(false);
  const [addRepo, setAddRepo] = useState<boolean>(false);
  const [issueData, setIssueData] = useState([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [issueDataError, setIssueDataError] = useState<boolean>(false);

  const getIssueData = async () => {
    try {
      const resp = await fetch(
        SERVER_URL + "/duplicate_issues?org_name=deepak"
      );
      if (resp.status === 200) {
        const data = await resp.json();
        setIssueData(data.duplicate_issues);
        setLoading(false);
      } else {
        throw Error("Unable to fetch the data");
      }
    } catch (error) {
      setIssueDataError(true);
      console.log(error);
    }
  };

  useEffect(() => {
    getIssueData();
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setRepo(e.target.value);
  };

  const handleAddNew = () => {
    setAddRepo(true);
    setError(false);
    setRepo("");
  };

  const handleAddRepo = () => {
    setError(false);
    const requestData = {
      org_name: "deepak2431",
      repository: repo,
    };

    const reqOptions = {
      method: "POST",
      body: JSON.stringify(requestData),
      headers: {
        "Content-Type": "application/json",
      },
    };

    fetch(`${SERVER_URL}/repository`, reqOptions)
      .then((res) => {
        if (res.status !== 201) {
          throw new Error("Request unsuccessful");
        }
        return res.json();
      })
      .then((res) => {
        console.log("Added successfully");
        setAddRepo(false);
      })
      .catch((res) => {
        setError(true);
        setRepo("");
      });
  };
  return (
    <div className="issues">
      <div className="add_repo">
        {addRepo && (
          <>
            <InputForm
              type="text"
              id="repository"
              labelName="Repository"
              value={repo}
              onInputChange={handleInputChange}
            />
            <div className="add_repo_btn">
              <Button text="Save" onPress={handleAddRepo} />
            </div>
          </>
        )}
        {error && (
          <p style={{ color: "red" }}>
            Error while saving the repo, Please try again!
          </p>
        )}
      </div>
      {!addRepo && (
        <>
          <div className="add_org_button">
            <Button text="Add Repository" onPress={handleAddNew} />
          </div>
        </>
      )}
      <div className="table_card_heading">
        {tableHeadings.map(({ headingTitle }) => (
          <h4>{headingTitle}</h4>
        ))}
      </div>
      {loading && <p className="loading_message">Loading the data!!!</p>}
      {!loading && !issueData.length && (
        <p className="loading_message">No data found.</p>
      )}
      {!loading && !issueData && issueDataError && (
        <p className="loading_message">Error while fetching the data.</p>
      )}
      {issueData.length &&
        issueData.map(
          ({
            organisation_name,
            repository_name,
            created_issue_id,
            duplicate_issue_id,
          }) => (
            <TableCard
              key={uuidv4()}
              orgName={organisation_name}
              repoName={repository_name}
              openIssue={created_issue_id}
              contributors={duplicate_issue_id}
            />
          )
        )}
    </div>
  );
};

export default Issues;
