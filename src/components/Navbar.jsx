import { Link, useNavigate } from "react-router-dom";
import { Menu, MenuButton, MenuItems, MenuItem, Transition } from '@headlessui/react';
import { Fragment } from 'react';
import { useAuth } from "../context/AuthContext.jsx"; // Fixed import path
import api from "../api/axios";
import {
    FaBars,
    FaTimes,
    FaHome,
    FaUsers,
    FaCalendarAlt,
    FaUser,
    FaSignOutAlt,
    FaCog
} from 'react-icons/fa';

function MobileMenu({ user, handleLogout }) {
    // Dynamic menu items based on auth status
    const getMenuItems = () => {
        const items = [
            { icon: FaHome, label: 'Home', href: '/' },
            { icon: FaUsers, label: 'Communities', href: '/communities' },
            { icon: FaCalendarAlt, label: 'Events', href: '/events' },
        ];

        if (user) {
            items.push(
                { icon: FaUser, label: 'Profile', href: '/profile' },
                { icon: FaCog, label: 'Settings', href: '/settings' }
            );
        } else {
            items.push({ icon: FaUser, label: 'Login', href: '/login' });
        }

        return items;
    };

    return (
        <Menu as="div" className="lg:hidden">
            {({ open }) => (
                <>
                    <MenuButton className="p-2 hover:bg-gray-100 rounded-lg transition-colors">
                        {open ? (
                            <FaTimes className="w-6 h-6 text-gray-700" />
                        ) : (
                            <FaBars className="w-6 h-6 text-gray-700" />
                        )}
                    </MenuButton>

                    <Transition
                        as={Fragment}
                        enter="transition ease-out duration-100"
                        enterFrom="transform opacity-0 scale-95"
                        enterTo="transform opacity-100 scale-100"
                        leave="transition ease-in duration-75"
                        leaveFrom="transform opacity-100 scale-100"
                        leaveTo="transform opacity-0 scale-95"
                    >
                        <MenuItems
                            anchor="bottom end"
                            className="absolute right-4 top-16 w-64 bg-white rounded-xl shadow-2xl border border-gray-200 py-2 z-50"
                        >
                            {getMenuItems().map((item) => {
                                const Icon = item.icon;

                                return (
                                    <MenuItem key={item.label}>
                                        {({ focus }) => (
                                            <Link
                                                to={item.href}
                                                className={`${
                                                    focus ? 'bg-primary/10 text-primary' : 'text-gray-700'
                                                } flex items-center gap-4 p-4 text-lg font-medium border-b border-gray-100 last:border-0 transition-colors`}
                                            >
                                                <Icon className="w-6 h-6" />
                                                <span>{item.label}</span>
                                            </Link>
                                        )}
                                    </MenuItem>
                                );
                            })}

                            {user && (
                                <MenuItem>
                                    {({ focus }) => (
                                        <button
                                            onClick={handleLogout}
                                            className={`${
                                                focus ? 'bg-red-50 text-red-600' : 'text-gray-700'
                                            } flex items-center gap-4 p-4 text-lg font-medium w-full text-left border-t border-gray-100 transition-colors`}
                                        >
                                            <FaSignOutAlt className="w-6 h-6" />
                                            <span>Logout</span>
                                        </button>
                                    )}
                                </MenuItem>
                            )}

                            <div className="p-4 border-t border-gray-100">
                                {!user && (
                                    <Link
                                        to="/signup"
                                        className="button--primary w-full py-3 flex-center"
                                    >
                                        Join a Village!
                                    </Link>
                                )}
                            </div>
                        </MenuItems>
                    </Transition>
                </>
            )}
        </Menu>
    );
}

export default function Navbar() {
    const { user, setUser } = useAuth();
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await api.delete("/logout");
        } catch (e) {
            console.error(e);
        }
        localStorage.removeItem("token");
        setUser(null);
        navigate("/");
    };


    return (
        <div className="flex justify-between items-center bg-white px-(--space-margin) py-3">
            <div>
                <Link to="/">
                    <h2 className="Logo">Village</h2>
                </Link>
            </div>

            <nav className="hidden lg:block">
                <ul className="flex-center gap-8 nav-links">
                    <li><Link to="/">Home</Link></li>
                    <li><a href="#about">About Us</a></li>
                    <li><Link to="/contact">Contact Us</Link></li>
                </ul>
            </nav>

            {user ? (
                <div className="hidden lg:flex items-center gap-4">
                    <span className="text-gray-700 font-medium">
                        Hello, {user.username || user.email}
                    </span>
                    <button
                        onClick={handleLogout}
                            className="px-6 py-3 bg-red-400 rounded-2xl text-sm text-white font-medium text-gray-700 hover:bg-red-600 transition-colors cursor-pointer"
                    >
                        Logout
                    </button>
                </div>
            ) : (
                <div className="hidden lg:block">
                    <Link to="/login" className="font-[500] text-black login">
                        Login
                    </Link>
                    <Link to="/signup" className="button--primary ml-4 lg:py-1.6 px-5.5">
                        Create Account
                    </Link>
                </div>
            )}

            <MobileMenu user={user} handleLogout={handleLogout} />
        </div>
    );
}