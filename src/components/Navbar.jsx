import {Link} from "react-router-dom";


export default function Navbar() {
    return (
        <div>
            <div>
                <h2>Village </h2>
            </div>
            <nav>
                <ul>
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/">About Us</Link></li>
                    <li><Link to="/">Contact Us</Link></li>
                </ul>
            </nav>
            <div>
                <a><Link to="/Login">Login</Link></a>
                <button><Link to="/SignUp"> Create Account</Link></button>
            </div>
        </div>
    )
}