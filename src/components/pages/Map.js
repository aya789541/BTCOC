import React, {useEffect, useState} from "react";
import "leaflet/dist/leaflet.css"
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import "./Map.css"
import { Icon } from "leaflet";
import LocationIcon from "../../images/pin-map.png"
import VehiculeIcon from "../../images/Car_icon.png"
import { eel } from "../../eel.js";

export default function Map(){
    const [position, setPosition] = useState(null);
    const [vehicule, setvehicules] = useState({});
    const locationIcon = new Icon({
        iconUrl : LocationIcon,
        iconSize : [30, 30],
    });
    const vehiculeIcon = new Icon({
        iconUrl : VehiculeIcon,
        iconSize : [30, 30]

        });


    useEffect(() => {

        const fetchVehiculePosition = async()=>{
            setvehicules( await eel.Get_Vehiculs_Location()())
        }
        const options = {
            enableHighAccuracy: true, // Request high accuracy
            maximumAge: 0 // Discard cached positions
          };
          
          const successCallback = (position) => {
              const { latitude, longitude } = position.coords;
              eel.Set_position([latitude, longitude]);
              setPosition([latitude, longitude]);
          };
          
          const errorCallback = (error) => {
            console.error(`Error getting location: ${error.message}`);
          };  

        const watchId = navigator.geolocation.watchPosition(successCallback, errorCallback, options);
        const vehiculeFetcher = setInterval(fetchVehiculePosition, 500);
        return ()=>{
            navigator.geolocation.clearWatch(watchId);
            clearInterval(vehiculeFetcher)
        
        }
      }, []);


    return (
    <div>
        {
            position && <MapContainer center={position} zoom={25}>
            <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {
                position && <Marker position={position} icon={locationIcon}>
                <Popup>Your Location</Popup>
                </Marker>
                
            }

            {
                vehicule && Object.keys(vehicule).map(_key => (
                    <Marker key={vehicule[_key].location.toString()} position={vehicule[_key].location} icon={vehiculeIcon}>
                        <Popup>{vehicule[_key].speed}</Popup>
                    </Marker>
                ))
    
            }
        </MapContainer>
    }
    </div>
    )
}