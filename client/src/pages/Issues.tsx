import React, { useState, useEffect } from "react";
import { v4 as uuidv4 } from "uuid";

import TableCard from "../components/TableCard";
import InputForm from "../components/InputForm";
import Button from "../components/Button";

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

const SERVER_URL =
  "https://8f4c-2401-4900-3cdc-583c-d81a-b569-b6e5-5a01.ngrok-free.app";

const Issues = () => {
  const [repo, setRepo] = useState("");
  const [error, setError] = useState(0);
  const [addRepo, setAddRepo] = useState(0);
  const [success, setSuccess] = useState(0);
  const [issueData, setIssueData] = useState([]);

  const getIssueData = async () => {
    try {
      const resp = await fetch(
        SERVER_URL + "/duplicate_issues?org_name=deepak"
      );
      if (resp.status === 200) {
        const data = await resp.json();
        setIssueData(data.duplicate_issues);
      } else {
        throw Error("Unable to fetch the data");
      }
    } catch (error) {
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
    setAddRepo(1);
    setError(0);
    setRepo("");
    setSuccess(0);
  };

  const handleAddRepo = () => {
    setError(0);
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
        setSuccess(1);
        setAddRepo(0);
      })
      .catch((res) => {
        setError(1);
        setRepo("");
      });
  };
  return (
    <div className="issues">
      <div className="add_repo">
        {addRepo === 1 && (
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
        {error === 1 && (
          <p style={{ color: "red" }}>
            Error while saving the repo, Please try again!
          </p>
        )}
      </div>
      {addRepo === 0 && (
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
      {issueData.map(
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
