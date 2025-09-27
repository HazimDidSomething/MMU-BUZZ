/**
 * Anonymous Mode Functionality
 * Provides anonymous posting, polls, and time-delayed reveals
 */

class AnonymousMode {
    constructor() {
        this.isAnonymousMode = false;
        this.anonymousSettings = {
            isSecret: false,
            revealType: 'none',
            revealDate: null,
            voteThreshold: 0
        };
        this.init();
    }

    init() {
        this.attachEventListeners();
        this.loadAnonymousSettings();
        this.initializePolls();
    }

    attachEventListeners() {
        // Anonymous mode toggle
        document.addEventListener('click', (e) => {
            if (e.target.closest('.anonymous-toggle')) {
                this.toggleAnonymousMode();
            }
        });

        // Anonymous settings form
        document.addEventListener('change', (e) => {
            if (e.target.closest('.anonymous-settings')) {
                this.updateAnonymousSettings();
            }
        });

        // Poll voting
        document.addEventListener('click', (e) => {
            if (e.target.closest('.anonymous-poll-option')) {
                this.handlePollOptionClick(e);
            }
            if (e.target.closest('.anonymous-poll-submit')) {
                this.submitPollVote(e);
            }
        });

        // Time-delayed reveal countdown
        this.startRevealCountdown();
    }

    toggleAnonymousMode() {
        this.isAnonymousMode = !this.isAnonymousMode;
        const toggle = document.querySelector('.anonymous-toggle');
        
        if (toggle) {
            toggle.classList.toggle('active', this.isAnonymousMode);
            const icon = toggle.querySelector('.toggle-icon');
            if (icon) {
                icon.textContent = this.isAnonymousMode ? '👻' : '👤';
            }
        }

        // Update form visibility
        this.updateFormVisibility();
        this.saveAnonymousSettings();
    }

    updateFormVisibility() {
        const anonymousSettings = document.querySelector('.anonymous-settings');
        if (anonymousSettings) {
            anonymousSettings.style.display = this.isAnonymousMode ? 'block' : 'none';
        }

        // Update post form
        const postForm = document.querySelector('form[method="post"]');
        if (postForm) {
            this.updatePostForm(postForm);
        }
    }

    updatePostForm(form) {
        // Add anonymous mode indicator to form
        let indicator = form.querySelector('.anonymous-mode-indicator');
        if (!indicator) {
            indicator = document.createElement('div');
            indicator.className = 'anonymous-mode-indicator';
            form.insertBefore(indicator, form.firstChild);
        }

        if (this.isAnonymousMode) {
            indicator.innerHTML = `
                <div class="alert alert-info d-flex align-items-center">
                    <i class="bi bi-ghost me-2"></i>
                    <strong>Anonymous Mode Active</strong> - Your post will be anonymous
                </div>
            `;
        } else {
            indicator.innerHTML = '';
        }
    }

    updateAnonymousSettings() {
        const settings = {
            isSecret: document.getElementById('is_secret')?.checked || false,
            revealType: document.getElementById('reveal_type')?.value || 'none',
            revealDate: document.getElementById('reveal_date')?.value || null,
            voteThreshold: parseInt(document.getElementById('vote_threshold')?.value) || 0
        };

        this.anonymousSettings = settings;
        this.saveAnonymousSettings();
        this.updateRevealInfo();
    }

    updateRevealInfo() {
        const revealInfo = document.querySelector('.anonymous-reveal-info');
        if (!revealInfo) return;

        const { revealType, revealDate, voteThreshold } = this.anonymousSettings;

        if (revealType === 'time_delayed' && revealDate) {
            const countdown = this.calculateCountdown(revealDate);
            revealInfo.innerHTML = `
                <div class="icon">⏰</div>
                <div class="countdown">Reveals in: ${countdown}</div>
                <small>Author will be revealed on ${new Date(revealDate).toLocaleDateString()}</small>
            `;
        } else if (revealType === 'community_vote' && voteThreshold > 0) {
            revealInfo.innerHTML = `
                <div class="icon">🗳️</div>
                <div class="countdown">Reveals at ${voteThreshold} votes</div>
                <small>Author will be revealed when post reaches ${voteThreshold} votes</small>
            `;
        } else if (revealType === 'moderator_approved') {
            revealInfo.innerHTML = `
                <div class="icon">👮</div>
                <div class="countdown">Moderator Approval Required</div>
                <small>Author will be revealed only with moderator approval</small>
            `;
        } else {
            revealInfo.style.display = 'none';
        }
    }

    calculateCountdown(revealDate) {
        const now = new Date();
        const reveal = new Date(revealDate);
        const diff = reveal - now;

        if (diff <= 0) return 'Revealed!';

        const days = Math.floor(diff / (1000 * 60 * 60 * 24));
        const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));

        if (days > 0) return `${days}d ${hours}h ${minutes}m`;
        if (hours > 0) return `${hours}h ${minutes}m`;
        return `${minutes}m`;
    }

    startRevealCountdown() {
        setInterval(() => {
            this.updateRevealInfo();
        }, 60000); // Update every minute
    }

    initializePolls() {
        const polls = document.querySelectorAll('.anonymous-poll');
        polls.forEach(poll => {
            this.setupPoll(poll);
        });
    }

    setupPoll(poll) {
        const options = poll.querySelectorAll('.anonymous-poll-option');
        const submitBtn = poll.querySelector('.anonymous-poll-submit');
        const isMultipleChoice = poll.dataset.multipleChoice === 'true';

        options.forEach(option => {
            const input = option.querySelector('input');
            if (input) {
                input.addEventListener('change', () => {
                    this.updatePollSelection(poll, option, isMultipleChoice);
                });
            }
        });

        if (submitBtn) {
            submitBtn.addEventListener('click', (e) => {
                this.submitPollVote(e, poll);
            });
        }
    }

    handlePollOptionClick(e) {
        const option = e.target.closest('.anonymous-poll-option');
        const poll = option.closest('.anonymous-poll');
        const isMultipleChoice = poll.dataset.multipleChoice === 'true';
        
        this.updatePollSelection(poll, option, isMultipleChoice);
    }

    updatePollSelection(poll, option, isMultipleChoice) {
        const input = option.querySelector('input');
        if (!input) return;

        if (isMultipleChoice) {
            option.classList.toggle('selected', input.checked);
        } else {
            // Single choice - unselect others
            const allOptions = poll.querySelectorAll('.anonymous-poll-option');
            allOptions.forEach(opt => {
                opt.classList.remove('selected');
                const optInput = opt.querySelector('input');
                if (optInput && optInput !== input) {
                    optInput.checked = false;
                }
            });
            option.classList.toggle('selected', input.checked);
        }

        this.updatePollSubmitButton(poll);
    }

    updatePollSubmitButton(poll) {
        const submitBtn = poll.querySelector('.anonymous-poll-submit');
        if (!submitBtn) return;

        const selectedOptions = poll.querySelectorAll('.anonymous-poll-option.selected');
        const isMultipleChoice = poll.dataset.multipleChoice === 'true';
        
        let canSubmit = false;
        if (isMultipleChoice) {
            canSubmit = selectedOptions.length > 0;
        } else {
            canSubmit = selectedOptions.length === 1;
        }

        submitBtn.disabled = !canSubmit;
    }

    async submitPollVote(e, poll = null) {
        if (!poll) {
            poll = e.target.closest('.anonymous-poll');
        }

        const selectedOptions = poll.querySelectorAll('.anonymous-poll-option.selected');
        const pollId = poll.dataset.pollId;
        
        if (!pollId || selectedOptions.length === 0) return;

        const selectedValues = Array.from(selectedOptions).map(option => {
            const input = option.querySelector('input');
            return input.value;
        });

        try {
            const response = await fetch(`/api/polls/${pollId}/vote`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    selected_options: selectedValues
                })
            });

            if (response.ok) {
                this.showPollResults(poll);
                this.disablePollVoting(poll);
            } else {
                throw new Error('Failed to submit vote');
            }
        } catch (error) {
            console.error('Error submitting poll vote:', error);
            alert('Failed to submit vote. Please try again.');
        }
    }

    showPollResults(poll) {
        const results = poll.querySelector('.anonymous-poll-results');
        if (!results) return;

        // This would typically fetch real results from the server
        // For now, we'll show a placeholder
        results.innerHTML = `
            <h4>Poll Results</h4>
            <p>Thank you for voting! Results will be displayed here.</p>
        `;
        results.style.display = 'block';
    }

    disablePollVoting(poll) {
        const options = poll.querySelectorAll('.anonymous-poll-option');
        const submitBtn = poll.querySelector('.anonymous-poll-submit');

        options.forEach(option => {
            const input = option.querySelector('input');
            if (input) input.disabled = true;
            option.style.cursor = 'not-allowed';
        });

        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Vote Submitted';
        }
    }

    saveAnonymousSettings() {
        localStorage.setItem('anonymousMode', JSON.stringify({
            isAnonymousMode: this.isAnonymousMode,
            settings: this.anonymousSettings
        }));
    }

    loadAnonymousSettings() {
        const saved = localStorage.getItem('anonymousMode');
        if (saved) {
            try {
                const data = JSON.parse(saved);
                this.isAnonymousMode = data.isAnonymousMode || false;
                this.anonymousSettings = data.settings || this.anonymousSettings;
                
                // Update UI
                const toggle = document.querySelector('.anonymous-toggle');
                if (toggle) {
                    toggle.classList.toggle('active', this.isAnonymousMode);
                }
                
                this.updateFormVisibility();
                this.updateRevealInfo();
            } catch (error) {
                console.error('Error loading anonymous settings:', error);
            }
        }
    }

    // Utility method to check if user is moderator
    isModerator() {
        // This would typically check the user's role from the server
        return document.body.dataset.userRole === 'moderator' || 
               document.body.dataset.userRole === 'admin';
    }

    // Method to reveal anonymous author (moderator only)
    revealAnonymousAuthor(postId) {
        if (!this.isModerator()) {
            alert('Only moderators can reveal anonymous authors.');
            return;
        }

        // This would make an API call to reveal the author
        console.log(`Revealing author for post ${postId}`);
    }
}

// Initialize anonymous mode when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AnonymousMode();
});

// Export for use in other scripts
window.AnonymousMode = AnonymousMode;
