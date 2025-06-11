"use client"
import { useEffect, useState } from 'react';
import { supabase } from '../app/utils/supabaseClient';
import { ContentBlock } from './ContentBlock';
import { ContentBlockProps } from '../types/ContentBlockProps';

export const ContentFeed = () => {
  const [blocks, setBlocks] = useState<ContentBlockProps[]>([]);

  useEffect(() => {
    const fetchBlocks = async () => {
      const { data, error } = await supabase
        .from('content_blocks')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) {
        console.error('Error fetching content blocks:', error);
      } else {
        setBlocks(data as ContentBlockProps[]);
      }
    };

    fetchBlocks();
  }, []);

  return (
    <div className='container'><h2 className='header-2'>Content Feed</h2>
    <div className="content-feed">
      {blocks.map((block) => (
        <ContentBlock key={block.id} {...block} />
      ))}
    </div>
    </div>
  );
};
