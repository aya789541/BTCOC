import React, {useState, useEffect} from "react";
import "./Configuration.css"
import TextField from "../TextField";
import Toggle from "../Toggle";
import Select from "../Select";
import { eel } from "../../eel.js"
import ConnectionStatus from "../ConnectioStatus.js";

export default function Configuration(){
    const [Authentication, setAuthentication] = useState(false);
    const [Encryption, setEncryption] = useState(false);
    const [brokerIp, setBrokerIP] = useState("");
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("")
    const [ClientKey, setClientKey] = useState("")
    const [ServerKey, setServerKey] = useState("")
    const [connected, setConnected] = useState(false)
    const [connecteing, setConnecting] = useState(false)
    const options = ["RSA_256", "RSA_512", "RSA_1024", "Curve448", "P-256"]
   
    async function hadnleConnect(){
        if (connected){
            await eel.disconnecte_Client()()
        }else{
            await eel.Connect_Client()()
            setConnecting(true)
            
        }
        setConnected(await eel.is_Connected()())
        setConnecting(false)
    }

    function handleToggleChange(title){
        if (title==="Authentication"){
            eel.setAuthentication(!Authentication)
            setAuthentication(!Authentication)
        }
        else if (title==="Encryption") {
            eel.setEncryption(!Encryption);
            setEncryption(!Encryption);

    }
    }

    function handleSelection(e, name){
        if (name == "Client"){
            eel.setKeyType(e.target.value, name)
            setClientKey(e.target.value)
        }
        else if(name == "Server"){
            eel.setKeyType(e.target.value, name)
            setServerKey(e.target.value)
        }
            
        e.target.value
    }

    function handleTextField(placeHolder, value){
        switch(placeHolder){
            case "Broker @IP":
                setBrokerIP(value)
                eel.setBrokerIP(value)
                break
            case "Username":
                setUsername(value)
                eel.setUsername(value)
                break
            case "Password":
                setPassword(value)
                eel.setPassword(value)
                break
        }
    }

    useEffect(()=>{

        const options = {
            enableHighAccuracy: true,
            maximumAge: 0,
          };
          
          function success(position) {
            const { latitude, longitude } = position.coords;
            eel.Set_position([latitude, longitude]);
          }
          
          function error(err) {
            console.warn(`ERROR(${err.code}): ${err.message}`);
          }
        const fetchposition = () =>{
            navigator.geolocation.getCurrentPosition(success, error, options);
        }
        
          

        const getValues = async ()=>{
            setEncryption(await eel.getEncryption()())
            setAuthentication(await eel.getAuthentication()())
            setBrokerIP(await eel.getBrokerIP()())
            setUsername(await eel.getUsername()())
            setPassword(await eel.getPassword()())
            setConnected(await eel.is_Connected()())
            setClientKey(await eel.getKeyType("Client")())
            setServerKey(await eel.getKeyType("Server")())
        }
        
        getValues()   
        const positionFetcher = setInterval(fetchposition, 500); 

        return () => clearInterval(positionFetcher);
    }
    ,[])


    return (
    <div className="Config--Container">
        
        <div className="Config--Card">
        <ConnectionStatus status={connecteing ? "connecting" : connected ? "connected" : "disconnected"}/>
            <div className="toggles--contianer">
                <Toggle toggle = {Encryption} handleToggleChange = {handleToggleChange} title ="Encryption"></Toggle>
                <Toggle toggle = {Authentication} handleToggleChange = {handleToggleChange} title ="Authentication"></Toggle>
            </div>
        <TextField placeHolder = "Broker @IP" display={true} value={brokerIp} handleTextField={handleTextField}/>
        <TextField placeHolder = "Username" display={Authentication} value={username} handleTextField={handleTextField}/>
        <TextField placeHolder = "Password" display={Authentication} value={password} handleTextField={handleTextField} />
        <Select options={options} handleSelection={handleSelection} display={Encryption} name="Client" selectedType={ClientKey}/>
        <Select options={options} handleSelection={handleSelection} display={Encryption} name="Server" selectedType={ServerKey}/>
        <div className={`connect-btn ${connected ? "connect" : ""}`} onClick={hadnleConnect}>{connected? "Disconnect" : "Connect"}</div>
        </div>
        
    </div>
    )
}