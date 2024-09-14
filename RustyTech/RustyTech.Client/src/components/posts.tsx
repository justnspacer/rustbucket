/* eslint-disable react-refresh/only-export-components */
/* eslint-disable @typescript-eslint/no-explicit-any */
import React, { useEffect, useState } from 'react';
import { getAllPosts } from '../services/postService';
import { GetPostRequest } from '../types/apiResponse';
import { BASE_API_URL } from '../types/urls';
import Spinner from './spinner';
import { Link } from 'react-router-dom';

const formatDate = (datetime: Date) => {
    const date = new Date(datetime);
    const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: 'long', year: 'numeric' };
    return new Intl.DateTimeFormat('en-GB', options).format(date);
};

const Posts: React.FC = () => {
    const [posts, setPosts] = useState<GetPostRequest[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);


    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const response = await getAllPosts();
                setPosts(response);
            } catch (err) {
                setError('Failed to fetch posts');
            } finally {
                setLoading(false);
            }
        };

        fetchPosts();

        const handleScrollToPost = (event) => {
            const postElement = event.target.closest('.post');
            if (postElement) {
                const postId = postElement.id;
                scrollToPost(postId);
            }
        };

        const scrollToPost = (postId: string) => {
            const post = document.getElementById(postId);
            if (post) {
                window.scrollTo({
                    top: post.offsetTop,
                    behavior: 'smooth'
                });
            }
        };

        const postListElement = document.querySelector('.post-list');
        postListElement?.addEventListener('click', handleScrollToPost);

        // Cleanup the event listener on component unmount
        return () => {
            postListElement?.removeEventListener('click', handleScrollToPost);
        };
    }, []);

    if (loading) {
        return <Spinner />;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className='post-list'>
            {posts?.map((post: GetPostRequest) => (
                <Link className="post-list-link" to={`/posts/${post.id}`} key={post.id}>
                    <div className='post'>
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
                            <h2 className="post-title">{post.title}</h2>
                            <span className="post-username">{post.user.userName}</span>
                            <span className='post-date'>{formatDate(post.createdAt)}</span>
                            {post.createdAt !== post.updatedAt && (
                                <div>
                                    <span className='post-date'>{formatDate(post.updatedAt)} (updated)</span>
                                </div>
                            )}
                        </div>
                    </div>
                </Link>
            ))}
        </div>
    );
};

export default Posts;