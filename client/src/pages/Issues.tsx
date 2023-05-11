import React from "react"

import TableCard from '../components/TableCard';

const tableHeadings = [
    {
        headingTitle: 'Organization Name'
    },
    {
        headingTitle: 'Repository Name'
    },
    {
        headingTitle: 'Open issues'
    },
    {
        headingTitle: 'Active contributors'
    },
]

const Issues = () => {
    return(
        <div className="issues">
            <div className='table_card_heading'>
                {
                    tableHeadings.map(({headingTitle}) => (
                        <h4>{headingTitle}</h4>
                    ))
                }
            </div>
            <TableCard 
            orgName='Deepak'
            repoName='Django'
            openIssue='500'
            contributors='10'
            />
        </div>
    )
}

export default Issues;