import AssignRole from "@/components/role/AssignRole";
import { AdminForm } from "@/components/AdminForm";
import { ContentFeed } from "@/components/content/ContentFeed";

const AdminPage = () => {
  return (
    <div className="admin-page">
      <AdminForm />
      <ContentFeed />
    </div>
  );
};

export default AdminPage;