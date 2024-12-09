import Navbar from '@/components/navBar';
import { AuthProvider } from '@/app/context/AuthContext';
import Login from '@/app/login/page';
import Layout from '@/app/layout';

const HomePage = () => {  
  return <>  
  <AuthProvider>
    <Layout>
      <Navbar />
    </Layout>
  </AuthProvider>
    </>
  ;
};

export default HomePage;