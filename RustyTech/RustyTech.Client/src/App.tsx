import { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import LoginForm from './components/loginForm';
import RegisterForm from './components/registerForm';
import Home from './components/home';
import AuthProvider from './contexts/authContext';
import Navbar from './components/navBar'; // Import the Navbar component

function App() {
    useEffect(() => {
    }, []);

    return (
        <AuthProvider>
            <BrowserRouter>
                <Navbar isAuthenticated={false} isTokenValid={false} />
                <Routes>
                    <Route path="/login" Component={LoginForm} />
                    <Route path="/register" Component={RegisterForm} />
                    <Route path="/" Component={Home} />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;