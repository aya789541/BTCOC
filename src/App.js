import React, { Component } from "react";
import "./App.css";
import Navbar from "./components/Navbar.js";
import { eel } from "./eel.js";
import { Route, Routes } from "react-router-dom";
import Configuration from "./components/pages/Configuration.js";
import Test from "./components/pages/Test.js";
import Map from "./components/pages/Map.js"
import Home from "./components/pages/Home.js";
class App extends Component {
  constructor(props) {
    super(props);
    eel.set_host("ws://localhost:8888"); }
  render() {
    return <div>

      <Navbar />
      <Routes>
        <Route path="/" element={<Home />}/>
        <Route path="/Configuration" element={<Configuration />}/>
        <Route path="/Map" element={<Map />}/>
        <Route path="/Test" element={<Test />}/>
      </Routes>
    </div>
  }
}

export default App;
