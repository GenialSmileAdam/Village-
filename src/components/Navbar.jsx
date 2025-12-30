import {Link} from "react-router-dom";
import { GiHamburgerMenu } from "react-icons/gi";


export default function Navbar() {
    return (
        <div className="flex justify-between items-center bg-white px-[var(--space-margin)] py-3 ">
            <div>
                <p className="logo">Village </p>
            </div>
            <nav className="hidden lg:block ">
                <ul className="flex-center gap-8">
                    <li><Link to="/">Home</Link></li>
                    <li><Link to="/">About Us</Link></li>
                    <li><Link to="/">Contact Us</Link></li>
                </ul>
            </nav>
            <div className="hidden lg:block">
                <Link to="/login" className="font-[500] text-black">Login</Link>
                <Link to="/signup" > <button className="button--primary ml-4 lg:py-1.6 px-5.5"> Create Account</button> </Link>
            </div>
            <GiHamburgerMenu className="lg:hidden"/>

        </div>
    )
}