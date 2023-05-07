import React from "react";
import Sidebar from "../components/Sidebar";
import InputForm from "../components/InputForm";

const Overview = () => {

    return(
        <div className="overview">
            <div className="overview_sidebar">
                <Sidebar />
            </div>
            <div className="overview_content">
                <InputForm />
            </div>
        </div>
    )
}

export default Overview;