import AssignRole from "@/components/AssignRole";
import { AdminForm } from "@/components/AdminForm";
import { ContentFeed } from "@/components/ContentFeed";

const AdminPage = () => {
  return (
    <div className="admin-page">
      <AdminForm />
      <ContentFeed />
    </div>
  );
};

export default AdminPage;