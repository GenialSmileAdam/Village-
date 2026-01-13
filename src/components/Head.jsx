import {Helmet} from "react-helmet-async";

const Head = ({title}) => {
    return(
        <Helmet>
            <title>Village - {title}</title>
        </Helmet>
    )
}

export default Head;