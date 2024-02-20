import React from "react";
import "./Select.css"

export default function Select({ options, handleSelection, display, name, selectedType }) {
    return (
        <div className="Select--Container" style={{ display: display ? "block" : "none" }}>
            <select className="select-options" onChange={(e) => {
                handleSelection(e, name)
            }} value={selectedType}>
                {options.map(option => (
                    <option value={option} key={option}>{option}</option>
                ))}
            </select>
        </div>
    )
}
