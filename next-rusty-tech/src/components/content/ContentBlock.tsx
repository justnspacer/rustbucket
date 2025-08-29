import { ContentBlockProps } from '../types/ContentBlockProps';


export const ContentBlock: React.FC<ContentBlockProps> = ({ title, body, layout, media_type, media_urls }) => {

    const getYouTubeVideoId = (url: string): string | null => {
  const match = url.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|shorts\/))([\w-]{11})/);
  return match ? match[1] : null;
};

  const YouTubeEmbed = ({ videoId }: { videoId: string }) => {
  return (
    <div className="youtube-container media-video" >
      <iframe
        width="100%"
        height="400"
        src={`https://www.youtube.com/embed/${videoId}`}
        title="YouTube video player"
        frameBorder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      ></iframe>
    </div>
  );
};

  const YouTubeFromUrl = ({ url }: { url: string }) => {
  const videoId = getYouTubeVideoId(url);
  if (!videoId) return <p>Invalid YouTube URL</p>;
  return <YouTubeEmbed videoId={videoId} />;
};



  return (
    <div className={`content-block layout-${layout}`}>
      <div className='content-text'>
      <h2>{title}</h2>
      <p>{body}</p>
      </div>
      <div className='content-media'>
      {media_type === 'image' &&
      media_urls?.map((url, i) => <img className='media-image' key={i} src={url} alt={`media-${i}`} />)}
      {media_type === 'video' &&
      media_urls?.map((url, i) => {
        const isYouTube = !!getYouTubeVideoId(url);
        if (isYouTube) {
        return <YouTubeFromUrl key={i} url={url} />;
        }
        return <video className='media-video' key={i} controls src={url} />;
      })}
      </div>
    </div>
  );
};
