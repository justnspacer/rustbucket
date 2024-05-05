import { useEffect } from 'react';
import './App.css';
import LoginForm from './components/loginForm';
import AuthProvider from './contexts/authContext';

function App() {

    useEffect(() => {
    }, []);

    return (
        <div>
            <h1 id="tabelLabel">Its morphin' time</h1>
            
            <AuthProvider>
                <LoginForm />
            </AuthProvider>
        </div>
    );
}

export default App;