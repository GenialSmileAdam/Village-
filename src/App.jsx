import {BrowserRouter, Routes, Route} from "react-router-dom";
import Home from './pages/Home';
import Signup from './pages/Signup';
import Login from './pages/Login';
import Navbar from "./components/Navbar.jsx";
import Footer from "./components/Footer.jsx";
export default function App() {
    return (
        <BrowserRouter>
            <Navbar/>
            <Routes>
                <Route path="/" element={<Home/>} />
                <Route path="/signup" element={<Signup/>}/>
                <Route path="/login" element={<Login/>}/>
            </Routes>
            <Footer/>
        </BrowserRouter>
    )
}