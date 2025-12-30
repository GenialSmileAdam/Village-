import village from "/imgs/village.jpg"
import Card from "../components/Card.jsx"
import { FaMapLocationDot } from "react-icons/fa6";


function Hero(){
    return(
        <section className="h-[370px] flex flex-col justify-center items-start gap-3 overflow-hidden lg:h-[90vh]">
            <h1>Find your people, <br/> Find your village</h1>
            <p>Join a community where you find people <br/> with your similar interests </p>
            <button className="button--primary mt-5">Join a Village!</button>

        </section>
    )
}

function About(){
    return(
        <section>
            <h2>About Village</h2>
            <div className="lg:flex justify-aroundt gap-3 lg:pt-5">

                <img src={village} alt="picture of a village" className=" h-[250px] w-full rounded-[10px]  mt-4 border object-cover object-center lg:w-1/2 "/>

                <p className="mt-5 lg:w-1/2">
                    Village is a interactive community where people get to meet people that they share similar interests with and they all hangout in a group called “Village”.<br/><br/>
                    Village was founded in 2025 by Jason Oladipo Hughes in the basement of his mother’s house.<br/><br/>
                    Village has set a goal to help every man and woman to find a friend
                    with their similar interest so the world dosen't get filled with gay men.</p>
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
                <Card name="Local People Finder" description="You can be able to socialize with people that are with a certain range from you"/>
                <Card/>
                <Card/>
                <Card/>
            </div>

        </section>
    )
}

function CTA(){
    return(
        <section className="section-space cta lg:w-1/2">
            <h2>Ready to Find Your Village?</h2>
            <p className="mt-3">Join Thousands of people connecting through shared interests and passions</p>
            <button className="button--primary mt-5">Join a Village!</button>
        </section>
    )
}

export default function Home() {
    return (
        <body>
            <Hero/>
            <div className="bg-background-secondary rounded-card py-5">
                <About/>
                <Features/>
            </div>
            <CTA/>
        </body>
    )
}