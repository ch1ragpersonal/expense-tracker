import LoginForm from "../components/LoginForm";
import { useNavigate } from 'react-router-dom';

function LoginPage() {
    const navigate = useNavigate()

    const handleLoginSuccess = () => {
        navigate('/dashboard');
    };

    return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100 p-4">
          <LoginForm onLoginSuccess={handleLoginSuccess} />
        </div>
      );
}

export default LoginPage;