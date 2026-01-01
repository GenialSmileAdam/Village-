export default function Card({icon, title, description}) {
    return (
        <div className="card">
            <div className="h-[120px] w-[120px] rounded-[100px] bg-white flex-center" >
                {icon}
            </div>
            <p className="mt-[20px] text-black font-bold">{title}</p>
            <p className="subtitle">{description}</p>
        </div>
    )
}