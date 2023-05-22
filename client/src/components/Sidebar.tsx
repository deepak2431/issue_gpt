import React, { ReactNode } from "react";
import { Link } from "react-router-dom";
import {
  MdDashboardCustomize,
  MdList,
  MdSettings,
  MdAccountCircle,
} from "react-icons/md";

interface Navbar {
  name: string;
  icon: ReactNode;
  key: number;
  linkRoutes: string;
}

const sidebarNav: Navbar[] = [
  {
    name: "Dashboard",
    key: 1,
    icon: <MdDashboardCustomize className="sidebar_icon" />,
    linkRoutes: "overview",
  },
  {
    name: "Issues",
    key: 2,
    icon: <MdList className="sidebar_icon" />,
    linkRoutes: "issues",
  },
  {
    name: "Settings",
    key: 3,
    icon: <MdSettings className="sidebar_icon" />,
    linkRoutes: "settings",
  },
  {
    name: "Profile",
    key: 4,
    icon: <MdAccountCircle className="sidebar_icon" />,
    linkRoutes: "profile",
  },
];

const Sidebar = () => {
  return (
    <div className="sidebar">
      <p className="sidebar_header">IssueGPT</p>
      <div className="sidebar_nav">
        {sidebarNav.map(({ name, icon, key, linkRoutes }) => (
          <Link to={linkRoutes} style={{ textDecoration: "none" }}>
            <button className="btn-nav" key={key}>
              {icon}
              {name}
            </button>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default Sidebar;
