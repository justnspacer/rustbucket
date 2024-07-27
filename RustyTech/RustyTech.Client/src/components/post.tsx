import React, { useEffect, useState } from 'react';
import Spinner from './spinner';
import { ApiResponseGetSinglePost, getPostById } from '../services/postService';
import { useParams } from 'react-router-dom';

const formatDate = (datetime: Date) => {
    const date = new Date(datetime);
    const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: 'long', year: 'numeric' };
    return new Intl.DateTimeFormat('en-GB', options).format(date);
};

const Post: React.FC = () => {
    const [post, setPost] = useState<ApiResponseGetSinglePost>();
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
        <div className='post' key={post?.data.id}>
            <h2>{post?.data.title}</h2>
            <p>{post?.data.userId}</p>
            <span className='date'>{post?.data && formatDate(post.data.createdAt)}</span>


            {post?.data.createdAt != post?.data.updatedAt && (
                <div>
                    <span className='date'>{post?.data && formatDate(post.data.updatedAt)} (updated)</span>
                </div>
            )}

            {post?.data.imageUrl && (
                <img src={post?.data.imageUrl} alt={post?.data.title} />
            )}
            {post?.data.videoUrl && (
                <video src={post?.data.videoUrl} controls />
            )}
            <p>{post?.data.content}</p>
            <p>Images:</p>
        </div>
    );
};
export default Post;