window.onSpotifyWebPlaybackSDKReady = () => {
  const token = '{{ token_info }}';
  const player = new Spotify.Player({
    name: 'Web Playback SDK Quick Start Player',
    getOAuthToken: (cb) => {
      cb(token);
    },
    volume: 0.5,
  });
  // Error handling
  player.addListener('initialization_error', ({ message }) => {
    console.error(message);
  });
  player.addListener('authentication_error', ({ message }) => {
    console.error(message);
  });
  player.addListener('account_error', ({ message }) => {
    console.error(message);
  });
  player.addListener('playback_error', ({ message }) => {
    console.error(message);
  });

  // Playback status updates
  player.addListener('player_state_changed', (state) => {
    console.log(state);
  });

  // Ready
  player.addListener('ready', ({ device_id }) => {
    console.log('Ready with Device ID', device_id);
  });

  // Not Ready
  player.addListener('not_ready', ({ device_id }) => {
    console.log('Device ID has gone offline', device_id);
  });

  document.getElementById('togglePlay').onclick = function () {
    player.togglePlay();
  };

  // Connect to the player!
  player.connect().then((success) => {
    if (success) {
      console.log('The Web Playback SDK successfully connected to Spotify!');
    }
  });
};
async function fetchCurrentlyPlaying() {
  try {
    const response = await fetch('/currently-playing');
    const data = await response.json();
    const container = document.getElementById('currently-playing');
    const trackUriInput = document.getElementById('trackUriInput');

    if (data.message) {
      container.classList.add('no-hover');
      container.innerHTML = `<span class="cp-message">${data.message}</span>`;
    } else {
      // Populate the input field with the track URI if a track is playing
      if (data.item && data.item.uri) {
        trackUriInput.value = data.item.uri;
      }
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
        <a href="${playlist.external_urls.spotify}" target="_blank">
          <ul>
          <li class="playlist-name">${playlist.name}</li>
          <li>${playlist.tracks.total} Tracks</li>
            </ul>
            </a>
        `;
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

function validateTrackUriInput() {
  const trackUri = document.getElementById('trackUriInput').value.trim();
  if (!trackUri) {
    document.getElementById('responseMessage').innerText =
      'Please enter a Spotify Track URI!';
    return false;
  }
  return trackUri;
}
function playTrack() {
  const trackUri = validateTrackUriInput();
  if (!trackUri) return;

  fetch('http://127.0.0.1:5000/play', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ track_uri: trackUri }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        document.getElementById('responseMessage').innerText =
          'Error: ' + data.error;
      } else {
        document.getElementById('responseMessage').innerText = 'Track playing!';
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      document.getElementById('responseMessage').innerText =
        'Failed to play the track.';
    });
}
function nextTrack() {
  const trackUri = validateTrackUriInput();
  if (!trackUri) return;
  fetch('http://127.0.0.1:5000/next', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      track_uri: document.getElementById('trackUriInput').value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        document.getElementById('responseMessage').innerText =
          'Error: ' + data.error;
      } else {
        document.getElementById('responseMessage').innerText =
          'Playing next track!';
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      document.getElementById('responseMessage').innerText =
        'Failed to play the next track.';
    });
}

function previousTrack() {
  const trackUri = validateTrackUriInput();
  if (!trackUri) return;
  fetch('http://127.0.0.1:5000/previous', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      track_uri: document.getElementById('trackUriInput').value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        document.getElementById('responseMessage').innerText =
          'Error: ' + data.error;
      } else {
        document.getElementById('responseMessage').innerText =
          'Playing previous track!';
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      document.getElementById('responseMessage').innerText =
        'Failed to play the previous track.';
    });
}

function pauseTrack() {
  const trackUri = validateTrackUriInput();
  if (!trackUri) return;
  fetch('http://127.0.0.1:5000/pause', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      track_uri: document.getElementById('trackUriInput').value,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        document.getElementById('responseMessage').innerText =
          'Error: ' + data.error;
      } else {
        document.getElementById('responseMessage').innerText = 'Track paused!';
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      document.getElementById('responseMessage').innerText =
        'Failed to pause the track.';
    });
}

function repeatTrack() {
  const trackUri = validateTrackUriInput();
  if (!trackUri) return;
  fetch('http://127.0.0.1:5000/repeat', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      track_uri: document.getElementById('trackUriInput').value,
      state: 'track',
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        document.getElementById('responseMessage').innerText =
          'Error: ' + data.error;
      } else {
        document.getElementById('responseMessage').innerText =
          'Track set to repeat!';
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      document.getElementById('responseMessage').innerText =
        'Failed to set repeat.';
    });
}

function shuffleTrack() {
  const trackUri = validateTrackUriInput();
  if (!trackUri) return;
  fetch('http://127.0.0.1:5000/shuffle', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      track_uri: document.getElementById('trackUriInput').value,
      state: true,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.error) {
        document.getElementById('responseMessage').innerText =
          'Error: ' + data.error;
      } else {
        document.getElementById('responseMessage').innerText =
          'Shuffle enabled!';
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      document.getElementById('responseMessage').innerText =
        'Failed to enable shuffle.';
    });
}
document.addEventListener('DOMContentLoaded', function () {
  const profilePicture = document.getElementById('user-profile-picture');
  const nav = document.querySelector('nav');
  const playbackControls = document.querySelector('#playback-controls');
  const icons = playbackControls.querySelectorAll('.fa-solid');
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

    icons.forEach((icon) => {
      icon.style.color = contrastColor;
    });
  }

  profilePicture.onload = applyGradientBackground;
  if (profilePicture.complete) {
    applyGradientBackground();
  }
});
