import React, { useEffect, useState } from 'react';
import Spinner from './spinner';
import { getPostById } from '../services/postService';
import { PostDto } from '../types/apiResponse';
import { useParams } from 'react-router-dom';

const formatDate = (datetime: Date) => {
    const date = new Date(datetime);
    const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: 'long', year: 'numeric' };
    return new Intl.DateTimeFormat('en-GB', options).format(date);
};

const Post: React.FC = () => {
    const [post, setPost] = useState<PostDto>();
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    const { id } = useParams();

    useEffect(() => {
        const fetchPost = async (id: number) => {
            try {
                const data = await getPostById(id);
                setPost(data);
            } catch (err) {
                setError('Failed to fetch post');
            } finally {
                setLoading(false);
            }
        };

        fetchPost(Number(id));
    }, [id]);

    if (loading) {
        return <Spinner />;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className='post' key={post?.id}>
            <h2>{post?.title}</h2>
            <p>{post?.userId}</p>
            <span className='date'>{post && formatDate(post.createdAt)}</span>


            {post?.createdAt != post?.updatedAt && (
                <div>
                    <span className='date'>{post && formatDate(post.updatedAt)} (updated)</span>
                </div>
            )}

            {post?.imageUrl && (
                <img src={post?.imageUrl} alt={post?.title} />
            )}
            {post?.videoUrl && (
                <video src={post?.videoUrl} controls />
            )}
            <p>{post?.content}</p>
            <p>Images:</p>
        </div>
    );
};
export default Post;