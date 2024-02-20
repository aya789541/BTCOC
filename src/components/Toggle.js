import React from "react";
import "./Toggle.css"


export default function Toggle({toggle, handleToggleChange, title}){
     
    return(
        <div className="toggle--Card">
            <h1 className="toggle--title">{title ? title : "Nothing"}</h1>
            <div className="toggle--container" onClick={()=>handleToggleChange(title)}>
                <div className={`toggle--btn ${!toggle ? "disable" : ""}`}>
                {toggle ? "ON" : "OFF"}
                </div>

            </div>
        </div>
    )

}