import { Navigate } from 'react-router-dom';

function PrivateRoute({ children }){
    const token = localStorage.getItem('access_token');

    if (!token){
        console.log("You are not authorised to enter")
        return <Navigate to="/" replace/>
    }

    return children;

}

export default PrivateRoute;