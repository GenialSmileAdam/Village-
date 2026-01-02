import { Link } from "react-router-dom"; 

export default function Login() {
    return (
        <main className="h-[87vh] lg:flex">
            <div className="auth-panel lg:w-1/2 bg-[var(--color-secondary)] flex-col flex-center ">
                <h2 className="stroke-0 text-black font-[200]">Welcome Back</h2>
                <p className="text-center mt-4 text-[20px] font-secondary text-black">Sign in to reconnect with your community and continue meaningful conversations.
                </p>
            </div>
            <div className="py-6 margin lg:w-1/2">

                <h2>Sign In</h2>
                <p className="mt-3">Enter your credentials to access your account</p>
                <form className="mt-9 form">
                  
                    <div className="form_input">
                        <label htmlFor="">Username or Email:</label>
                        <input type="text" className="border"
                        placeholder="Enter Username or Email"></input>
                    </div>
                    <div className="form_input">
                        <label htmlFor="">Password:</label>
                        <input type="password" className="border"
                       ></input>
                    </div>
                    
                    <div className="flex justify-between mt-[-1em]">
                        <div className="flex ">
                            <input type="checkbox" />
                            <p className="text-[12px]">Remember Me</p>
                        </div>
                        <p className="text-[12px]">Forgot Password?</p>
                    </div>
                    <div className="w-full flex-col gap-[1rem] flex-center">
                        <button type="submit" className="button--primary w-[300px] ">Sign In</button>
                        
                        <div className="w-[300px] flex items-center gap-3">
                            <div className="flex-1 h-px bg-gray-300"></div>
                            <span className="text-[var(--color-text-primary)]">OR</span>
                            <div className="flex-1 h-px bg-gray-300"></div>
                        </div>
                        
                        <button type="submit" className="button--primary w-[300px] bg-white border-0">Continue with Google  </button>
                    </div>

                    <p className="text-center">Dont have an account? <Link to="/signup"><span className="text-primary login_v2">Create one</span></Link></p>
                </form>
            </div>
        </main>

    )
}