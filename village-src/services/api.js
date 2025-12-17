const API = {
    baseURL: 'http://localhost:3000/api',

    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const token = localStorage.getItem('authToken');

        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        };

        if (token) {
            config.headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Request failed');
            }

            return data;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    auth: {
        async signup(userData) {
            return API.request('/auth/signup', {
                method: 'POST',
                body: JSON.stringify(userData)
            });
        },

        async login(credentials) {
            return API.request('/auth/login', {
                method: 'POST',
                body: JSON.stringify(credentials)
            });
        },

        async logout() {
            return API.request('/auth/logout', {
                method: 'POST'
            });
        }
    },

    users: {
        async getProfile() {
            return API.request('/users/profile');
        },

        async updateProfile(data) {
            return API.request('/users/profile', {
                method: 'PUT',
                body: JSON.stringify(data)
            });
        }
    },

    messages: {
        async getMessages(channelId) {
            return API.request(`/messages/${channelId}`);
        },

        async sendMessage(channelId, content) {
            return API.request('/messages', {
                method: 'POST',
                body: JSON.stringify({ channelId, content })
            });
        },

        async deleteMessage(messageId) {
            return API.request(`/messages/${messageId}`, {
                method: 'DELETE'
            });
        }
    },

    channels: {
        async getChannels() {
            return API.request('/channels');
        },

        async getChannel(channelId) {
            return API.request(`/channels/${channelId}`);
        },

        async createChannel(data) {
            return API.request('/channels', {
                method: 'POST',
                body: JSON.stringify(data)
            });
        },

        async joinChannel(channelId) {
            return API.request(`/channels/${channelId}/join`, {
                method: 'POST'
            });
        }
    }
};

if (typeof module !== 'undefined' && module.exports) {
    module.exports = API;
}