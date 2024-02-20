import React from "react";
import logo from "../images/Logo.jpg";
import {Link, NavLink} from "react-router-dom";
import "./Navbar.css";
export default function Navbar(){
    return (
    <nav>
        <div>
            <Link to="/" className="Logo">
            <img src={logo} className="Logo-image" />
            <h2 className="title"> BTCOC </h2>
            </Link>
        </div>
        

        <div>
            <ul>
                <li>
                    <NavLink to="/Configuration">Configuration</NavLink>
                </li>
                <li>
                    <NavLink to="/Map">Map</NavLink>
                </li>
                <li>
                    <NavLink to="/Test">Test</NavLink>
                </li>
            </ul>
        </div>
        
    </nav>
    )
}