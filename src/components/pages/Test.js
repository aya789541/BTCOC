import React, { useEffect, useState } from "react";
import { Chart as ChartJS} from "chart.js/auto";
import {Bar} from "react-chartjs-2"
import './Test.css'
import TextField from "../TextField";
import { eel } from "../../eel.js"

function MCQ({ question, options, onSelect, selectedOptions1, name , offset}) {

    const handleOptionChange = (option, name) => {
       onSelect(option, name)
    };

    return (
        <div className="MCQ">
            <h3>{question}</h3>
            <ul>
                {options.map((option, index) => (
                    <li key={index + offset}>
                        <div className="checkbox-wrapper-24">
                            <input 
                                type="checkbox"
                                id={`check-${index + offset}`} // Use dynamic IDs
                                name="check"
                                value={option}
                                checked={selectedOptions1.includes(option)}
                                onChange={() => handleOptionChange(option, name)} // Pass only option
                            />
                            <label htmlFor={`check-${index + offset}`}> {/* Use dynamic htmlFor */}
                                <span></span>{option}
                            </label>
                        </div>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default function Test() {
    const [connectionArrayTimeAuth, setConnectionArrayTimeAuth] = useState([]);
    //const [latencyArrayTimeAuth, setLatencyArrayTimeAuth] = useState([]);
    const [connectionArrayTimeNoAuth, setConnectionArrayTimeNoAuth] = useState([]);
    const [Xlabels, setXlabels] = useState([])
    const [clientOptions, setClientOptions] = useState([]);
    const [serverOptions, setServerOptions] = useState([]);
    const [choosedClientKeys, setChoosedClientKeys] = useState([]);
    const [choosedServerKeys, setChoosedServerKeys] = useState([]);
    const [brokerIp, setBrokerIP] = useState("");
    const [testing, setTesting] = useState(false)
    let tmpfunc;

    function handleTextField(placeHolder, value){
        switch(placeHolder){
            case "Broker @IP":
                setBrokerIP(value)
                eel.setBrokerIP(value)
                break
        }
    }

    async function GetConnectionTime(){
        setXlabels(await eel.getX_labels()())
        setConnectionArrayTimeAuth(await eel.getConnection_Times()())
    }


    async function hadnleConnect(){
        if (!testing){
            eel.Connection_Time_Test()
            tmpfunc = setInterval(GetConnectionTime, 100)
        }
        else{
            clearInterval(tmpfunc)
        }
        setTesting(!testing)
    }


    useEffect(() => {
        const getValues = async () => {
            setChoosedClientKeys(await eel.getTest_Client_keys()());
            //console.log(await eel.getTest_Client_keys()())
            //console.log(choosedClientKeys)
            setChoosedServerKeys(await eel.getTest_Server_keys()());
            setServerOptions(await eel.getServerKeyTypes()());
            setClientOptions(await eel.getClientKeyTypes()());
            setBrokerIP(await eel.getBrokerIP()())
        };

        getValues();
        //console.log(choosedClientKeys)

            
        
        
        }, []);

    const handleSelectOption = (option, name) => {
        if (name === "Server") {
            let tmp;
            const is_selected = choosedServerKeys.includes(option)
            is_selected ? tmp = choosedServerKeys.filter( element => element !=option) : tmp = [...choosedServerKeys, option];
            eel.setTest_Server_keys(tmp);
            setChoosedServerKeys(tmp);

        } else if (name === "Client") {
            let tmp;
            const is_selected = choosedClientKeys.includes(option)
            is_selected ? tmp = choosedClientKeys.filter( element => element !=option) : tmp = [...choosedClientKeys, option];
            eel.setTest_Client_keys(tmp);
            setChoosedClientKeys(tmp);
        }
    };

    return (
        <div className="Test--Container">
            <div className="Test--card">
            {!testing && (
                <div>
                    <div className="Walo">
                        <TextField placeHolder="Broker @IP" display={true} value={brokerIp} handleTextField={handleTextField} />
                    </div>
                    <div className="QCMs">
                        <MCQ
                            question="Client keys"
                            options={clientOptions}
                            onSelect={handleSelectOption}
                            selectedOptions1={choosedClientKeys}
                            name="Client"
                            offset={0}
                        />
                        <MCQ
                            question="Server keys"
                            options={serverOptions}
                            onSelect={handleSelectOption}
                            selectedOptions1={choosedServerKeys}
                            name="Server"
                            offset={clientOptions.length}
                        />
                    </div>
                </div>
            )}
                
                {testing && (
                    <Bar
                    style={{ paddingRight: '60px' }}
                    className="Bargrarph"
                    data={{
                        labels: Xlabels,
                        datasets: [
                            {
                                label: "Connection Time",
                                data: connectionArrayTimeAuth,
                                backgroundColor: 'rgba(255, 99, 132, 0.2)', // Example color for bars
                                borderColor: 'rgba(255, 99, 132, 1)', // Example border color for bars
                                borderWidth: 1,
                            },
                        ],
                    }}
                    options={{
                        plugins: {
                            legend: {
                                display: true,
                                position: 'top', // Change position if needed
                            },
                        },
                        scales: {
                            y: {
                                ticks: {
                                    font: {
                                        size: 10, // Adjust font size for Y-axis labels
                                    },
                                },
                            },
                            x: {
                                ticks: {
                                    font: {
                                        size: 10, // Adjust font size for X-axis labels
                                    },
                                },
                            },
                        },
                    }}
                />
                
                )}
                <div className={`connect-btn ${testing ? "connect" : ""}`} onClick={hadnleConnect}>{testing? "Stop test" : "launch test"}</div>
            </div>
            <div className="Test--card">
                <Bar
                    data={{
                        labels: ["A", "B", "C"],
                        datasets: [
                            {
                                label: "Revenue",
                                data: [200, 300, 400],
                            },
                        ],
                    }}
                />
            </div>
        </div>
    );
}

