/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState } from 'react';
import { getAllUsers } from '../services/userService';
import { BASE_API_URL } from '../types/urls';
import { Link } from 'react-router-dom';


const UserList: React.FC = () => {
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
                <div className="user-list">
                    {users.map((user: any) => (
                        <Link to={`/profile/${user.id}`} className="user" key={user.id}>
                            <img className="profile-picture" src={`${BASE_API_URL}${user.pictureUrl}`} />
                            <span className="picture-username">{user.userName}</span>
                        </Link>
                    ))}
                </div>
            ) : (
                <p>Loading users...</p>
            )}
        </main>
    );
};

export default UserList;