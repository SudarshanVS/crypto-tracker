import './App.css';

import {Routes, Route} from "react-router-dom";
import IntroForm from "./components/IntroForm";
import Dashboard from "./components/Dashboard";

function App() {
    return (
        <div className="App">
            <Routes>
                <Route path={"/"} element={<IntroForm/>}></Route>
                <Route path={"/dashboard"} element={<Dashboard/>}></Route>
            </Routes>
        </div>
    );
}

export default App;
