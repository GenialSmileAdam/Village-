import { FaMapLocationDot, FaUsers, FaStar, FaTrophy, FaHeart, FaTree, FaSeedling} from "react-icons/fa6";
import {Link, useNavigate} from "react-router-dom";
import { useForm } from "react-hook-form";
import { signup } from "../api/auth";
import  Head  from "../components/Head.jsx"
import {useState} from "react";



export default function SignUp() {

    const { register,
        handleSubmit,
        reset,
            formState:{errors, isSubmitting},
            getValues} = useForm();
    // const [error, setError] = useState(null);
    const navigate = useNavigate();
    const onSubmit = async (data) => {
        console.log("FORM DATA:", data);
        try {
            const res = await signup(data);
            console.log("API RESPONSE:", res.data);
            alert("Account created!");
            reset()
            navigate("/")
        } catch (err) {
            // const message = err.response?.data.errors?.message || err.message || "An unexpected error occurred";
            // setError(message);
            console.error("API ERROR:", err.response || err);
        }

        reset()
    };


    return (

        <main className="h-fit  lg:flex">
            <Head title="SignUp" />
            <div className="auth-panel lg:w-1/2 bg-[var(--color-secondary)] flex-col flex-center ">
                <h2 className="stroke-0 text-black font-[200]">Join your Village!</h2>
                <p className="text-center mt-4 text-[20px] font-secondary text-black">Connect with communities that share your <br/>
                passions and interests.</p>
            </div>
            <div className="py-16 margin lg:w-1/2">
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <h2>Create Account</h2>
                <p className="mt-3">Get ready to find your village people</p>
                <form className="mt-9 form" onSubmit={handleSubmit(onSubmit)}>
                    <div className="form_input">
                        <label htmlFor="">Full Name:</label>
                        <input type="text" className="border" placeholder="Jason Hughes" {...register("full_name", {required:"Enter your Full Name", min:5, max:5} )}></input>
                        {errors.full_name&&(<p className="text-red-500 text-sm mt-2">{`${errors.full_name.message}`}</p>)}
                    </div>

                    <div className="form_input">
                        <label htmlFor="">Username:</label>
                        <input type="text" className="border"
                        placeholder="@jason_hughes" {...register("username", {required:"Enter a Username", min:5, max:5})}></input>
                        {errors.username&&(<p className="text-red-500 text-sm mt-2">{`${errors.username.message}`}</p>)}

                    </div>

                    <div className="form_input">
                        <label htmlFor="">Email Address:</label>
                        <input type="email" className="border"
                        placeholder="jasonhughes@gmail.com" {...register("email", {required:"Enter your Email Address"})}></input>
                        {errors.email&&(<p className="text-red-500 text-sm mt-2">{`${errors.email.message}`}</p>)}
                    </div>

                    <div className="form_input">
                        <label htmlFor="">Password:</label>
                        <input type="password" className="border" {...register("password", {required:"Password is Required",validate: {
                                minLength: (value) =>
                                    value.length >= 8 || "At least 8 characters",
                                hasUpper: (value) =>
                                    /[A-Z]/.test(value) || "One uppercase letter",
                                hasLower: (value) =>
                                    /[a-z]/.test(value) || "One lowercase letter",
                                hasNumber: (value) =>
                                    /\d/.test(value) || "One number",
                                hasSpecial: (value) =>
                                    /[!@#$%^&*(),.?":{}|<>]/.test(value) ||
                                    "One special character (!@#$%^&* etc.)",

                            },   })}></input>
                    </div>
                    {errors.password&&(<p className="text-red-500 text-sm ">{`${errors.password.message}`}</p>)}

                    <div className="form_input" >
                        <label htmlFor="">Confirm Password:</label>
                        <input type="password" className="border" {...register("confirm_password", {
                            required: "Confirm Password is Required",
                            validate: (value) =>
                                value === getValues("password") || "Password must Match",
                        })}></input>
                    </div>
                    {errors.confirm_password && <p className="text-red-500 text-sm ">{`${errors.confirm_password.message}`}</p>}


                    <div className="flex gap-2 mt-4">
                        <input type="checkbox" value="True" {...register("agree_to_terms", {required:"True"})} />
                        <p className="text-[12px]">I agree to the Terms of Service and Privacy Policy</p>
                    </div>

                    <div className="w-full flex-center">
                    <button disabled={isSubmitting} type="submit" className="button--primary w-[300px] ">Create Account</button></div>

                    <p className="text-center">Already have an account? <Link to="/login"><span className="text-primary login_v2">Sign In</span></Link></p>
                </form>
            </div>
        </main>
    )
}