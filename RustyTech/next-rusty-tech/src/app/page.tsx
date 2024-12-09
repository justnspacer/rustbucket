import Navbar from '@/components/navBar';
import { AuthProvider } from '@/app/context/AuthContext';

const HomePage = () => {
  return <>
  <AuthProvider>
  <Navbar />
  </AuthProvider>
    </>
  ;
};

export default HomePage;