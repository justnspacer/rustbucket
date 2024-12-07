import { updateUserProfile } from "@/firebase/authService";
import { useState } from "react";
import { useEffect } from "react";
import { getUser } from "@/firebase/authService";
import { getAuth, onAuthStateChanged } from "firebase/auth";


export default function UpdateUserProfile() {
  const [name, setName] = useState('');
  const [photoURL, setPhotoURL] = useState('');
  const [user, setUser] = useState(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const currentUser = await getUser();
        setUser(currentUser);
      } catch (error) {
        console.error(error);
      }
    };

    fetchUser();
  }, []);

  const handleUpdateUserProfile = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await updateUserProfile(user, name, photoURL);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleUpdateUserProfile}>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Name"
      />
      <input
        type="text"
        value={photoURL}
        onChange={(e) => setPhotoURL(e.target.value)}
        placeholder="Photo URL"
      />
      <button type="submit">Update Profile</button>
    </form>
  );
}