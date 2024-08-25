import React, { useEffect, useState } from 'react';
import { getAllPosts } from '../services/postService';
import { GetPostRequest } from '../types/apiResponse';
import { BASE_URL } from '../types/urls';
import Spinner from './spinner';

const formatDate = (datetime: Date) => {
    const date = new Date(datetime);
    const options: Intl.DateTimeFormatOptions = { day: '2-digit', month: 'long', year: 'numeric' };
    return new Intl.DateTimeFormat('en-GB', options).format(date);
};

const PostsList: React.FC = () => {
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
                {posts?.map((post: GetPostRequest) => (
                    <a className='postlink' href={`/posts/get/${post.id}`} key={post.id}>
                        <li className='post' >
                           
                            {post.imageFile && (
                                <img src={`${BASE_URL}${post.imageFile}`} alt={post.title} />
                            )}
                            {post.videoFile && (
                                <video controls>
                                    <source src={`${BASE_URL}${post.videoFile}`} type="video/mp4" />
                                    Your browser does not support the video tag.
                                </video>
                            )}
                            {post?.imageFiles && (
                                <>
                                    {post.imageFiles.map((imageFile, index) => (
                                        <img key={index} src={`${BASE_URL}${imageFile}`} alt={post?.title} />
                                    ))}
                                </>
                            )}
                            <h2>{post.title}</h2>
                            <p>{post.user.userName}</p>
                            <span className='date'>{formatDate(post.createdAt)}</span>
                            {post.createdAt != post.updatedAt && (
                                <div>
                                    <span className='date'>{formatDate(post.updatedAt)} (updated)</span>
                                </div>
                            )}

                            <ul className='post-keyword-list'>
                                {post?.keywords && post.keywords.map((keyword, index) => (
                                    <li className='keyword-text' key={index}>{keyword}</li>
                                ))}
                            </ul>
                        </li>
                    </a>
                ))}
            </ul>
        </div>
    );
};

export default PostsList;