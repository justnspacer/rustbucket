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


const ProfilePage: React.FC = () => {
    const [user, setUser] = useState<any>(null);
    const [posts, setPosts] = useState<any[]>([]);
    const { id } = useParams();

    const [scrollPosition, setScrollPosition] = useState(0);

    const handleScroll = () => {
        setScrollPosition(window.scrollY);
    };

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

    useEffect(() => {
        window.addEventListener("scroll", handleScroll);
        return () => window.removeEventListener("scroll", handleScroll);
    }, []);

    return (
        <main>
            {user ? (
                <>
                    <section className="profile-info">
                        <div className="profile-username">
                            <h2 className="picture-username">{user.userName}</h2>
                        </div>
                        <div className="profile-picture">
                            <img className="" src={`${BASE_API_URL}${user.pictureUrl}`} />
                        </div>
                        <div className="profile-text">
                            <h2>Spotify Stuff</h2>
                            <p>You hope!</p>
                        </div>
                    </section>
                </>
            ) : (
                <p>Loading user data...</p>
            )}
            <div className="posts-container">
                {posts.map((post, index) => (
                    <div
                        className={`post-card ${scrollPosition > 100 && scrollPosition < 400 ? "fade" : ""
                            }`}
                        key={index}
                        id={post.id.toString()}
                        style={{ transform: `rotate(${index * (360 / post.length)}deg) translate(150px)` }}
                    >
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
                            <span className="post-username">{post.user.userName}</span>
                        </div>
                    </div>
                ))}
            </div>
        </main>
    );
};

export default ProfilePage;