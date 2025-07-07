const list = document.querySelector('[data-animate-stagger]');
if (list) {
  console.log('Stagger group found');
}

function applyUserImageColor() {
  document.addEventListener('DOMContentLoaded', (event) => {
    console.log('DOM fully loaded and parsed');
    const profilePicture = document.getElementById('user-profile-picture');
    const nav = document.querySelector('nav');
    const userInfo = document.querySelector('.user-info');
    const customColorItems = document.querySelectorAll('.custom-color-item');

    function getAverageColor(imageElement) {
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      canvas.width = imageElement.width;
      canvas.height = imageElement.height;
      context.drawImage(imageElement, 0, 0, canvas.width, canvas.height);

      const imageData = context.getImageData(0, 0, canvas.width, canvas.height);
      const data = imageData.data;
      let r = 0,
        g = 0,
        b = 0;

      for (let i = 0; i < data.length; i += 4) {
        r += data[i];
        g += data[i + 1];
        b += data[i + 2];
      }

      r = Math.floor(r / (data.length / 4));
      g = Math.floor(g / (data.length / 4));
      b = Math.floor(b / (data.length / 4));

      return { r, g, b };
    }

    function rgbToHex({ r, g, b }) {
      return `rgb(${r}, ${g}, ${b})`;
    }

    function getLuminance({ r, g, b }) {
      const a = [r, g, b].map(function (v) {
        v /= 255;
        return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
      });
      return a[0] * 0.2126 + a[1] * 0.7152 + a[2] * 0.0722;
    }

    function getContrastColor(rgb) {
      const luminance = getLuminance(rgb);
      return luminance > 0.5 ? 'black' : 'white';
    }

    function applyGradientBackground() {
      const averageColor = getAverageColor(profilePicture);
      const color1 = rgbToHex(averageColor);
      const color2 = rgbToHex(averageColor); // Example second color for gradient
      const contrastColor = getContrastColor(averageColor);

      customColorItems.forEach((item) => {
        item.style.color = color1;
      });
    }

    profilePicture.onload = applyGradientBackground;
    if (profilePicture.complete) {
      applyGradientBackground();
    }
  });
}

// Get user ID from the page (either from current user or public profile)
function getUserSpotifyId() {
  // // Try to get from data attributes first
  // const userDataElement = document.getElementById('user-data');
  // if (userDataElement && userDataElement.dataset.spotifyId) {
  //   return userDataElement.dataset.spotifyId;
  // }

  // Try to get from global window data (fallback)
  if (window.spotifyUserData && window.spotifyUserData.spotify_id) {
    return window.spotifyUserData.spotify_id;
  }

  // Try to get from URL path for public profiles (/spotify/u/USER_ID)
  const pathMatch = window.location.pathname.match(/\/spotify\/u\/([^\/]+)/);
  if (pathMatch) {
    return pathMatch[1];
  }

  // For authenticated users, get from user info element
  const userIdElement = document.querySelector('.user-info p');
  if (userIdElement) {
    return userIdElement.textContent.trim();
  }

  return null;
}

// Check if this is a public profile
function isPublicProfile() {
  // Try to get from data attributes first
  const userDataElement = document.getElementById('user-data');
  if (userDataElement && userDataElement.dataset.isPublic) {
    return userDataElement.dataset.isPublic === 'true';
  }

  // Try to get from global window data (fallback)
  if (
    window.spotifyUserData &&
    typeof window.spotifyUserData.is_public !== 'undefined'
  ) {
    return window.spotifyUserData.is_public;
  }

  return window.location.pathname.includes('/spotify/u/');
}

async function fetchUserCurrentlyPlaying() {
  try {
    const userId = getUserSpotifyId();
    const isPublic = isPublicProfile();

    let url;
    if (isPublic && userId) {
      url = `/spotify/u/${userId}/currently-playing`;
    } else {
      url = '/spotify/currently-playing';
    }

    const response = await fetch(url);
    const data = await response.json();
    const container = document.getElementById('currently-playing');

    if (data.message || data.error) {
      container.classList.add('no-hover');
      container.innerHTML = `<span class="cp-message">${
        data.message || data.error
      }</span>`;
    } else {
      const item = data.currently_playing || data;
      container.innerHTML = `
      <div>
        <h2>Currently Playing</h2>
        <img class='spotify-album-image' src="${
          item.currently_playing_type === 'episode'
            ? item.item.show.images[0].url
            : item.item.album.images[0].url
        }" alt="${
        item.currently_playing_type === 'episode'
          ? item.item.show.name
          : item.item.album.name
      }"/>
        <ul class="track-info">
        <li class="track-name">${item.item.name}</li>
        ${
          item.currently_playing_type === 'episode'
            ? `
        <li class="artist-line"><span class="label">Show</span> ${item.item.show.name}</li>
        <li class="album-line"><span class="label">Publisher</span> ${item.item.show.publisher}</li>
        `
            : `
        <li class="artist-line"><span class="label">Artists</span> ${item.item.artists
          .map((artist) => artist.name)
          .join(', ')}</li>
        <li class="album-line"><span class="label">Album</span> ${
          item.item.album.name
        }</li>
        `
        }
        </ul>
      </div>
      `;
    }
  } catch (error) {
    console.error('Error fetching currently playing data:', error);
  }
}

async function fetchUserTopItems() {
  try {
    const userId = getUserSpotifyId();
    const isPublic = isPublicProfile();

    let artistsUrl, tracksUrl;
    if (isPublic && userId) {
      artistsUrl = `/spotify/u/${userId}/top-artists`;
      tracksUrl = `/spotify/u/${userId}/top-tracks`;
    } else {
      artistsUrl = '/spotify/top-artists-and-tracks';
      tracksUrl = '/spotify/top-artists-and-tracks';
    }

    const topArtistsContainer = document.getElementById('user-top-artists');
    const topTracksContainer = document.getElementById('user-top-tracks');
    const artistsList = document.getElementById('top-artists-list');
    const tracksList = document.getElementById('top-tracks-list');

    if (isPublic && userId) {
      // Fetch artists and tracks separately for public profiles
      const [artistsResponse, tracksResponse] = await Promise.all([
        fetch(artistsUrl),
        fetch(tracksUrl),
      ]);

      const artistsData = await artistsResponse.json();
      const tracksData = await tracksResponse.json();

      if (artistsData.error || tracksData.error) {
        topArtistsContainer.innerText =
          artistsData.error || 'Error loading artists';
        topTracksContainer.innerText =
          tracksData.error || 'Error loading tracks';
        return;
      }

      // Display top artists
      if (artistsData.top_artists) {
        artistsData.top_artists.forEach((artist) => {
          const li = document.createElement('li');
          li.classList.add('list-item');
          if (artist.images.length > 0) {
            const randomIndex = Math.floor(
              Math.random() * artist.images.length
            );
            li.style.backgroundImage = `url(${artist.images[randomIndex].url})`;
          }
          li.innerHTML = `
          <a id="spotify_artist_url_${artist.id}" href="${artist.external_urls.spotify}" target="_blank">
            <ul>
            <li class="list-name">${artist.name}</li>
              </ul>
          </a>
          `;
          artistsList.appendChild(li);
          observeElement(li);
        });
        topArtistsContainer.appendChild(artistsList);
      }

      // Display top tracks
      if (tracksData.top_tracks) {
        tracksData.top_tracks.forEach((track) => {
          const li = document.createElement('li');
          li.classList.add('user-top-track-item');
          li.innerHTML = `
            <p><span><span class="item-name"><span class="popularity">${
              track.popularity
            }</span><a id="spotify_track_url_${track.id}" href="${
            track.external_urls.spotify
          }" target="_blank">${
            track.name
          }</a></span> - <span class="item-artist">${track.artists
            .map((artist) => artist.name)
            .join(', ')}</span></span></p>     
          `;
          tracksList.appendChild(li);
          observeElement(li);
        });
        topTracksContainer.appendChild(tracksList);
      }
    } else {
      // Original combined endpoint for authenticated users
      const response = await fetch(artistsUrl);
      const data = await response.json();

      if (data.error) {
        topArtistsContainer.innerText = data.error;
        topTracksContainer.innerText = data.error;
      } else {
        // Display top artists
        data.top_artists.forEach((artist) => {
          const li = document.createElement('li');
          li.classList.add('list-item');
          if (artist.images.length > 0) {
            const randomIndex = Math.floor(
              Math.random() * artist.images.length
            );
            li.style.backgroundImage = `url(${artist.images[randomIndex].url})`;
          } else {
            li.style.backgroundImage = `url(${artist.images[0].url})`;
          }
          li.innerHTML = `
          <a id="spotify_artist_url_${artist.id}" href="${artist.external_urls.spotify}" target="_blank">
            <ul>
            <li class="list-name">${artist.name}</li>
              </ul>
          </a>
          `;
          artistsList.appendChild(li);
          observeElement(li);
        });
        topArtistsContainer.appendChild(artistsList);

        // Display top tracks
        data.top_tracks.forEach((track) => {
          const li = document.createElement('li');
          li.classList.add('user-top-track-item');
          li.innerHTML = `
            <p><span><span class="item-name"><span class="popularity">${
              track.popularity
            }</span><a id="spotify_track_url_${track.id}" href="${
            track.external_urls.spotify
          }" target="_blank">${
            track.name
          }</a></span> - <span class="item-artist">${track.artists
            .map((artist) => artist.name)
            .join(', ')}</span></span></p>     
          `;
          tracksList.appendChild(li);
          observeElement(li);
        });
        topTracksContainer.appendChild(tracksList);
      }
    }
  } catch (error) {
    console.error('Error fetching user top items:', error);
  }
}

async function fetchUserSavedTracks() {
  try {
    const response = await fetch('/spotify/user-saved-tracks');
    const data = await response.json();
    const savedTracksContainer = document.getElementById('user-saved-tracks');
    const tracksList = document.getElementById('saved-tracks');

    if (data.error) {
      savedTracksContainer.innerText = data.error;
    } else {
      tracksList.classList.add('column-list');
      data.forEach((item) => {
        const track = item;
        const li = document.createElement('li');
        li.classList.add('saved-track-item');
        li.innerHTML = `
          <p><span class="item-name"><span class="item-added">${track.added_at}</span><a href="${track.url}" target="_blank">${track.name}</a></span> - <span class="item-artist">${track.artist}</span></p>                 
        `;
        tracksList.appendChild(li);
        observeElement(li);
      });
      savedTracksContainer.appendChild(tracksList);
    }
  } catch (error) {
    console.error('Error fetching user saved tracks:', error);
  }
}

async function fetchUserPlaylists() {
  try {
    const userId = getUserSpotifyId();
    const isPublic = isPublicProfile();

    let url;
    if (isPublic && userId) {
      url = `/spotify/u/${userId}/playlists`;
    } else {
      url = '/spotify/playlists';
    }

    const response = await fetch(url);
    const data = await response.json();
    const container = document.getElementById('user-lists');
    const ul = document.getElementById('playlist-list');

    if (data.error) {
      container.innerText = data.error;
    } else {
      const playlists = data.playlists || data.items || [];
      playlists.forEach((playlist) => {
        const li = document.createElement('li');
        li.classList.add('list-item');
        if (playlist.images && playlist.images.length > 0) {
          li.style.backgroundImage = `url(${playlist.images[0].url})`;
        }
        li.innerHTML = `
        <div class="list-info">
          <ul>
            <li class="list-name">${playlist.name}</li>
            <li>${playlist.tracks.total} Tracks</li>
          </ul>
        </div>
        `;

        li.addEventListener('click', async () => {
          const playlistId = playlist.id;

          try {
            const response = await fetch(
              `/spotify/playlist-tracks/${playlistId}`
            );
            const data = await response.json();
            const body = document.querySelector('body');
            const modal = document.createElement('div');
            modal.classList.add('modal');
            modal.innerHTML = `
              <div class="modal-content">
            <span class="close-button">&times;</span>
            <h2>${playlist.name}</h2>
            ${
              playlist.images && playlist.images.length > 0
                ? `<img src="${playlist.images[0].url}"/>`
                : ''
            }
            <ul class="list-tracks">
            ${data.items
              .map(
                (track) => `
              <li>
              <p><strong><a href="${
                track.track.external_urls.spotify
              }" target="_blank">${
                  track.track.name
                }</a></strong> - ${track.track.artists
                  .map((artist) => artist.name)
                  .join(', ')}</p>
              </li>
            `
              )
              .join('')}
            </ul>
              </div>
            `;

            document.body.appendChild(modal);
            body.style.overflow = 'hidden';

            const closeButton = modal.querySelector('.close-button');
            closeButton.addEventListener('click', () => {
              modal.remove();
              body.style.overflow = 'auto';
            });

            modal.addEventListener('click', (e) => {
              if (e.target === modal) {
                modal.remove();
                body.style.overflow = 'auto';
              }
            });
          } catch (error) {
            console.error('Error fetching playlist tracks:', error);
          }
        });
        ul.appendChild(li);
        observeElement(li);
      });
      container.appendChild(ul);
    }
  } catch (error) {
    console.error('Error fetching user playlists:', error);
  }
}

// Initialize page based on profile type
function initializePage() {
  const isPublic = isPublicProfile();
  const userId = getUserSpotifyId();

  if (!userId) {
    console.error('No user ID found');
    return;
  }

  console.log('Initializing page for user:', userId, 'Public:', isPublic);

  // Always fetch these for both public and private profiles
  fetchUserCurrentlyPlaying();
  fetchUserTopItems();
  fetchUserPlaylists();

  // Only fetch saved tracks for non-public profiles (private authenticated users)
  if (!isPublic) {
    fetchUserSavedTracks();
  }

  applyUserImageColor();
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', initializePage);

window.addEventListener('load', () => {
  setupIntersectionAnimations();
});
