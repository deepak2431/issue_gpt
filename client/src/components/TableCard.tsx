import React from "react";

interface IProps {
  orgName: string;
  repoName: string;
  openIssue: string;
  contributors: string;
}

const TableCard: React.FC<IProps> = ({
  orgName,
  repoName,
  openIssue,
  contributors,
}) => {
  return (
    <div className="table_card">
      <div className="table_content">
        <p>{orgName}</p>
        <p>{repoName}</p>
        <p>{openIssue}</p>
        <p>{contributors}</p>
      </div>
    </div>
  );
};

export default TableCard;
