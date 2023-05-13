import React from 'react'
import { useSelector } from 'react-redux';
import { RootState } from '../redux';

const Overview = () => {

    const orgName = useSelector((state:RootState) => state.profile.orgName)
    return(
        <div className='overview_info'>
            <div className='overview_header'>
                <p>Welcome, {orgName} </p>
            </div>
            <div className='overview_metrics'>
                    <p>This is a section one component</p>
            </div>
            <div className='overview_metrics_info'>
                <div className='overview_section_1'>
                    <p>This is a section one component</p>
                </div>
                <div className='overview_section_2'>
                    <p>This is a section one component</p>
                </div>
            </div>
        </div>
    )
}

export default Overview;