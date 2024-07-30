import React, { useEffect, useState } from 'react';
import { getAllPosts } from '../services/postService';
import { PostDto } from '../types/apiResponse';
import Spinner from './spinner';

const formatDate = (datetime: Date) => {
    const date = new Date(datetime);
    const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: 'long', year: 'numeric' };
    return new Intl.DateTimeFormat('en-GB', options).format(date);
};

const PostsList: React.FC = () => {
    const [posts, setPosts] = useState<PostDto[]>();
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);


    useEffect(() => {
        const fetchPosts = async () => {
            try {
                const data = await getAllPosts();
                setPosts(data);
            } catch (err) {
                setError('Failed to fetch posts');
            } finally {
                setLoading(false);
            }
        };

        fetchPosts();
    }, []);

    if (loading) {
        return <Spinner />;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div>
            <h1>Posts</h1>
            <ul className='postlist'>
                {posts?.map((post: PostDto) => (
                    <a className='postlink' href={`/posts/get/${post.id}`} key={post.id}>
                        <li className='post' >
                            <h2>{post.title}</h2>
                            <p>{post.userId}</p>
                            <span className='date'>{formatDate(post.createdAt)}</span>
                            {post.createdAt != post.updatedAt && (
                                <div>                                    
                                    <span className='date'>{formatDate(post.updatedAt)} (updated)</span>
                                </div>
                            )}
                            {post.imageUrl && (
                                <img src={post.imageUrl} alt={post.title} />
                            )}
                            {post.videoUrl && (
                                <video src={post.videoUrl} controls />
                            )}
                            <p>{post.content}</p>
                            <p>Images:</p>
                        </li>
                    </a>
                ))}
            </ul>
        </div>
    );
};

export default PostsList;