"use client";
import { useAuth } from "@/app/context/AuthContext";
import ProfileUpdateForm from "@/components/ProfileUpdateForm";

const ProfilePage = () => {
  const { user } = useAuth();

  return (
    <div>
      <div className="profile-header">
      {user?.email && <img className="profile-image" src={user?.user_metadata.photoURL} alt={user?.email ||
        'User profile picture'}/>}
      {user?.email && <h2>{user.email}</h2> }
      </div>

      <ProfileUpdateForm />
    </div>
  );
};

export default ProfilePage;