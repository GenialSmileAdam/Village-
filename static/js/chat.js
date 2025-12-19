const Chat = {
    currentChannel: 'general',
    currentUser: null,

    init() {
        this.checkAuth();
        this.loadUser();
        this.setupMessageInput();
        this.setupLogout();
        this.loadMessages();
    },

    checkAuth() {
        const user = localStorage.getItem('currentUser');
        if (!user) {
            window.location.href = 'login.html';
        }
    },

    loadUser() {
        const user = JSON.parse(localStorage.getItem('currentUser'));
        if (user) {
            this.currentUser = user;
            const userNameEl = document.querySelector('.user-name');
            const userAvatarEl = document.querySelector('.user-avatar');
            
            if (userNameEl) userNameEl.textContent = user.fullName;
            if (userAvatarEl) {
                userAvatarEl.textContent = user.fullName.split(' ').map(n => n[0]).join('').toUpperCase();
            }
        }
    },

    setupMessageInput() {
        const input = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');

        if (sendBtn) {
            sendBtn.addEventListener('click', () => this.sendMessage());
        }

        if (input) {
            input.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.sendMessage();
                }
            });
        }
    },

    sendMessage() {
        const input = document.getElementById('messageInput');
        const text = input.value.trim();

        if (!text) return;

        const message = {
            id: Date.now(),
            channel: this.currentChannel,
            author: this.currentUser.fullName,
            text: text,
            time: new Date().toLocaleTimeString('en-US', { 
                hour: 'numeric', 
                minute: '2-digit' 
            }),
            userId: this.currentUser.id
        };

        const messages = JSON.parse(localStorage.getItem('villageMessages') || '[]');
        messages.push(message);
        localStorage.setItem('villageMessages', JSON.stringify(messages));

        this.appendMessage(message);
        input.value = '';
        this.scrollToBottom();
    },

    loadMessages() {
        const messages = JSON.parse(localStorage.getItem('villageMessages') || '[]');
        const channelMessages = messages.filter(m => m.channel === this.currentChannel);
        
        const container = document.getElementById('messagesContainer');
        if (!container) return;

        const groupedMessages = this.groupMessages(channelMessages);
        
        groupedMessages.forEach(group => {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'message-group';
            
            group.forEach((msg, idx) => {
                groupDiv.appendChild(this.createMessageElement(msg, idx === 0));
            });
            
            container.appendChild(groupDiv);
        });

        this.scrollToBottom();
    },

    groupMessages(messages) {
        const groups = [];
        let currentGroup = [];
        let lastAuthor = null;

        messages.forEach(msg => {
            if (msg.author !== lastAuthor) {
                if (currentGroup.length > 0) {
                    groups.push(currentGroup);
                }
                currentGroup = [msg];
                lastAuthor = msg.author;
            } else {
                currentGroup.push(msg);
            }
        });

        if (currentGroup.length > 0) {
            groups.push(currentGroup);
        }

        return groups;
    },

    createMessageElement(message, showHeader) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';

        const colors = [
            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
            'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
        ];
        
        const colorIndex = message.userId % colors.length;
        const initials = message.author.split(' ').map(n => n[0]).join('').toUpperCase();

        if (showHeader) {
            messageDiv.innerHTML = `
                <div class="message-avatar" style="background: ${colors[colorIndex]};">${initials}</div>
                <div class="message-content">
                    <div class="message-header">
                        <span class="message-author">${message.author}</span>
                        <span class="message-time">${message.time}</span>
                    </div>
                    <div class="message-text">${message.text}</div>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="message-avatar" style="background: ${colors[colorIndex]};">${initials}</div>
                <div class="message-content">
                    <div class="message-text">${message.text}</div>
                </div>
            `;
        }

        return messageDiv;
    },

    appendMessage(message) {
        const container = document.getElementById('messagesContainer');
        if (!container) return;

        const lastGroup = container.lastElementChild;
        const lastMessage = lastGroup?.lastElementChild;
        const lastAuthor = lastMessage?.querySelector('.message-author')?.textContent;

        if (lastAuthor === message.author) {
            lastGroup.appendChild(this.createMessageElement(message, false));
        } else {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'message-group';
            groupDiv.appendChild(this.createMessageElement(message, true));
            container.appendChild(groupDiv);
        }
    },

    scrollToBottom() {
        const container = document.getElementById('messagesContainer');
        if (container) {
            container.scrollTop = container.scrollHeight;
        }
    },

    setupLogout() {
        const logoutBtn = document.querySelector('.logout-btn');
        if (logoutBtn) {
            logoutBtn.addEventListener('click', () => {
                localStorage.removeItem('currentUser');
                window.location.href = 'login.html';
            });
        }
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Chat.init();
});