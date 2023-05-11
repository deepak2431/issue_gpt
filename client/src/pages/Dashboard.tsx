import React from "react";
import { Outlet } from "react-router-dom";
import Sidebar from "../components/Sidebar";


const Dashboard = () => {

    return(
        <div className="overview">
            <div className="overview_sidebar">
                <Sidebar />
            </div>
            <Outlet />
        </div>
    )
}

export default Dashboard;