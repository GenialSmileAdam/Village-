import village from "/imgs/village.jpg"
import Card from "../components/Card.jsx"
import { FaMapLocationDot, FaUsers, FaStar, FaTrophy, FaHeart, FaTree, FaSeedling} from "react-icons/fa6";
import {FaHome} from "react-icons/fa";
import { Link } from "react-router-dom";
import Head  from "../components/Head.jsx"


function Hero(){
    return(
        <section className="h-92.5 flex flex-col justify-center items-start gap-3 overflow-hidden lg:h-[90vh]">
            <Head title="Home" />

            <div className="hero-gradient-bg"></div>
            <div className="floating-icons">
                <FaUsers className="icon icon-1" />
                <FaHeart className="icon icon-2" />
                <FaHome className="icon icon-3" />
                <FaTree className="icon icon-4" />
                <FaSeedling className="icon icon-5" />
                <FaUsers className="icon icon-6" />
            </div>

            <h1>Find your people, <br/> Find your village</h1>
            <p>Join a community where you find people <br/> with your similar interests </p>
        </section>
    )
}

function About(){
    return(
        <section id="about">
            <h2>About Village</h2>
            <div className="lg:flex justify-aroundt gap-3 lg:pt-5">

                <img src={village} alt="picture of a village" className=" h-62.5 w-full rounded-card  mt-4 border object-cover object-center lg:w-1/2 "/>

                <p className="mt-5 lg:w-1/2">
                    Village is a interactive community where people get to meet people that they share similar interests with and they all hangout in a group called “Village”.<br/><br/>
                    Village was founded in 2025 by Jason Oladipo Hughes in the basement of his mother’s house.<br/><br/>
                    Village has set a goal to help every man and woman to find a friend
                    with their similar interest so the world doesn't get filled with gay men.</p>
            </div>
        </section>
    )
}

function Features(){
    return(
        <section className="section-space">
            <h2>Features</h2>
            <p className="mt-3">What makes Villages different from other communities.</p>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-4">
                <Card
                    icon={<FaMapLocationDot className="text-6xl text-green-600" />}
                    title="Local People Finder"
                    description="You can be able to socialize with people that are with a certain range from you"/>
                <Card
                    icon={<FaUsers className="text-6xl text-green-600" />}
                    title="Interest Groups"
                    description="Join local groups based on hobbies, professions, or passions. From book clubs to hiking teams"
                />
                <Card
                    icon={<FaTrophy className="text-6xl text-yellow-600" />}
                    title="Community Rewards"
                    description="Earn badges and rewards for being active, organizing events, and helping neighbors"
                />
                <Card
                    icon={<FaStar className="text-6xl text-amber-600" />}
                    title="Local Guides"
                    description="Crowdsourced recommendations for best cafes, parks, doctors, and services in your area"
                />
            </div>

        </section>
    )
}

function CTA(){
    return(
        <section className="section-space cta lg:w-1/2 "> 
            <h2>Ready to Find Your Village?</h2>
            <p className="mt-3">Join Thousands of people connecting through shared interests and passions</p>
            <Link to="/signup" className="button--primary mt-5"> Join a Village!</Link>
        </section>
    )
}

export default function Home() {
    return (
        <main className="grow pb-12">
            <Hero/>
            <div className="bg-background-secondary rounded-card py-5">
                <About/>
                <Features/>
            </div>
            <CTA/>
        </main>
    )
}