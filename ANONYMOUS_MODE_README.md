# 👻 Anonymous Mode Feature

A comprehensive anonymous posting system for MMU-BUZZ that allows users to speak freely while maintaining community safety and moderation capabilities.

## ✨ Features

### 🎭 Core Anonymous Features

1. **Anonymous Posts**
   - Post without revealing your identity
   - Author shown as "Anonymous User"
   - Ghost icon and special styling
   - Full moderation capabilities maintained

2. **Secret Posts**
   - Only visible to community moderators
   - Perfect for sensitive feedback
   - Lock icon and special styling
   - Requires moderator approval for public viewing

3. **Anonymous Polls**
   - "What do you really think?" polls
   - Multiple choice or single choice options
   - Anonymous voting
   - Real-time results display

4. **Time-Delayed Reveals**
   - Author revealed after a set date/time
   - Countdown timer display
   - Automatic reveal when conditions are met

5. **Vote-Based Reveals**
   - Author revealed when post reaches vote threshold
   - Community-driven reveal system
   - Transparent voting process

### 👮 Moderator Features

1. **Anonymous Management Dashboard**
   - View all anonymous and secret posts
   - Reveal anonymous authors when needed
   - Approve time-delayed reveals
   - Monitor anonymous activity statistics

2. **Special Permissions**
   - See all secret posts
   - Reveal anonymous authors
   - Access to anonymous post analytics
   - Override reveal conditions

## 🚀 Usage

### For Regular Users

1. **Creating Anonymous Posts:**
   - Go to "Create Post"
   - Click the "Post Anonymously" toggle
   - Configure anonymous settings
   - Write and submit your post

2. **Anonymous Settings:**
   - **Secret Post:** Only visible to moderators
   - **Reveal Type:** Choose how/when to reveal identity
   - **Time-Delayed:** Set a specific date/time
   - **Vote Threshold:** Set minimum votes required
   - **Moderator Approval:** Requires manual approval

3. **Creating Anonymous Polls:**
   - Enable anonymous mode
   - Add poll question and options
   - Choose single or multiple choice
   - Set expiration date (optional)

### For Moderators

1. **Access Management Dashboard:**
   - Navigate to "👻 ANONYMOUS" in the menu
   - View all anonymous and secret posts
   - Manage reveal conditions

2. **Reveal Anonymous Authors:**
   - Click "Reveal" button on any anonymous post
   - Confirm the action
   - Author identity becomes visible

3. **Approve Reveals:**
   - Review pending reveals
   - Approve time-delayed reveals
   - Monitor reveal conditions

## 🎨 UI Components

### Anonymous Toggle
```html
<button class="anonymous-toggle">
    <span class="toggle-icon">👤</span>
    <span class="toggle-text">Post Anonymously</span>
</button>
```

### Anonymous Post Display
```html
<div class="cm-card anonymous-post">
    <span class="anonymous-badge">
        <i class="bi bi-ghost icon"></i>
        Anonymous
    </span>
    <span class="anonymous-author">Anonymous User</span>
</div>
```

### Anonymous Poll
```html
<div class="anonymous-poll">
    <div class="anonymous-poll-question">Question here</div>
    <div class="anonymous-poll-options">
        <!-- Poll options -->
    </div>
    <button class="anonymous-poll-submit">Vote</button>
</div>
```

## 🗄️ Database Schema

### New Tables

1. **anonymous_polls**
   - `id` (Primary Key)
   - `post_id` (Foreign Key to Posts)
   - `question` (Poll question)
   - `options` (JSON array of options)
   - `is_multiple_choice` (Boolean)
   - `expires_at` (Optional expiration)

2. **anonymous_poll_votes**
   - `id` (Primary Key)
   - `poll_id` (Foreign Key to anonymous_polls)
   - `user_id` (Optional, for tracking)
   - `selected_options` (JSON array)
   - `ip_hash` (For anonymous tracking)

3. **anonymous_reveals**
   - `id` (Primary Key)
   - `post_id` (Foreign Key to Posts)
   - `reveal_type` (time_delayed, community_vote, moderator_approved)
   - `scheduled_reveal_date` (For time-delayed)
   - `reveal_condition` (JSON for conditions)
   - `is_revealed` (Boolean)
   - `revealed_at` (Timestamp)

### Updated Tables

1. **Posts Table**
   - `is_anonymous` (Boolean)
   - `anonymous_author_id` (Foreign Key to User)
   - `reveal_date` (DateTime)
   - `is_secret` (Boolean)

2. **Posts_comment Table**
   - `is_anonymous` (Boolean)
   - `anonymous_author_id` (Foreign Key to User)

## 🔧 Technical Implementation

### Models
- `Posts` - Updated with anonymous fields
- `PostComment` - Updated with anonymous fields
- `AnonymousPoll` - New model for polls
- `AnonymousPollVote` - New model for poll votes
- `AnonymousReveal` - New model for reveal conditions

### Utility Functions
- `can_see_secret_posts()` - Check moderator permissions
- `get_author_display_name()` - Get appropriate author name
- `should_reveal_author()` - Check reveal conditions
- `filter_posts_for_user()` - Filter posts by permissions
- `check_reveal_conditions()` - Process reveal logic

### JavaScript Classes
- `AnonymousMode` - Main anonymous functionality
- Poll management and voting
- Settings persistence
- UI interactions

## 🎯 Use Cases

### ✅ Appropriate Uses
- Honest feedback on sensitive topics
- Reporting issues without fear of retaliation
- Asking embarrassing or personal questions
- Sharing personal struggles or experiences
- Voting on controversial topics anonymously
- Providing constructive criticism

### ❌ Inappropriate Uses
- Harassment or bullying
- Spreading misinformation
- Hate speech or discrimination
- Spam or off-topic content
- Violating community guidelines
- Trolling or disruptive behavior

## 🛡️ Safety & Moderation

### Content Moderation
- Anonymous posts are still subject to community guidelines
- Moderators can see all anonymous content
- Reporting system works for anonymous posts
- Inappropriate content can be removed

### Privacy Protection
- Author identity is protected by default
- Only moderators can reveal identities
- All reveal actions are logged
- IP addresses are hashed for poll tracking

### Reveal Conditions
1. **Time-Delayed:** Automatic reveal after set date
2. **Vote Threshold:** Reveal when post reaches vote count
3. **Moderator Approval:** Manual reveal by moderators
4. **Emergency Override:** Moderators can reveal anytime

## 📊 Analytics & Statistics

### Available Metrics
- Total anonymous posts
- Secret posts count
- Revealed authors count
- Pending reveals count
- Poll participation rates
- Anonymous post engagement

### Moderator Dashboard
- Real-time statistics
- Post management interface
- Reveal approval workflow
- Activity monitoring

## 🚀 Getting Started

### For Users
1. Visit `/anonymous-demo` to see the feature in action
2. Create a post and enable anonymous mode
3. Configure your reveal preferences
4. Submit your anonymous post

### For Moderators
1. Visit `/anonymous-moderator` to access management tools
2. Review anonymous and secret posts
3. Manage reveal conditions
4. Monitor anonymous activity

## 🔄 Future Enhancements

### Planned Features
- Anonymous comment system
- Anonymous messaging between users
- Advanced poll types (ranked choice, etc.)
- Anonymous post categories
- Enhanced analytics dashboard
- Mobile app integration

### Potential Improvements
- Machine learning for content moderation
- Advanced reveal conditions
- Anonymous post recommendations
- Integration with external moderation tools
- Enhanced privacy controls

## 📝 Configuration

### Environment Variables
- `ANONYMOUS_MODE_ENABLED` - Enable/disable feature
- `ANONYMOUS_POLL_MAX_OPTIONS` - Maximum poll options
- `ANONYMOUS_REVEAL_DEFAULT_DAYS` - Default reveal delay

### Database Migration
Run the migration to add anonymous mode tables:
```bash
flask db upgrade
```

## 🤝 Contributing

### Development Setup
1. Clone the repository
2. Install dependencies
3. Run database migrations
4. Start the development server
5. Visit `/anonymous-demo` to test

### Testing
- Test anonymous post creation
- Test poll functionality
- Test reveal conditions
- Test moderator features
- Test edge cases and error handling

---

**🎉 Enjoy the enhanced anonymous posting experience!**

*Remember: Anonymous mode is a tool for honest communication, not for harmful behavior. Please use it responsibly and in accordance with community guidelines.*
