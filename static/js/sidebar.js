const Sidebar = {
    init() {
        this.setupChannelSwitching();
    },

    setupChannelSwitching() {
        const channelItems = document.querySelectorAll('.channel-item');
        
        channelItems.forEach(item => {
            item.addEventListener('click', () => {
                const channel = item.dataset.channel;
                this.switchChannel(channel);
            });
        });
    },

    switchChannel(channel) {
        document.querySelectorAll('.channel-item').forEach(item => {
            item.classList.remove('active');
        });

        const activeItem = document.querySelector(`[data-channel="${channel}"]`);
        if (activeItem) {
            activeItem.classList.add('active');
        }

        const currentChannelEl = document.getElementById('currentChannel');
        if (currentChannelEl) {
            currentChannelEl.textContent = channel;
        }

        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.placeholder = `Message #${channel}`;
        }

        this.updateChannelDescription(channel);
        this.loadChannelMessages(channel);
    },

    updateChannelDescription(channel) {
        const descriptions = {
            general: 'General discussions and announcements',
            engineering: 'Engineering team discussions and code reviews',
            design: 'Design critiques and creative collaboration',
            photography: 'Share your photos and photography tips',
            gaming: 'Gaming discussions and team coordination'
        };

        const descEl = document.querySelector('.channel-description');
        if (descEl) {
            descEl.textContent = descriptions[channel] || 'Channel discussion';
        }
    },

    loadChannelMessages(channel) {
        Chat.currentChannel = channel;
        
        const container = document.getElementById('messagesContainer');
        if (!container) return;

        container.innerHTML = '';

        const messages = JSON.parse(localStorage.getItem('villageMessages') || '[]');
        const channelMessages = messages.filter(m => m.channel === channel);

        if (channelMessages.length === 0) {
            container.innerHTML = `
                <div style="text-align: center; color: var(--text-secondary); padding: 2rem;">
                    <p>No messages yet. Start the conversation!</p>
                </div>
            `;
            return;
        }

        const groupedMessages = Chat.groupMessages(channelMessages);
        
        groupedMessages.forEach(group => {
            const groupDiv = document.createElement('div');
            groupDiv.className = 'message-group';
            
            group.forEach((msg, idx) => {
                groupDiv.appendChild(Chat.createMessageElement(msg, idx === 0));
            });
            
            container.appendChild(groupDiv);
        });

        Chat.scrollToBottom();
    }
};

document.addEventListener('DOMContentLoaded', () => {
    Sidebar.init();
});