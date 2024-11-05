/* eslint-disable @typescript-eslint/no-explicit-any */
import { useEffect, useState } from 'react';
import { getAllUsers } from '../services/userService';
import { BASE_API_URL } from '../types/urls';
import { Link } from 'react-router-dom';

// Select the image element
const image = document.querySelector('.profile-image') as HTMLImageElement | null;
const container = document.querySelector('.profile-picture') as HTMLImageElement | null;

// Function to check the shape of the image
function checkImageShape(img: HTMLImageElement): void {

    if (img.naturalWidth !== img.naturalHeight) {
        // Image is a rectangle
        container?.classList.add('circle');
    }
    else {
        console.log('image is not rectangle');
    }
}
if (image) {
    checkImageShape(image);
}


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
                        <Link to={`/profile/${user.id}`} className="profile-picture" key={user.id}>
                            <img className="profile-image" src={`${BASE_API_URL}${user.pictureUrl}`} />
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