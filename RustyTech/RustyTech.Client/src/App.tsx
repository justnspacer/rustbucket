import { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import LoginForm from './components/loginForm';
import Home from './components/home';
import AuthProvider from './contexts/authContext';

function App() {

    useEffect(() => {
    }, []);

    return (
        <AuthProvider>
            <BrowserRouter>
                <Routes>
                    <Route path="/login" Component={LoginForm} />
                    <Route path="/" Component={Home} />
                </Routes>
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;