import Navbar from '@/components/NavBar';
import { AuthProvider } from '@/app/context/AuthContext';
import Login from '@/app/login/page';
import Layout from '@/app/layout';

const HomePage = () => {  
  return <>  
    <Layout>
      <Navbar />
    </Layout>
    </>
  ;
};

export default HomePage;