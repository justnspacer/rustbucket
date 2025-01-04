/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/authContext';
import { MessageProvider } from './contexts/messageContext';
import LoginPage from './components/loginPage';
import RegisterPage from './components/registerPage';
import HomePage from './components/homePage';
import Navbar from './components/navBar';
import Footer from './components/footer';
import Post from './components/post';
import UserList from './components/userList';
import ProfilePage from './components/profilePage';
import RequestForm from './components/requestForm';
import ContactPage from './components/contactPage';
import NotFoundPage from './components/NotFoundPage';
import VerifyEmailPage from './components/verifyEmailPage';
import MessageDisplay from './components/messageDisplay';
import SpotifyCallbackPage from './components/spotifyCallback';
import Spotify from './components/spotify';

function App() {
    return (
        <MessageProvider>
            <AuthProvider>
                <BrowserRouter>
                    <Navbar />
                    <MessageDisplay />
                    <Routes>
                        <Route path="/" Component={HomePage} />
                        <Route path="/login" Component={LoginPage} />
                        <Route path="/register" Component={RegisterPage} />
                        <Route path="/verify/email" Component={VerifyEmailPage} />
                        <Route path="/profile/:id" Component={ProfilePage} />
                        <Route path="/posts/:id" Component={Post} />
                        <Route path="/users" Component={UserList} />
                        <Route path="/contact" Component={ContactPage} />
                        <Route path="/request" Component={RequestForm} />
                        <Route path="/spotify/callback" Component={SpotifyCallbackPage} />
                        <Route path="/spotify" Component={Spotify} />
                        <Route path="*" Component={NotFoundPage} />
                    </Routes>
                    <Footer />
                </BrowserRouter>
            </AuthProvider>
        </MessageProvider>
    );
}

export default App;