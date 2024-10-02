/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState } from 'react';
import { getAllUsers } from '../services/userService';
import { BASE_API_URL } from '../types/urls';
import { Link } from 'react-router-dom';


const Users: React.FC = () => {
    const [users, setUsers] = useState<any>(null);

    useEffect(() => {
        const fetchUsers = async () => {
            try {
                const usersData = await getAllUsers();
                setUsers(usersData);
            } catch (error) {
                console.error('Error occurred while fetching users:', error);
            }
        };
        fetchUsers();
    }, []);

    return (
        <main>
            {users ? (
                <div>
                    {users.map((user: any) => (
                        <div key={user.id}>
                            <Link to={`/profile/${user.id}`}>
                            <img className="profile-picture" src={`${BASE_API_URL}${user.pictureUrl}`} />
                                <p>Username: {user.userName}</p>
                            </Link>

                        </div>
                    ))}
                </div>
            ) : (
                <p>Loading users...</p>
            )}
        </main>
    );
};

export default Users;