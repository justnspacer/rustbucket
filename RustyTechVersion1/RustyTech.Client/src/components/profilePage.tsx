/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useEffect, useState } from 'react';
import { getUserById } from '../services/userService';
import { getPostByUserId } from '../services/postService';
import { BASE_API_URL } from '../types/urls';
import { useParams } from 'react-router-dom';

const formatDate = (datetime: Date) => {
    const date = new Date(datetime);
    const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: 'long', year: 'numeric' };
    return new Intl.DateTimeFormat('en-GB', options).format(date);
};


// Select the image element
const image = document.querySelector('.profile-image') as HTMLImageElement | null;
const container = document.querySelector('.profile-picture') as HTMLImageElement | null;

// Function to check the shape of the image
function checkImageShape(img: HTMLImageElement): void {
    // Wait for the image to load to ensure width and height are available
    console.log('is image loading');

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

const ProfilePage: React.FC = () => {
    const [user, setUser] = useState<any>(null);
    const [posts, setPosts] = useState<any[]>([]);
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

    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const postsData = await getPostByUserId(id);
                setPosts(postsData);
            } catch (error) {
                console.error('Error occurred while fetching posts:', error);
            }
        };

        fetchPosts();
    }, [id]);

    return (
        <main>
            {user ? (
                <>
                    <section className={`profile-info`}>
                        <div className="profile-username">
                            <p className="picture-username">{user.userName}</p>
                        </div>
                        <div className="profile-picture">
                            <img className="profile-image" src={`${BASE_API_URL}${user.pictureUrl}`} />
                        </div>
                        <div className="profile-text">
                            <p>Spotify Stuff</p>
                        </div>
                    </section>
                </>
            ) : (
                <p>Loading user data...</p>
            )}
            <div className="posts-container">
                {posts.map((post, index) => (
                    <div className={`post-card`} key={index} id={post.id.toString()}>
                        {post.imageFile && (
                            <>
                                {post.videoFile && (
                                    <i className="fa-solid fa-play play-button"></i>
                                )}
                                <img className='post-main-image' src={`${BASE_API_URL}${post.imageFile}`} alt={post.title} />
                            </>
                        )}

                        {post?.imageFiles && (
                            <>
                                {post?.imageFiles && (
                                    <img className='post-image' src={`${BASE_API_URL}${post.imageFiles[0]}`} alt={post?.title} />
                                )}
                            </>
                        )}
                        <div className='post-content'>
                            <span className='post-date'>{formatDate(post.createdAt)}</span>
                            <h2 className="post-title">{post.title}</h2>
                        </div>
                    </div>
                ))}
                </div>
        </main>
    );
};

export default ProfilePage;