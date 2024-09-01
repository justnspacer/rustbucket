import React, { useEffect, useState } from 'react';
import Spinner from './spinner';
import { getPostById } from '../services/postService';
import { GetPostRequest } from '../types/apiResponse';
import { Link, useParams } from 'react-router-dom';
import { BASE_API_URL } from '../types/urls';


const formatDate = (datetime: Date) => {
    const date = new Date(datetime);
    const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: 'long', year: 'numeric' };
    return new Intl.DateTimeFormat('en-GB', options).format(date);
};

const Post: React.FC = () => {
    const [post, setPost] = useState<GetPostRequest>();
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
        <div className='single-post' key={post?.id}>
            {post?.videoFile && (
                <video className='post-main-video' controls>
                    <source src={`${BASE_API_URL}${post?.videoFile}`} type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
            )}
            {post?.imageFile && (
                <img className='post-main-image' src={`${BASE_API_URL}${post?.imageFile}`} alt={post?.title} />
            )}
            {post?.imageFiles && (
                <>
                    {post.imageFiles.map((imageFile, index) => (
                        <img className='post-image' key={index} src={`${BASE_API_URL}${imageFile}`} alt={post?.title} />
                    ))}
                </>
            )}
            <div className='post-info'>
                <h2 className="post-title">{post?.title}</h2>
                <Link to={`/profile/${post?.userId}`} className="post-username">{post?.user.userName}</Link>
                <span className='post-date'>{post && formatDate(post.createdAt)}</span>


                {post?.createdAt != post?.updatedAt && (
                    <div>
                        <span className='post-date'>{post && formatDate(post.updatedAt)} (updated)</span>
                    </div>
                )}
                <div dangerouslySetInnerHTML={{ __html: post?.content }}></div>

                {post?.keywords && post.keywords.map((keyword, index) => (
                    <span className='keyword-text' key={index}>{keyword}</span>
                ))}
            </div>
        </div>
    );
};
export default Post;