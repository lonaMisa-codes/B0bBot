# B0bBot - Spawner Ticket Bot

Fully customizable Discord bot with:

- Spawner Sell/Buy ticket panel (with modals + auto calculation)
- Normal ticket system
- Calculator
- Moderation commands
- Reaction Roles
- Everything configurable by admins

---

## Features

- Spawner Panel → Sell & Buy buttons with forms
- Ticket System → Private tickets + close/add/remove
- Calculator → /calc
- Moderation → ban, kick, timeout, purge, lock, unlock
- Reaction Roles → React to get roles (fully command controlled)
- Fully customizable (roles, prices, messages, channels, etc.)

---

## Setup

1. Clone the repo
2. Install requirements: pip install -r requirements.txt
3. Create a .env file and put your bot token:
   DISCORD_TOKEN=your_bot_token_here
4. Invite the bot with Administrator + applications.commands scope
5. Run the bot: python bot.py
6. Use /setup and configure everything
7. Run /spawnerpanel to post the Sell/Buy panel

---

## Admin Commands

- /setup → Shows setup guide
- /setcategory → Set ticket category
- /setrole → Set Seller / Buy Price / Admin roles
- /setlogchannel → Set log channel
- /setbuyprice → Set buy price for a spawner type
- /config → View current config
- /spawnerpanel → Post the Sell/Buy panel
- /rr_add → Add reaction role to a message
- /rr_remove → Remove a reaction role

---

## Reaction Roles

1. Post any message (or use an existing one)
2. Copy the Message ID
3. Run: /rr_add message_id:123456789 emoji:📢 role:@Announcements
4. Users react → get the role
5. Users remove reaction → lose the role

---

## Notes

- All settings are saved in config.json
- Token is loaded from .env (never put token in config.json)
- Make sure the bot has permission to manage roles and manage channels
