export type LayoutType = 'media-left' | 'media-right' | 'stacked' | 'media-background';
export type MediaType = 'image' | 'video' | 'youtube';

export interface ContentBlockProps {
  id?: string; // optional for now unless you're doing updates
  title: string;
  body: string;
  layout: LayoutType;
  media_type?: MediaType;
  media_urls?: string[];
  user_id?: string;
  is_published?: boolean;
  tags?: string[];
  created_at?: string;
  updated_at?: string;
}
