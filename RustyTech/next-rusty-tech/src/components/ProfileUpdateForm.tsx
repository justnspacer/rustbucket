"use client";
import React, { useState, useEffect } from "react";
import { useAuth } from "@/app/context/AuthContext";

const ProfileUpdateForm = () => {
  const { user, updateProfile, loading } = useAuth();
  const [displayName, setDisplayName] = useState(user?.displayName || "");
  const [photoURL, setPhotoURL] = useState(user?.photoURL || "");
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    if (showForm) {
      setDisplayName(user?.displayName || "");
      setPhotoURL(user?.photoURL || "");
    }
  }, [showForm, user]);


  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    try {
      await updateProfile({ displayName, photoURL });
      setShowForm(false);
    } catch (error) {
      setError("Failed to update profile. Please try again.");
    }
  };

  return (
    <div>
    {!showForm && (
      <button onClick={() => setShowForm(true)}>Update Profile</button>
    )}
    {showForm && (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="displayName">Change your display name:</label>
        <input
          type="text"
          id="displayName"
          value={displayName}
          onChange={(e) => setDisplayName(e.target.value)}
          disabled={loading}
        />
      </div>
      <div>
        <label htmlFor="photoURL">Change your photo:</label>
        <input
          type="text"
          id="photoURL"
          value={photoURL}
          onChange={(e) => setPhotoURL(e.target.value)}
          disabled={loading}
        />
      </div>
      {error && <p>{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? "Updating..." : "Save Changes"}
      </button>
    </form>
      )}
      </div>
  );
};

export default ProfileUpdateForm;