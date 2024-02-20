import React from "react"
import "./TextField.css"

export default function TextField({placeHolder, display, value, handleTextField}){
    return (
    <div className="input--card" >
        <input className="input--field" value={value} onChange={(e) => handleTextField(placeHolder, e.target.value)} placeholder={placeHolder} style={{display: display? "block" : "none"}}></input>
    </div>
    )
}