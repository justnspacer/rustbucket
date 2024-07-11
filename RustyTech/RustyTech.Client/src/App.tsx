import { useEffect } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
//import './App.css';
import LoginForm from './components/loginForm';
import RegisterForm from './components/registerForm';
import Home from './components/home';
import AuthProvider from './contexts/authContext';
import Navbar from './components/navBar';
import Footer from './components/footer';
import Post from './components/post';

function App() {
    useEffect(() => {
    }, []);

    return (
        <AuthProvider>
            <BrowserRouter>
                <Navbar />
                <Routes>
                    <Route path="/posts/get/:id" Component={Post} />
                    <Route path="/login" Component={LoginForm} />
                    <Route path="/register" Component={RegisterForm} />
                    <Route path="/" Component={Home} />
                </Routes>
                <Footer />
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;