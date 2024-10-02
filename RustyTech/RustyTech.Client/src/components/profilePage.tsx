/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useEffect, useRef, useState } from 'react';
import { getUserById } from '../services/userService';
import { getPostByUserId } from '../services/postService';
import { BASE_API_URL } from '../types/urls';
import { Link, useParams } from 'react-router-dom';

const formatDate = (datetime: Date) => {
    const date = new Date(datetime);
    const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: 'long', year: 'numeric' };
    return new Intl.DateTimeFormat('en-GB', options).format(date);
};


const ProfilePage: React.FC = () => {
    const [user, setUser] = useState<any>(null);
    const [posts, setPosts] = useState<any[]>([]);
    const { id } = useParams();
    const refs = useRef<(HTMLDivElement | null)[]>([]);

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
                <div>
                    <img className="profile-picture" src={`${BASE_API_URL}${user.pictureUrl}`} />
                    <p>Username: {user.userName}</p>
                </div>
            ) : (
                <p>Loading user data...</p>
            )}
            <div className="post-list">
                {posts.map((post, index) => (
                    <div key={index} ref={(el) => (refs.current[index] = el)} className='hidden'>
                        <Link className={`post-list-link`} to={`/posts/${post.id}`} key={post.id.toString()} id={post.id.toString()}>
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
                            <div className='post-info'>
                                <span className='post-date'>{formatDate(post.createdAt)}</span>
                                <h2 className="post-title">{post.title}</h2>
                                <span className="post-username">{post.user.userName}</span>
                            </div>
                        </Link></div>
                ))}
            </div>
        </main>
    );
};

export default ProfilePage;