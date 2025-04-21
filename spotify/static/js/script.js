async function fetchCurrentlyPlaying() {
  try {
    const response = await fetch('/currently-playing');
    const data = await response.json();
    const container = document.getElementById('currently-playing');

    if (data.message) {
      container.classList.add('no-hover');
      container.innerHTML = `<span class="cp-message">${data.message}</span>`;
    } else {
      container.innerHTML = `
      <div>
        <h2>Currently Playing</h2>
        <img class='spotify-album-image' src="${
          data.currently_playing_type === 'episode'
            ? data.item.show.images[0].url
            : data.item.album.images[0].url
        }" alt="${
        data.currently_playing_type === 'episode'
          ? data.item.show.name
          : data.item.album.name
      }"/>
        <ul class="track-info">
        <li class="track-name">${data.item.name}</li>
        ${
          data.currently_playing_type === 'episode'
            ? `
        <li class="artist-line"><span class="label">Show</span> ${data.item.show.name}</li>
        <li class="album-line"><span class="label">Publisher</span> ${data.item.show.publisher}</li>
        `
            : `
        <li class="artist-line"><span class="label">Artists</span> ${data.item.artists
          .map((artist) => artist.name)
          .join(', ')}</li>
        <li class="album-line"><span class="label">Album</span> ${
          data.item.album.name
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

fetchCurrentlyPlaying();

async function fetchUserPlaylists() {
  try {
    const response = await fetch('/playlists');
    const data = await response.json();
    const container = document.getElementById('user-playlists');

    if (data.error) {
      container.innerText = data.error;
    } else {
      const ul = document.createElement('ul');
      ul.classList.add('playlists');
      data.items.forEach((playlist) => {
        const li = document.createElement('li');
        li.classList.add('playlist-item');
        li.style.backgroundImage = `url(${playlist.images[0].url})`;
        li.innerHTML = `
        <div class="playlist-info">
          <ul>
            <li class="playlist-name">${playlist.name}</li>
            <li>${playlist.tracks.total} Tracks</li>
          </ul>
        </div>
        `;

        li.addEventListener('click', async () => {
          const playlistId = playlist.id;

          try {
            const response = await fetch(`/playlist-tracks/${playlistId}`);
            const data = await response.json();
            const body = document.querySelector('body');
            const modal = document.createElement('div');
            modal.classList.add('modal');
            modal.innerHTML = `
              <div class="modal-content" style="background-image: url(${
                playlist.images[0].url
              }); background-size: cover;">
            <span class="close-button">&times;</span>
            <h2>${playlist.name}'s Tracks</h2>
            <ul class="playlist-tracks">
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
      });
      container.appendChild(ul);
    }

    document.body.appendChild(container);
  } catch (error) {
    console.error('Error fetching user playlists:', error);
  }
}

fetchUserPlaylists();

async function fetchUserTopItems() {
  try {
    const response = await fetch('/top-artists-and-tracks');
    const data = await response.json();
    const topArtistsContainer = document.getElementById('user-top-artists');
    const topTracksContainer = document.getElementById('user-top-tracks');

    if (data.error) {
      topArtistsContainer.innerText = data.error;
      topTracksContainer.innerText = data.error;
    } else {
      // Display top artists
      const artistsList = document.createElement('ul');
      artistsList.classList.add('top-artists-list');
      data.top_artists.forEach((artist) => {
        const li = document.createElement('li');
        li.classList.add('playlist-item');
        li.classList.add('circle-image');
        li.setAttribute('data-artist-id', artist.id);
        li.setAttribute('data-artist-name', artist.id);
        if (artist.images.length > 0) {
          const randomIndex = Math.floor(Math.random() * artist.images.length);
          li.style.backgroundImage = `url(${artist.images[randomIndex].url})`;
        } else {
          li.style.backgroundImage = `url(${artist.images[0].url})`;
        }
        li.innerHTML = `
        <a href="${artist.external_urls.spotify}" target="_blank">
          <ul>
          <li class="playlist-name">${artist.name}</li>
            </ul>
                    </a>
        `;
        artistsList.appendChild(li);
      });
      topArtistsContainer.appendChild(artistsList);

      // Display top tracks
      const tracksList = document.createElement('ul');
      tracksList.classList.add('top-tracks-list');
      data.top_tracks.forEach((track) => {
        const li = document.createElement('li');
        li.classList.add('user-top-track-item');
        li.innerHTML = `
          <p><span><span class="item-name"><a href="${
            track.external_urls.spotify
          }" target="_blank">${
          track.name
        }</a></span> - <span class="item-artist">${track.artists
          .map((artist) => artist.name)
          .join(', ')}</span></span></p> 
              <p>Popularity: <span class="popularity">${
                track.popularity
              }</span></p>          
        `;
        tracksList.appendChild(li);
      });
      topTracksContainer.appendChild(tracksList);
    }
  } catch (error) {
    console.error('Error fetching user top items:', error);
  }
}

fetchUserTopItems();

async function fetchUserSavedTracks() {
  try {
    const response = await fetch('/user-saved-tracks');
    const data = await response.json();
    const savedTracksContainer = document.getElementById('user-saved-tracks');

    if (data.error) {
      savedTracksContainer.innerText = data.error;
    } else {
      const tracksList = document.createElement('ul');
      tracksList.classList.add('user-saved-tracks');
      data.forEach((item) => {
        const track = item;
        const li = document.createElement('li');
        li.classList.add('saved-track-item');
        li.innerHTML = `
          <p><span class="item-name"><a href="${track.url}" target="_blank">${track.name}</a></span> - <span class="item-artist">${track.artist}</span></p>
          <p>Added: <span class="item-added">${track.added_at}</span></p>          
        `;
        tracksList.appendChild(li);
      });
      savedTracksContainer.appendChild(tracksList);
    }
  } catch (error) {
    console.error('Error fetching user saved tracks:', error);
  }
}

fetchUserSavedTracks();

document.addEventListener('DOMContentLoaded', function () {
  const profilePicture = document.getElementById('user-profile-picture');
  const nav = document.querySelector('nav');
  const userInfo = document.querySelector('.user-info');

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

    document.body.style.background = `linear-gradient(${color1}, ${color2})`;
    document.body.style.color = contrastColor; // Example usage of contrast color
    nav.style.background = contrastColor;
    nav.style.color = color1;
    userInfo.style.color = contrastColor;
  }

  profilePicture.onload = applyGradientBackground;
  if (profilePicture.complete) {
    applyGradientBackground();
  }
});
