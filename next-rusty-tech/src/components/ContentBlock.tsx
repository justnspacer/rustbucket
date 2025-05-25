import { ContentBlockProps } from '../types/ContentBlockProps';

export const ContentBlock: React.FC<ContentBlockProps> = ({ title, body, layout, media_type, media_urls }) => {
  return (
    <div className={`content-block layout-${layout}`}>
      <h2>{title}</h2>
      <p>{body}</p>
      {media_type === 'image' &&
        media_urls?.map((url, i) => <img key={i} src={url} alt={`media-${i}`} />)}
      {media_type === 'video' &&
        media_urls?.map((url, i) => (
          <video key={i} controls src={url} />
        ))}
    </div>
  );
};
