import React, { useEffect, useRef, useState } from 'react';
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
    const refs = useRef<(HTMLDivElement | null)[]>([]);

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
    }, [id]);

    if (loading) {
        return <Spinner />;
    }

    if (error) {
        return <div>{error}</div>;
    }

    return (
        <div className="post-list" key={post?.id}>
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
                    <section className='image-list'>
                        {post.imageFiles.map((imageFile, index) => (
                            <div className="parallax-image" role='img' aria-label={`${post?.title}`} key={index} style={{ backgroundImage: `url(${BASE_API_URL}${imageFile})`}}></div>
                        ))}
                    </section>
                </>
            )}
            <div className='post-main'>
                <h2 className="post-main-title">{post?.title}</h2>
                <div className='post-details'>
                    <Link to={`/profile/${post?.userId}`} className="post-username">{post?.user.userName}</Link>
                    <span className='post-date'>{post && formatDate(post.createdAt)}</span>
                </div>

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