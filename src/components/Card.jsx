export default function Card({icon, img_alt, name, description}) {
    return (
        <div className="card">
            <div className="h-[120px] w-[120px] rounded-[100px] bg-white">
                <img src={icon} alt={img_alt} />
            </div>
            <p className="mt-[20px] text-black font-bold">{name}</p>
            <p className="subtitle">{description}</p>
        </div>
    )
}