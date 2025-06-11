"use client";
import React, { useState } from 'react';
import { supabase } from '../app/utils/supabaseClient';
import { ContentBlockProps, LayoutType, MediaType } from '../types/ContentBlockProps';

const defaultLayout: LayoutType = 'media-left';
const defaultMediaType: MediaType = 'image';

export const AdminForm = () => {
  const [formData, setFormData] = useState<ContentBlockProps>({
    title: '',
    body: '',
    layout: defaultLayout,
    media_type: defaultMediaType,
    media_urls: [],
  });

  const [mediaInput, setMediaInput] = useState('');
  const [statusMsg, setStatusMsg] = useState('');

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const addMediaUrl = () => {
    if (mediaInput) {
      setFormData((prev) => ({
        ...prev,
        media_urls: [...(prev.media_urls || []), mediaInput],
      }));
      setMediaInput('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatusMsg('Saving...');

    const { error } = await supabase.from('content_blocks').insert([formData]);

    if (error) {
      console.error('Error saving content block:', error);
      setStatusMsg('❌ Error saving block.');
    } else {
      setStatusMsg('✅ Content block saved!');
      setFormData({
        title: '',
        body: '',
        layout: defaultLayout,
        media_type: defaultMediaType,
        media_urls: [],
        is_published: true,
      });
    }
  };

  const [file, setFile] = useState<File | null>(null);

const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  if (e.target.files && e.target.files.length > 0) {
    setFile(e.target.files[0]);
  }
};

const uploadFile = async () => {
  if (!file) return;

  const fileExt = file.name.split('.').pop();
  const fileName = `${Date.now()}.${fileExt}`;
  const filePath = `${fileName}`;

  const { error: uploadError } = await supabase.storage
    .from('media')
    .upload(filePath, file);

  if (uploadError) {
    console.error('Upload failed:', uploadError);
    setStatusMsg('❌ File upload failed.');
    return;
  }

  const { data } = supabase.storage.from('media').getPublicUrl(filePath);
  const publicUrl = data.publicUrl;

  setFormData((prev) => ({
    ...prev,
    media_urls: [...(prev.media_urls || []), publicUrl],
  }));

  setStatusMsg('✅ File uploaded!');
};

  const [showFileUpload, setShowFileUpload] = useState(false);
  const toggleFileUpload = () => {
     setShowFileUpload((prev) => {
    // Reset both fields when toggling
    setFile(null);
    setMediaInput('');
    return !prev;
  });
  };
  const handleMediaTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedType = e.target.value as MediaType;
    setFormData((prev) => ({
      ...prev,
      media_type: selectedType,
    }));
  };
  const handleLayoutChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedLayout = e.target.value as LayoutType;
    setFormData((prev) => ({
      ...prev,
      layout: selectedLayout,
    }));
  };
  const handleMediaUrlChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMediaInput(e.target.value);
  };
  const handleMediaUrlsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const urls = e.target.value.split(',').map((url) => url.trim());
    setFormData((prev) => ({
      ...prev,
      media_urls: urls,
    }));
  };

  return (
          <div className='container'><h2 className='header-2'>Create Content Item</h2><form onSubmit={handleSubmit} className="admin-form">
      <input type="text" name="title" value={formData.title} onChange={handleChange} placeholder="Title" required />

      <textarea name="body" value={formData.body} onChange={handleChange} placeholder="Body text" required />

      <select name="layout" value={formData.layout} onChange={handleLayoutChange}>
        <option value="media-left">Media Left</option>
        <option value="media-right">Media Right</option>
        <option value="stacked">Stacked</option>
        <option value="media-background">Media Background</option>
      </select>

      <select name="media_type" value={formData.media_type} onChange={handleMediaTypeChange}>
        <option value="image">Image</option>
        <option value="video">Video</option>
      </select>

      <div>
        <button
          type="button"
          className='button-1'
          onClick={toggleFileUpload}
          style={{ marginBottom: '1rem' }}
        >
          {showFileUpload ? 'Switch to URL Input' : 'Switch to File Upload'}
        </button>
        {showFileUpload ? (
          <div className="file-upload">
            <input type="file" onChange={handleFileChange} key="upload" />
            <button type="button" className='button-1' onClick={uploadFile}>Upload File</button>
          </div>
        ) : (
          <div className="media-url-input">
            <input type="text" value={mediaInput} onChange={handleMediaUrlChange} placeholder="Media URL" />
            <button type="button" className='button-1' onClick={addMediaUrl}>Add Media</button>
          </div>
        )}
      </div>

      <ul>
        {formData.media_urls?.map((url, idx) => (
          <li key={idx}>{url}</li>
        ))}
      </ul>

      <button type="submit" className='button-2'>Create Item</button>
      <p>{statusMsg}</p>
    </form></div>
  );
};
