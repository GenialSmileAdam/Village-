import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { signup } from "../api/auth";
import Head from "../components/Head.jsx";
import { useState } from "react";

export default function SignUp() {
    const {
        register,
        handleSubmit,
        reset,
        formState: { errors, isSubmitting },
        getValues
    } = useForm();

    const [signupError, setSignupError] = useState(null);
    const [successMessage, setSuccessMessage] = useState(null);
    const navigate = useNavigate();

    const onSubmit = async (data) => {
        // Remove confirm_password before sending to API
        const {  ...signupData } = data;

        console.log("FORM DATA:", signupData);
        setSignupError(null);

        try {
            const res = await signup(signupData);
            console.log("API RESPONSE:", res.data);

            // Show success message
            setSuccessMessage("Account created successfully!");

            // Option 2: Redirect to log in (safer)
            setTimeout(() => navigate("/login"), 2000);

            reset(); // Reset form after successful submission

        } catch (err) {
            console.error("API ERROR:", err.response || err);

            // Extract error message from API response
            const message = err.response?.data?.message ||
                err.response?.data?.errors?.message ||
                err.message ||
                "An unexpected error occurred";

            setSignupError(message);
        }
    };

    return (
        <main className="h-fit lg:flex">
            <Head title="SignUp" />
            <div className="auth-panel lg:w-1/2 bg-[var(--color-secondary)] flex-col flex-center">
                <h2 className="stroke-0 text-black font-[200]">Join your Village!</h2>
                <p className="text-center mt-4 text-[20px] font-secondary text-black">
                    Connect with communities that share your <br/>
                    passions and interests.
                </p>
            </div>

            <div className="py-16 margin lg:w-1/2">
                <h2>Create Account</h2>
                <p className="mt-3">Get ready to find your village people</p>

                {/* Success Message */}
                {successMessage && (
                    <div className="mt-4 p-3 bg-green-100 text-green-700 rounded">
                        {successMessage} Redirecting to login...
                    </div>
                )}

                {/* Error Message */}
                {signupError && (
                    <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
                        {signupError}
                    </div>
                )}

                <form className="mt-9 form" onSubmit={handleSubmit(onSubmit)}>
                    <div className="form_input">
                        <label>Full Name:</label>
                        <input
                            type="text"
                            className="border"
                            placeholder="Jason Hughes"
                            {...register("full_name", {
                                required: "Enter your Full Name",
                                minLength: { value: 2, message: "Name must be at least 2 characters" },
                                maxLength: { value: 50, message: "Name is too long" }
                            })}
                        />
                        {errors.full_name && (
                            <p className="text-red-500 text-sm mt-2">{errors.full_name.message}</p>
                        )}
                    </div>

                    <div className="form_input">
                        <label>Username:</label>
                        <input
                            type="text"
                            className="border"
                            placeholder="@jason_hughes"
                            {...register("username", {
                                required: "Enter a Username",
                                minLength: { value: 3, message: "Username must be at least 3 characters" },
                                maxLength: { value: 20, message: "Username is too long" },
                                pattern: {
                                    value: /^[a-zA-Z0-9_]+$/,
                                    message: "Username can only contain letters, numbers, and underscores"
                                }
                            })}
                        />
                        {errors.username && (
                            <p className="text-red-500 text-sm mt-2">{errors.username.message}</p>
                        )}
                    </div>

                    <div className="form_input">
                        <label>Email Address:</label>
                        <input
                            type="email"
                            className="border"
                            placeholder="jasonhughes@gmail.com"
                            {...register("email", {
                                required: "Enter your Email Address",
                                pattern: {
                                    value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                                    message: "Invalid email address"
                                }
                            })}
                        />
                        {errors.email && (
                            <p className="text-red-500 text-sm mt-2">{errors.email.message}</p>
                        )}
                    </div>

                    <div className="form_input">
                        <label>Password:</label>
                        <input
                            type="password"
                            className="border"
                            {...register("password", {
                                required: "Password is Required",
                                validate: {
                                    minLength: (value) =>
                                        value.length >= 8 || "At least 8 characters required",
                                    hasUpper: (value) =>
                                        /[A-Z]/.test(value) || "Must contain one uppercase letter",
                                    hasLower: (value) =>
                                        /[a-z]/.test(value) || "Must contain one lowercase letter",
                                    hasNumber: (value) =>
                                        /\d/.test(value) || "Must contain one number",
                                    hasSpecial: (value) =>
                                        /[!@#$%^&*(),.?":{}|<>]/.test(value) ||
                                        "Must contain one special character (!@#$%^&* etc.)",
                                }
                            })}
                        />
                        {errors.password && (
                            <p className="text-red-500 text-sm mt-1">{errors.password.message}</p>
                        )}
                    </div>

                    <div className="form_input">
                        <label>Confirm Password:</label>
                        <input
                            type="password"
                            className="border"
                            {...register("confirm_password", {
                                required: "Please confirm your password",
                                validate: (value) =>
                                    value === getValues("password") || "Passwords do not match",
                            })}
                        />
                        {errors.confirm_password && (
                            <p className="text-red-500 text-sm mt-1">{errors.confirm_password.message}</p>
                        )}
                    </div>

                    <div className="flex gap-2 mt-4">
                        <input
                            type="checkbox"
                            {...register("agree_to_terms", {
                                required: "You must agree to the Terms of Service"
                            })}
                        />
                        <p className="text-[12px]">
                            I agree to the <Link to="/terms" className="text-primary">Terms of Service</Link> and <Link to="/privacy" className="text-primary">Privacy Policy</Link>
                        </p>
                    </div>
                    {errors.agree_to_terms && (
                        <p className="text-red-500 text-sm mt-1">{errors.agree_to_terms.message}</p>
                    )}

                    <div className="w-full flex-center mt-4 ">
                        <button
                            disabled={isSubmitting || successMessage}
                            type="submit"
                            className="button--primary h-[50px] w-[350px] min-w-0 sm:w-100 sm:min-w-85"
                        >
                            {isSubmitting ? "Creating Account..." : "Create Account"}
                        </button>
                    </div>

                    <p className="text-center mt-4">
                        Already have an account? <Link to="/login"><span className="text-primary login_v2">Sign In</span></Link>
                    </p>
                </form>
            </div>
        </main>
    );
}