import React, { useEffect, useState } from 'react';
import Spinner from './spinner';
import { getPostById } from '../services/postService';
import { PostDto } from '../types/apiResponse';
import { useParams } from 'react-router-dom';
import { MEDIA_URL } from '../types/urls';


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
            {post?.videoFile && (
                <video controls>
                    <source src={`${MEDIA_URL}${post?.videoFile}`} type="video/mp4" />
                    Your browser does not support the video tag.
                </video>
            )}
            {post?.imageFile && (
                <img src={`${MEDIA_URL}${post?.imageFile}`} alt={post?.title} />
            )}
            {post?.imageFiles && (
                <>
                    {post.imageFiles.map((imageFile, index) => (
                        <img key={index} src={`${MEDIA_URL}${imageFile}`} alt={post?.title} />
                    ))}
                </>
            )}
            <h2>{post?.title}</h2>
            <p>{post?.user.userName}</p>
            <span className='date'>{post && formatDate(post.createdAt)}</span>


            {post?.createdAt != post?.updatedAt && (
                <div>
                    <span className='date'>{post && formatDate(post.updatedAt)} (updated)</span>
                </div>
            )}
            <div dangerouslySetInnerHTML={{ __html: post?.content }}></div>

            <ul className='post-keyword-list'>
                {post?.keywords && post.keywords.map((keyword, index) => (
                    <li className='keyword-text' key={index}>{keyword}</li>
                ))}
            </ul>

        </div>
    );
};
export default Post;