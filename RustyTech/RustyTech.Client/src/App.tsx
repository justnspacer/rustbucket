import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './contexts/authContext';
import LoginPage from './components/loginPage';
import RegisterPage from './components/registerPage';
import HomePage from './components/homePage';
import Navbar from './components/navBar';
import Footer from './components/footer';
import Post from './components/post';
import Posts from './components/posts';
import AboutPage from './components/aboutPage';
import ProfilePage from './components/profilePage';
import RequestPage from './components/requestPage';
import ContactPage from './components/contactPage';
import ProjectsPage from './components/projectsPage';

function App() {

    return (
        <AuthProvider>
            <BrowserRouter>
                <Navbar />
                <Routes>
                    <Route path="/profile/:id" Component={ProfilePage} />
                    <Route path="/posts/:id" Component={Post} />
                    <Route path="/posts/" Component={Posts} />
                    <Route path="/login" Component={LoginPage} />
                    <Route path="/register" Component={RegisterPage} />
                    <Route path="/projects" Component={ProjectsPage} />
                    <Route path="/about" Component={AboutPage} />
                    <Route path="/contact" Component={ContactPage} />
                    <Route path="/request" Component={RequestPage} />
                    <Route path="/" Component={HomePage} />
                </Routes>
                <Footer />
            </BrowserRouter>
        </AuthProvider>
    );
}

export default App;