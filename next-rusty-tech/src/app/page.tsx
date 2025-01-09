import Navbar from '@/components/NavBar';
import { AuthProvider } from '@/app/context/AuthContext';
import Layout from '@/app/layout';

const HomePage = () => {  
  return <>  
              <div className="homepage-message">
                <h1 className="homepage-header">Welcome to Rust Bucket</h1>
                <p className="homepage-description">Let's work together to bring your vision to life on the web!</p>
            </div>
    </>
  ;
};

export default HomePage;