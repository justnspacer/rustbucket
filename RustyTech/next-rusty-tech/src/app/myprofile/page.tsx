"use client";
import { useAuth } from "@/app/context/AuthContext";
import ProfileUpdateForm from "@/components/ProfileUpdateForm";

const ProfilePage = () => {
  const { user } = useAuth();

  return (
    <div>
      {user?.photoURL && <img className="profile-image" src={user?.photoURL} alt={user?.displayName ||
        'User profile picture'}/>}
      {user?.displayName && <h2>{user.displayName}</h2>}

      <ProfileUpdateForm />
    </div>
  );
};

export default ProfilePage;