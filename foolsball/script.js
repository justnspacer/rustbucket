class NFLDashboardApp {
    constructor() {
        this.teams = [];
        this.filteredTeams = [];
        this.players = [];
        this.filteredPlayers = [];
        this.currentTab = 'teams';
        this.positions = [];
        this.teamsList = [];
        this.init();
    }

    async init() {
        await this.loadTeams();
        await this.loadPositions();
        this.setupEventListeners();
        this.renderTeams();
        this.setupTabs();
        this.hideLoading();
    }

    async loadTeams() {
        try {
            console.log('Starting to load teams...');
            
            // Use static JSON file for now to isolate the issue
            console.log('Loading from teams_data.json...');
            const response = await fetch('teams_data.json');
            console.log('Response status:', response.status);
            console.log('Response ok:', response.ok);
            
            if (!response.ok) {
                throw new Error(`Failed to fetch teams_data.json: ${response.status} ${response.statusText}`);
            }
            
            // Get response as text first to debug
            const text = await response.text();
            console.log('Response text length:', text.length);
            console.log('Response first 100 chars:', text.substring(0, 100));
            
            if (!text.trim()) {
                throw new Error('Empty response received from teams_data.json');
            }
            
            // Parse JSON
            let data;
            try {
                data = JSON.parse(text);
                console.log('JSON parsed successfully');
            } catch (parseError) {
                console.error('JSON Parse Error:', parseError);
                console.error('Response text sample:', text.substring(0, 500));
                throw new Error(`Invalid JSON in teams_data.json: ${parseError.message}`);
            }
            
            // Validate data structure
            if (!Array.isArray(data)) {
                throw new Error(`Expected array but got ${typeof data}`);
            }
            
            if (data.length === 0) {
                throw new Error('No teams found in data');
            }
            
            this.teams = data;
            this.filteredTeams = [...this.teams];
            console.log(`✅ Teams loaded successfully:`, this.teams.length);
            
        } catch (error) {
            console.error('❌ Error loading teams:', error);
            this.showError(`Failed to load team data: ${error.message}`);
        }
    }

    async loadPositions() {
        try {
            console.log('Loading positions and team list...');
            
            // Load positions
            const posResponse = await fetch('/api/positions');
            if (posResponse.ok) {
                this.positions = await posResponse.json();
                console.log('Positions loaded:', this.positions.length);
            }
            
            // Create teams list from loaded teams
            this.teamsList = [...new Set(this.teams.map(t => t.team_abbr))].sort();
            
            // Populate filter dropdowns
            this.populateFilters();
            
        } catch (error) {
            console.error('Error loading positions:', error);
        }
    }

    populateFilters() {
        // Populate position filter
        const positionFilter = document.getElementById('positionFilter');
        if (positionFilter) {
            positionFilter.innerHTML = '<option value="">All Positions</option>';
            this.positions.forEach(position => {
                if (position) {
                    const option = document.createElement('option');
                    option.value = position;
                    option.textContent = position;
                    positionFilter.appendChild(option);
                }
            });
        }
        
        // Populate team filter for players
        const teamFilterPlayers = document.getElementById('teamFilterPlayers');
        if (teamFilterPlayers) {
            teamFilterPlayers.innerHTML = '<option value="">All Teams</option>';
            this.teamsList.forEach(team => {
                if (team) {
                    const option = document.createElement('option');
                    option.value = team;
                    option.textContent = team;
                    teamFilterPlayers.appendChild(option);
                }
            });
        }
    }

    setupTabs() {
        // Tab switching functionality
        document.querySelectorAll('.tab-button').forEach(button => {
            button.addEventListener('click', () => {
                const tabName = button.dataset.tab;
                this.switchTab(tabName);
            });
        });
    }

    switchTab(tabName) {
        this.currentTab = tabName;
        
        // Update tab buttons
        document.querySelectorAll('.tab-button').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}Tab`).classList.add('active');
        
        // Load data if needed
        if (tabName === 'players' && this.players.length === 0) {
            this.showLoading('Loading players...');
            this.searchPlayers();
        }
    }

    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('searchInput');
        searchInput.addEventListener('input', (e) => {
            this.filterTeams();
        });

        // Filter functionality
        const conferenceFilter = document.getElementById('conferenceFilter');
        const divisionFilter = document.getElementById('divisionFilter');
        
        conferenceFilter.addEventListener('change', () => this.filterTeams());
        divisionFilter.addEventListener('change', () => this.filterTeams());

        // Modal functionality
        const modal = document.getElementById('teamModal');
        const closeBtn = document.querySelector('.close');
        
        closeBtn.addEventListener('click', () => this.closeModal());
        
        window.addEventListener('click', (e) => {
            if (e.target === modal) {
                this.closeModal();
            }
        });

        // Escape key to close modal
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
                this.closePlayerModal();
            }
        });

        // Player search functionality
        const playerSearchBtn = document.getElementById('searchPlayersBtn');
        const playerSearchInput = document.getElementById('playerSearchInput');
        
        if (playerSearchBtn) {
            playerSearchBtn.addEventListener('click', () => this.searchPlayers());
        }
        
        if (playerSearchInput) {
            playerSearchInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.searchPlayers();
                }
            });
        }

        // Modal functionality for players
        window.addEventListener('click', (e) => {
            const teamModal = document.getElementById('teamModal');
            const playerModal = document.getElementById('playerModal');
            
            if (e.target === teamModal) {
                this.closeModal();
            }
            if (e.target === playerModal) {
                this.closePlayerModal();
            }
        });
    }

    async searchPlayers() {
        try {
            this.showLoading('Searching players...');
            
            const nameQuery = document.getElementById('playerSearchInput').value;
            const positionFilter = document.getElementById('positionFilter').value;
            const teamFilter = document.getElementById('teamFilterPlayers').value;
            
            // Build query parameters
            const params = new URLSearchParams();
            if (nameQuery) params.append('name', nameQuery);
            if (positionFilter) params.append('position', positionFilter);
            if (teamFilter) params.append('team', teamFilter);
            params.append('limit', '100'); // Limit results
            
            const response = await fetch(`/api/players/search?${params}`);
            if (!response.ok) {
                throw new Error(`Search failed: ${response.status}`);
            }
            
            this.players = await response.json();
            this.filteredPlayers = [...this.players];
            
            console.log(`Found ${this.players.length} players`);
            this.renderPlayers();
            this.hideLoading();
            
        } catch (error) {
            console.error('Error searching players:', error);
            this.showPlayerError(`Player search failed: ${error.message}`);
            this.hideLoading();
        }
    }

    renderPlayers() {
        const grid = document.getElementById('playersGrid');
        
        if (!this.filteredPlayers || this.filteredPlayers.length === 0) {
            grid.innerHTML = `
                <div class="no-results">
                    <h3>No players found</h3>
                    <p>Try adjusting your search criteria or search terms.</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = this.filteredPlayers.map(player => this.createPlayerCard(player)).join('');
        
        // Add click listeners to player cards
        document.querySelectorAll('.player-card').forEach(card => {
            card.addEventListener('click', () => {
                const playerId = card.dataset.playerId;
                const player = this.players.find(p => p.player_id === playerId);
                this.showPlayerModal(player);
            });
        });
    }

    createPlayerCard(player) {
        const initials = player.player_name ? 
            player.player_name.split(' ').map(n => n[0]).join('').substring(0, 2) : 'P';
        
        // Get key stats to display
        const targetShare = player.tgt_sh ? (player.tgt_sh * 100).toFixed(1) : '0.0';
        const receivingYards = player.receiving_yards || 0;
        const receptions = player.receptions || 0;
        const pprPoints = player.fantasy_points_ppr ? player.fantasy_points_ppr.toFixed(1) : '0.0';
        
        return `
            <div class="player-card" data-player-id="${player.player_id}">
                <div class="player-header">
                    <div class="player-avatar">${initials}</div>
                    <div class="player-info">
                        <h3>${player.player_name || 'Unknown'}</h3>
                        <div class="player-meta">
                            <span class="position-badge">${player.position || 'N/A'}</span>
                            <span class="team-badge">${player.team || 'FA'}</span>
                        </div>
                    </div>
                </div>
                <div class="player-stats">
                    <div class="stat-item">
                        <div class="stat-label">Target Share</div>
                        <div class="stat-value">${targetShare}%</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Rec Yards</div>
                        <div class="stat-value">${receivingYards}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Receptions</div>
                        <div class="stat-value">${receptions}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">PPR Points</div>
                        <div class="stat-value">${pprPoints}</div>
                    </div>
                </div>
            </div>
        `;
    }

    filterTeams() {
        const searchTerm = document.getElementById('searchInput').value.toLowerCase();
        const conferenceFilter = document.getElementById('conferenceFilter').value;
        const divisionFilter = document.getElementById('divisionFilter').value;

        this.filteredTeams = this.teams.filter(team => {
            const matchesSearch = !searchTerm || 
                team.team_name.toLowerCase().includes(searchTerm) ||
                team.team_nick.toLowerCase().includes(searchTerm) ||
                team.team_abbr.toLowerCase().includes(searchTerm);

            const matchesConference = !conferenceFilter || team.team_conf === conferenceFilter;
            const matchesDivision = !divisionFilter || team.team_division === divisionFilter;

            return matchesSearch && matchesConference && matchesDivision;
        });

        this.renderTeams();
    }

    renderTeams() {
        const grid = document.getElementById('teamsGrid');
        
        if (this.filteredTeams.length === 0) {
            grid.innerHTML = `
                <div class="no-results">
                    <h3>No teams found</h3>
                    <p>Try adjusting your search or filter criteria.</p>
                </div>
            `;
            return;
        }

        grid.innerHTML = this.filteredTeams.map(team => this.createTeamCard(team)).join('');
        
        // Add click listeners to team cards
        document.querySelectorAll('.team-card').forEach(card => {
            card.addEventListener('click', () => {
                const teamAbbr = card.dataset.teamAbbr;
                const team = this.teams.find(t => t.team_abbr === teamAbbr);
                this.showTeamModal(team);
            });
        });
    }

    createTeamCard(team) {
        return `
            <div class="team-card" data-team-abbr="${team.team_abbr}">
                <div class="team-header">
                    <img src="${team.team_logo_espn || team.team_logo_wikipedia}" 
                         alt="${team.team_name} logo" 
                         class="team-logo"
                         onerror="this.style.display='none'">
                    <div class="team-info">
                        <h3>${team.team_name}</h3>
                        <div class="team-abbr">${team.team_abbr}</div>
                    </div>
                </div>
                <div class="team-details">
                    <div class="detail-item">
                        <div class="detail-label">Conference</div>
                        <div class="detail-value">
                            <span class="conference-badge conference-${team.team_conf.toLowerCase()}">
                                ${team.team_conf}
                            </span>
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Division</div>
                        <div class="detail-value">${team.team_division}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Nickname</div>
                        <div class="detail-value">${team.team_nick}</div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">Team ID</div>
                        <div class="detail-value">${team.team_id}</div>
                    </div>
                </div>
            </div>
        `;
    }

    showTeamModal(team) {
        const modal = document.getElementById('teamModal');
        const teamDetails = document.getElementById('teamDetails');
        
        teamDetails.innerHTML = `
            <div class="modal-team-header">
                <img src="${team.team_logo_espn || team.team_logo_wikipedia}" 
                     alt="${team.team_name} logo" 
                     class="modal-team-logo"
                     onerror="this.style.display='none'">
                <div class="modal-team-info">
                    <h2>${team.team_name}</h2>
                    <div class="modal-team-abbr">${team.team_abbr} • ${team.team_nick}</div>
                </div>
            </div>
            
            <div class="modal-details">
                <div class="modal-detail-item">
                    <div class="detail-label">Conference</div>
                    <div class="detail-value">
                        <span class="conference-badge conference-${team.team_conf.toLowerCase()}">
                            ${team.team_conf}
                        </span>
                    </div>
                </div>
                
                <div class="modal-detail-item">
                    <div class="detail-label">Division</div>
                    <div class="detail-value">${team.team_division}</div>
                </div>
                
                <div class="modal-detail-item">
                    <div class="detail-label">Team ID</div>
                    <div class="detail-value">${team.team_id}</div>
                </div>
                
                <div class="modal-detail-item">
                    <div class="detail-label">Primary Color</div>
                    <div class="detail-value">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <div style="width: 20px; height: 20px; background-color: ${team.team_color}; border-radius: 4px; border: 1px solid #ddd;"></div>
                            ${team.team_color}
                        </div>
                    </div>
                </div>
                
                ${team.team_color2 ? `
                <div class="modal-detail-item">
                    <div class="detail-label">Secondary Color</div>
                    <div class="detail-value">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <div style="width: 20px; height: 20px; background-color: ${team.team_color2}; border-radius: 4px; border: 1px solid #ddd;"></div>
                            ${team.team_color2}
                        </div>
                    </div>
                </div>
                ` : ''}
                
                ${team.team_color3 ? `
                <div class="modal-detail-item">
                    <div class="detail-label">Tertiary Color</div>
                    <div class="detail-value">
                        <div style="display: flex; align-items: center; gap: 0.5rem;">
                            <div style="width: 20px; height: 20px; background-color: ${team.team_color3}; border-radius: 4px; border: 1px solid #ddd;"></div>
                            ${team.team_color3}
                        </div>
                    </div>
                </div>
                ` : ''}
                
                ${team.team_wordmark ? `
                <div class="modal-detail-item">
                    <div class="detail-label">Wordmark</div>
                    <div class="detail-value">
                        <img src="${team.team_wordmark}" alt="${team.team_name} wordmark" style="max-width: 150px; max-height: 40px;">
                    </div>
                </div>
                ` : ''}
            </div>
        `;
        
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    showPlayerModal(player) {
        const modal = document.getElementById('playerModal');
        const playerDetails = document.getElementById('playerDetails');
        
        const initials = player.player_name ? 
            player.player_name.split(' ').map(n => n[0]).join('').substring(0, 2) : 'P';
        
        // Organize performance metrics
        const performanceMetrics = [
            { label: 'Target Share', value: player.tgt_sh ? (player.tgt_sh * 100).toFixed(1) + '%' : 'N/A', desc: 'Share of team targets' },
            { label: 'Air Yards Share', value: player.ay_sh ? (player.ay_sh * 100).toFixed(1) + '%' : 'N/A', desc: 'Share of team air yards' },
            { label: 'YAC Share', value: player.yac_sh ? (player.yac_sh * 100).toFixed(1) + '%' : 'N/A', desc: 'Yards after catch share' },
            { label: 'WOPR', value: player.wopr_x ? player.wopr_x.toFixed(2) : 'N/A', desc: 'Weighted opportunity rating' },
            { label: 'Receiving Yards Share', value: player.ry_sh ? (player.ry_sh * 100).toFixed(1) + '%' : 'N/A', desc: 'Share of team receiving yards' },
            { label: 'Dominator Rating', value: player.dom ? player.dom.toFixed(2) : 'N/A', desc: 'Overall domination of team offense' },
            { label: 'W8DOM', value: player.w8dom ? player.w8dom.toFixed(2) : 'N/A', desc: 'Weighted dominator (yards favored)' },
            { label: 'YPTMPA', value: player.yptmpa ? player.yptmpa.toFixed(2) : 'N/A', desc: 'Receiving yards per team pass attempt' },
            { label: 'PPR Share', value: player.ppr_sh ? (player.ppr_sh * 100).toFixed(1) + '%' : 'N/A', desc: 'PPR fantasy points share' }
        ];
        
        const basicStats = [
            { label: 'Targets', value: player.targets || 0 },
            { label: 'Receptions', value: player.receptions || 0 },
            { label: 'Receiving Yards', value: player.receiving_yards || 0 },
            { label: 'Receiving TDs', value: player.receiving_tds || 0 },
            { label: 'PPR Points', value: player.fantasy_points_ppr ? player.fantasy_points_ppr.toFixed(1) : '0.0' }
        ];
        
        playerDetails.innerHTML = `
            <div class="modal-team-header">
                <div class="player-avatar" style="width: 80px; height: 80px; font-size: 1.8rem;">${initials}</div>
                <div class="modal-team-info">
                    <h2>${player.player_name || 'Unknown Player'}</h2>
                    <div class="modal-team-abbr">
                        <span class="position-badge">${player.position || 'N/A'}</span>
                        <span class="team-badge">${player.team || 'FA'}</span>
                        ${player.jersey_number ? `• #${player.jersey_number}` : ''}
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 2rem;">
                <h3 style="color: #2d3748; margin-bottom: 1rem;">Basic Information</h3>
                <div class="modal-details" style="grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));">
                    ${player.height ? `<div class="modal-detail-item">
                        <div class="detail-label">Height</div>
                        <div class="detail-value">${player.height}</div>
                    </div>` : ''}
                    ${player.weight ? `<div class="modal-detail-item">
                        <div class="detail-label">Weight</div>
                        <div class="detail-value">${player.weight} lbs</div>
                    </div>` : ''}
                    ${player.college ? `<div class="modal-detail-item">
                        <div class="detail-label">College</div>
                        <div class="detail-value">${player.college}</div>
                    </div>` : ''}
                    ${player.years_exp ? `<div class="modal-detail-item">
                        <div class="detail-label">Experience</div>
                        <div class="detail-value">${player.years_exp} years</div>
                    </div>` : ''}
                </div>
            </div>
            
            <div style="margin-bottom: 2rem;">
                <h3 style="color: #2d3748; margin-bottom: 1rem;">Season Stats</h3>
                <div class="modal-details">
                    ${basicStats.map(stat => `
                        <div class="modal-detail-item">
                            <div class="detail-label">${stat.label}</div>
                            <div class="detail-value">${stat.value}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
            
            <div style="margin-bottom: 1rem;">
                <h3 style="color: #2d3748; margin-bottom: 1rem;">Advanced Metrics</h3>
                <div class="modal-details">
                    ${performanceMetrics.map(metric => `
                        <div class="modal-detail-item" title="${metric.desc}">
                            <div class="detail-label">${metric.label}</div>
                            <div class="detail-value">${metric.value}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        const modal = document.getElementById('teamModal');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    closePlayerModal() {
        const modal = document.getElementById('playerModal');
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    showLoading(message = 'Loading NFL Data...') {
        const loading = document.getElementById('loading');
        const loadingText = loading.querySelector('p');
        if (loadingText) {
            loadingText.textContent = message;
        }
        loading.style.display = 'flex';
    }

    hideLoading() {
        const loading = document.getElementById('loading');
        loading.style.display = 'none';
    }

    showError(message) {
        const grid = document.getElementById('teamsGrid');
        grid.innerHTML = `
            <div class="error-message">
                <h3>Error Loading Teams</h3>
                <p>${message}</p>
                <button onclick="location.reload()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">
                    Retry
                </button>
            </div>
        `;
        this.hideLoading();
    }

    showPlayerError(message) {
        const grid = document.getElementById('playersGrid');
        grid.innerHTML = `
            <div class="error-message">
                <h3>Error Loading Players</h3>
                <p>${message}</p>
                <button onclick="location.reload()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">
                    Retry
                </button>
            </div>
        `;
        this.hideLoading();
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new NFLDashboardApp();
});

// Add some additional CSS for error and no results states
const additionalStyles = `
    .no-results, .error-message {
        grid-column: 1 / -1;
        text-align: center;
        padding: 3rem 2rem;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    .no-results h3, .error-message h3 {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2d3748;
        margin-bottom: 0.5rem;
    }
    
    .no-results p, .error-message p {
        color: #718096;
        font-size: 1rem;
    }
    
    .error-message {
        border-left: 4px solid #e53e3e;
    }
`;

// Inject additional styles
const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);
