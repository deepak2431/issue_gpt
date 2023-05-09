import React from "react";
import Sidebar from "../components/Sidebar";
import Settings from "./Settings";

const Overview = () => {

    return(
        <div className="overview">
            <div className="overview_sidebar">
                <Sidebar />
            </div>
            <div className="settings">
                <Settings />
            </div>
        </div>
    )
}

export default Overview;