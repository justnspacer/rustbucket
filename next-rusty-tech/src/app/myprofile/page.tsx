"use client";
import { useAuth } from "@/app/context/AuthContext";
import ProfileUpdateForm from "@/components/ProfileUpdateForm";

const ProfilePage = () => {
  const { user } = useAuth();

  return (
    <div>
      {user?.email && <img className="profile-image" src={user?.user_metadata.photoURL} alt={user?.email ||
        'User profile picture'}/>}
      {user?.email && <h2>{user.email}</h2> }
      

      <ProfileUpdateForm />
    </div>
  );
};

export default ProfilePage;