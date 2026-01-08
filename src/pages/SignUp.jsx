import { FaMapLocationDot, FaUsers, FaStar, FaTrophy, FaHeart, FaTree, FaSeedling} from "react-icons/fa6";
import { Link } from "react-router-dom"; 

export default function SignUp() {
    return (
        <main className="h-fit lg:flex">
            <div className="auth-panel lg:w-1/2 bg-[var(--color-secondary)] flex-col flex-center ">
                <h2 className="stroke-0 text-black font-[200]">Join your Village!</h2>
                <p className="text-center mt-4 text-[20px] font-secondary text-black">Connect with communities that share your <br/>
                passions and interests.</p>
            </div>
            <div className="py-6 margin lg:w-1/2">

                <h2>Create Account</h2>
                <p className="mt-3">Get ready to find your village people</p>
                <form className="mt-9 form">
                    <div className="form_input">
                        <label htmlFor="">Full Name:</label>
                        <input type="text" className="border" placeholder="Jason Hughes"></input>
                    </div>
                    <div className="form_input">
                        <label htmlFor="">Username:</label>
                        <input type="text" className="border"
                        placeholder="@jason_hughes"></input>
                    </div>
                    <div className="form_input">
                        <label htmlFor="">Email Address:</label>
                        <input type="email" className="border"
                        placeholder="jasonhughes@gmail.com"></input>
                    </div>
                    <div className="form_input">
                        <label htmlFor="">Password:</label>
                        <input type="password" className="border"></input>
                    </div>
                    <div className="form_input" >
                        <label htmlFor="">Confirm Password:</label>
                        <input type="password" className="border"></input>
                    </div>
                    
                    <div className="flex gap-2 mt-4">
                        <input type="checkbox" />
                        <p className="text-[12px]">I agree to the Terms of Service and Privacy Policy</p>
                    </div>
                    <div className="w-full flex-center">
                    <button type="submit" className="button--primary w-[300px] ">Create Account</button></div>

                    <p className="text-center">Already have an account? <Link to="/login"><span className="text-primary login_v2">Sign In</span></Link></p>
                </form>
            </div>
        </main>
    )
}