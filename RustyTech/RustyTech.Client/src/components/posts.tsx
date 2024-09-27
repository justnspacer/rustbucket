/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable @typescript-eslint/no-explicit-any */
import { useState, useEffect, useRef } from 'react';
import { GetPostRequest } from '../types/apiResponse';
import { Link } from 'react-router-dom';
import { BASE_API_URL } from '../types/urls';
import { getAllPosts } from '../services/postService';
import Spinner from './spinner';


const formatDate = (datetime: Date) => {
    const date = new Date(datetime);
    const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: 'long', year: 'numeric' };
    return new Intl.DateTimeFormat('en-GB', options).format(date);
};

const Posts: React.FC = () => {
    const [posts, setPosts] = useState<GetPostRequest[]>([]);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const refs = useRef<(HTMLDivElement | null)[]>([]);

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
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible'); // Add 'visible' class when in view
                } else {
                    entry.target.classList.remove('visible'); // Optionally remove when out of view
                }
            });
        });

        refs.current.forEach(ref => {
            if (ref) observer.observe(ref);
        });

        return () => {
            refs.current.forEach(ref => {
                if (ref) observer.unobserve(ref);
            });
        };
    }, []);

    if (loading) {
        return <Spinner />;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
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
    );
};

export default Posts;