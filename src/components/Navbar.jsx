import {Link} from "react-router-dom";
import { Menu, MenuButton, MenuItems, MenuItem, Transition } from '@headlessui/react';
import { Fragment } from 'react';
import {
    FaBars,
    FaTimes,
    FaHome,
    FaUsers,
    FaCalendarAlt,
    FaUser,
    FaCog
} from 'react-icons/fa';

function MobileMenu() {
    const menuItems = [
        { icon: FaHome, label: 'Home', href: '/' },
        { icon: FaUsers, label: 'Communities', href: '/communities' },
        { icon: FaCalendarAlt, label: 'Events', href: '/events' },
        { icon: FaUser, label: 'Profile', href: '/profile' },
        { icon: FaCog, label: 'Settings', href: '/settings' },
    ];

    return (
        <Menu as="div" className="md:hidden">
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
                            {menuItems.map((item) => {
                                const Icon = item.icon;

                                return (
                                    <MenuItem key={item.label}>
                                        {({ focus }) => (
                                            <a
                                                href={item.href}
                                                className={`${
                                                    focus ? 'bg-primary/10 text-primary' : 'text-gray-700'
                                                } flex items-center gap-4 p-4 text-lg font-medium border-b border-gray-100 last:border-0`}
                                            >
                                                <Icon className="w-6 h-6" />
                                                <span>{item.label}</span>
                                            </a>
                                        )}
                                    </MenuItem>
                                );
                            })}

                            <div className="p-4 border-t border-gray-100">
                                <button className="w-full bg-primary text-white py-3 rounded-lg font-medium hover:bg-primary/90 transition-colors">
                                    Join Village
                                </button>
                            </div>
                        </MenuItems>
                    </Transition>
                </>
            )}
        </Menu>
    );
}
export default function Navbar() {
    return (
        <div className="flex justify-between items-center bg-white px-[var(--space-margin)] py-3 ">
            <div>
                <h2 className="Logo">Village </h2>
            </div>
            <nav className="hidden lg:block ">
                <ul className="flex-center gap-8 nav-links">
                    <li><Link to="/">Home</Link></li>
                    <li><a href="#about">About Us</a></li>
                    <li><Link to="/">Contact Us</Link></li>
                </ul>
            </nav>
            <div className="hidden lg:block">
                <Link to="/login" className="font-[500] text-black login">Login</Link>
                <Link to="/signup" className="button--primary ml-4 lg:py-1.6 px-5.5"> Create Account</Link>
            </div>
            <MobileMenu/>

        </div>
    )
}