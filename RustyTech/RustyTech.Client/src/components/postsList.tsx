import React, { useEffect, useState } from 'react';
import { ApiResponseGetPost, getAllPosts, PostDto } from '../services/rustyTechService';
import Spinner from './spinner';

const PostsList: React.FC = () => {
    const [posts, setPosts] = useState<ApiResponseGetPost>();
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
            <ul>
                {posts?.data.map((post: PostDto) => (
                    <li key={post.id}>
                        <p>{post.id}</p>
                        <p>{post.isPublished ? 'Published' : 'Unpublished'}</p>
                        <h2>{post.title}</h2>
                        {post.imageUrl && (
                            <img src={post.imageUrl} alt={post.title} />
                        )}
                        {post.videoUrl && (
                            <video src={post.videoUrl} controls />
                        )}
                        <p>User: {post.userId}</p>
                        <p>{post.content}</p>
                        <p>Created: {post.createdAt.toString()}</p>
                        <p>Last Updated: {post.updatedAt.toString()}</p>
                        <p>Images:</p>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PostsList;