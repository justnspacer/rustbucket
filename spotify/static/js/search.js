async function searchUsers() {
  const query = document.getElementById('searchInput').value;
  const resultsDiv = document.getElementById('results');

  resultsDiv.innerHTML = '<div class="loading">Searching...</div>';

  try {
    const response = await fetch(
      `/spotify/search-users?q=${encodeURIComponent(query)}`
    );
    const data = await response.json();

    if (data.users && data.users.length > 0) {
      resultsDiv.innerHTML = data.users
        .map(
          (user) => `
                        <div class="user-card">
                            <img src="${
                              user.images && user.images.length > 0
                                ? user.images[0].url
                                : '/static/default-avatar.png'
                            }" 
                                 alt="${user.display_name}" class="user-avatar">
                            <div>
                                <h3><a href="/spotify/u/${user.spotify_id}">${
            user.display_name || user.spotify_id
          }</a></h3>
                                <p>Followers: ${
                                  user.followers || 0
                                } | Country: ${user.country || 'N/A'}</p>
                                <p>Last updated: ${new Date(
                                  user.last_updated
                                ).toLocaleDateString()}</p>
                            </div>
                        </div>
                    `
        )
        .join('');
    } else {
      resultsDiv.innerHTML = '<div class="loading">No users found.</div>';
    }
  } catch (error) {
    resultsDiv.innerHTML = '<div class="loading">Error searching users.</div>';
    console.error('Error:', error);
  }
}

// Load all users on page load
window.onload = async function () {
  const resultsDiv = document.getElementById('results');
  resultsDiv.innerHTML = '<div class="loading">Loading users...</div>';

  try {
    const response = await fetch('/spotify/users');
    const data = await response.json();

    if (data.users && data.users.length > 0) {
      resultsDiv.innerHTML = data.users
        .map(
          (user) => `
                        <div class="user-card">
                            <img src="${
                              user.images && user.images.length > 0
                                ? user.images[0].url
                                : '/static/default-avatar.png'
                            }" 
                                 alt="${user.display_name}" class="user-avatar">
                            <div>
                                <h3><a href="/spotify/u/${user.spotify_id}">${
            user.display_name || user.spotify_id
          }</a></h3>
                                <p>Followers: ${
                                  user.followers || 0
                                } | Country: ${user.country || 'N/A'}</p>
                                <p>Last updated: ${new Date(
                                  user.last_updated
                                ).toLocaleDateString()}</p>
                            </div>
                        </div>
                    `
        )
        .join('');
    } else {
      resultsDiv.innerHTML =
        '<div class="loading">No users found. Users need to authorize the app first.</div>';
    }
  } catch (error) {
    resultsDiv.innerHTML = '<div class="loading">Error loading users.</div>';
    console.error('Error:', error);
  }
};

// Allow search on Enter key
document
  .getElementById('searchInput')
  .addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
      searchUsers();
    }
  });
