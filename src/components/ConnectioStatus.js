import React from "react";
import ConnectedLogo from "../images/Connection Status On-595b40b65ba036ed117d3e64.svg";
import ConnectingLogo from "../images/Connecting.svg";
import "./ConnectionStatus.css";



export default function ConnectionStatus({status}){
    function icon(status){
        switch(status){
            case "connected":
                return ConnectedLogo
            case "connecting":
                return ConnectingLogo
            case "unconnected":
                return ConnectedLogo
        }
    }
        return(
            <div className="container--state" >
                
                <h1 className="connection--status">{status}</h1>
                <img className="Icon--conenction" src={icon(status)}/>

            </div>      
             
        )
}