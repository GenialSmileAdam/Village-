import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { login } from "../api/auth";
import Head from "../components/Head.jsx";
import { useAuth } from "../Context/AuthContext"; // Add this import
import { useState } from "react";

export default function Login() {
    const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm();
    const navigate = useNavigate();
    const { setUser } = useAuth(); // Get setUser from auth context
    const [loginError, setLoginError] = useState("");

    const onSubmit = async (data) => {
        setLoginError("");

        try {
            const res = await login(data);
            console.log(res.data);

            // Store token
            localStorage.setItem("token", res.data.access_token);

            // Update user state in context
            if (res.data.user) {
                setUser(res.data.user);
            }

            alert("Login Successful!");
            navigate("/");
        } catch (err) {
            console.error("API ERROR:", err.response || err);
            const errorMessage = err.response?.data?.message || "Login failed. Please check your credentials.";
            setLoginError(errorMessage);
        }
    };

    return (
        <main className="lg:flex">
            <Head title="Login" />
            <div className="auth-panel lg:w-1/2 bg-[var(--color-secondary)] flex-col flex-center">
                <h2 className="stroke-0 text-black font-[200]">Welcome Back</h2>
                <p className="text-center mt-4 text-[20px] font-secondary text-black">
                    Sign in to reconnect with your community and continue meaningful conversations.
                </p>
            </div>
            <div className="py-16 margin lg:w-1/2">
                <h2>Sign In</h2>
                <p className="mt-3">Enter your credentials to access your account</p>

                {loginError && (
                    <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
                        {loginError}
                    </div>
                )}

                <form className="mt-9 form" onSubmit={handleSubmit(onSubmit)}>
                    <div className="form_input">
                        <label>Username or Email:</label>
                        <input
                            type="email"
                            className="border"
                            placeholder="Enter Username or Email"
                            {...register("email", { required: "Email is required" })}
                        />
                        {errors.email && <p className="text-red-500 text-sm mt-2">{errors.email.message}</p>}
                    </div>

                    <div className="form_input">
                        <label>Password:</label>
                        <input
                            type="password"
                            className="border"
                            {...register("password", { required: "Password is required" })}
                        />
                        {errors.password && <p className="text-red-500 text-sm mt-2">{errors.password.message}</p>}
                    </div>

                    <div className="flex justify-between mt-[-1em]">
                        <div className="flex">
                            <input type="checkbox" {...register("remember_me")} />
                            <p className="text-[14px] ml-3">Remember Me</p>
                        </div>
                        <p className="text-[12px]">Forgot Password?</p>
                    </div>

                    <div className="w-full flex-col gap-[1rem] flex-center">
                        <button
                            type="submit"
                            className="button--primary w-[300px]"
                            disabled={isSubmitting}
                        >
                            {isSubmitting ? "Signing in..." : "Sign In"}
                        </button>

                        <div className="w-[300px] flex items-center gap-3">
                            <div className="flex-1 h-px bg-gray-300"></div>
                            <span className="text-[var(--color-text-primary)]">OR</span>
                            <div className="flex-1 h-px bg-gray-300"></div>
                        </div>

                        <button
                            type="button"
                            className="button--primary w-[300px] bg-white border-0"
                            onClick={() => window.location.href = "/auth/google"} // Or your Google OAuth URL
                        >
                            Continue with Google
                        </button>
                    </div>

                    <p className="text-center">
                        Don't have an account? <Link to="/signup"><span className="text-primary login_v2">Create one</span></Link>
                    </p>
                </form>
            </div>
        </main>
    );
}