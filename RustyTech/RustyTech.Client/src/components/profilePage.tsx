/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useEffect, useState } from 'react';
import { getUserById } from '../services/userService';
import { BASE_URL } from '../types/urls';
import { useParams } from 'react-router-dom';

const ProfilePage: React.FC = () => {
    const [user, setUser] = useState<any>(null);
    const { id } = useParams();

    useEffect(() => {
        const fetchUser = async () => {
            try {
                const userData = await getUserById(id);
                setUser(userData);
            } catch (error) {
                console.error('Error occurred while fetching user:', error);
            }
        };

        fetchUser();
    }, [id]);

    return (
        <main>
            {user ? (
                <div>
                    <img className="profile-picture" src={`${BASE_URL}${user.pictureUrl}`} />
                    <p>Username: {user.userName}</p>
                </div>
            ) : (
                <p>Loading user data...</p>
            )}
        </main>
    );
};

export default ProfilePage;