import { useEffect, useState } from 'react';
import { fetchData } from '../services/rustyTechService';

const RegisterComponent = () => {
    const [data, setData] = useState(null);
    useEffect(() => {
        fetchData()
            .then(data => setData(data))
            .catch(error => console.error(error));
    }, []);

    return (<div>{data ? <pre>{JSON.stringify(data)}</pre> : 'Loading data...' }</div>);
};

export default RegisterComponent;