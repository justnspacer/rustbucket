import AssignRole from "@/components/AssignRole";
import { AdminForm } from "@/components/AdminForm";

const AdminPage = () => {
  return (
    <div>
      <h1>Admin Page</h1>
      <p>Manage your content and user roles here.</p>
      <AdminForm />
      
    </div>
  );
};

export default AdminPage;