import React, { ReactNode } from 'react';
import { MdDashboardCustomize, MdList, MdSettings, MdAccountCircle } from 'react-icons/md'

interface Navbar {
    name: string
    icon: ReactNode
}


const sidebarNav : Navbar[] = [
    {
        name: 'Dashboard',
        icon: <MdDashboardCustomize className='sidebar_icon' />,
    },
    {
        name: 'Issues',
        icon:<MdList className='sidebar_icon' />,
    },
    {
        name: 'Settings',
        icon: <MdSettings className='sidebar_icon' />,
    },
    {
        name: 'Profile',
        icon: <MdAccountCircle className='sidebar_icon' />,
    }

]

const Sidebar = () => {



    return(
        <div className='sidebar'>
            <p className='sidebar_header'>IssueGPT</p>
            <div className='sidebar_nav'>
                {
                    sidebarNav.map(({name, icon}) => (
                        <button className='btn-nav'>
                            {icon}
                            {name}
                        </button>
                    ))
                }
            </div>
        </div>
    )
}

export default Sidebar;