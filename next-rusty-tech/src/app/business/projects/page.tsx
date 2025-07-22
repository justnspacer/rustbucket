'use client';
import React from 'react';
import { useAuth } from '@/app/context/AuthContext';

export default function ProjectsPage() {
  const { getAuthToken } = useAuth();

  const handleSpotifyClick = () => {
    const token = getAuthToken();
    if (token) {
      // Open the Spotify API endpoint with the bearer token in the Authorization header
      const headers = { Authorization: token }; // auth header with bearer token
      console.log('Fetching Spotify data with headers:', headers);
      fetch('http://127.0.0.1:8000/api/spotify/', { headers }).then(
        (response) => response.json()
      );
    } else {
      alert('Please log in to access this feature');
    }
  };

  return (
    <div>
      <h1 id="project-header" className="header">
        Projects
      </h1>
      <ul className="project-list">
        <li id="project-1" className="project-container">
          <div>
            <h2>Nothing App</h2>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sapiente
              quam officiis animi sit?
            </p>
            <img
              src="https://images.unsplash.com/photo-1749127025851-d1f416fe7da0?q=80&w=687&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              alt="Project 1 Screenshot"
              className="project-image"
            />
          </div>
        </li>
        <li id="project-2" className="project-container">
          <div
            onClick={handleSpotifyClick}
            className="project-container-clickable"
            style={{ cursor: 'pointer' }}
          >
            <h2>Spotify App</h2>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sapiente
              quam officiis animi sit?
            </p>
            <img
              src="https://images.unsplash.com/photo-1519821767025-2b43a48282ca?q=80&w=1170&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              alt="Project 1 Screenshot"
              className="project-image"
            />
          </div>
        </li>
        <li id="project-3" className="project-container">
          <div>
            <h2>Cool App</h2>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sapiente
              quam officiis animi sit?
            </p>
            <img
              src="https://images.unsplash.com/photo-1722080768196-8983bbbb5c0f?q=80&w=880&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              alt="Project 1 Screenshot"
              className="project-image"
            />
          </div>
        </li>
        <li id="project-4" className="project-container">
          <div>
            <h2>Awesome App</h2>
            <p>
              Lorem ipsum dolor sit amet, consectetur adipisicing elit. Sapiente
              quam officiis animi sit?
            </p>
            <img
              src="https://images.unsplash.com/photo-1738937444519-f0a7084c955e?q=80&w=630&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
              alt="Project 1 Screenshot"
              className="project-image"
            />
          </div>
        </li>
      </ul>
    </div>
  );
}
