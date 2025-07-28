import telebot
from telebot import types
import re
import os

# Initialize bot with token from environment variable (for Render.com)
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))

# Temporary user data storage (replace with database in production)
user_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Create inline keyboard with task buttons
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    btn_telegram = types.InlineKeyboardButton(
        "✅ Join Telegram Group", 
        url="https://t.me/+XjGAPZD62hxhZDNh"
    )
    btn_twitter = types.InlineKeyboardButton(
        "✅ Follow Twitter", 
        url="https://x.com/RealGoobaCoin"
    )
    btn_tiktok = types.InlineKeyboardButton(
        "✅ Follow TikTok", 
        url="https://www.tiktok.com/@realgoobacoin"
    )
    btn_verify = types.InlineKeyboardButton(
        "🔍 Verify All Tasks", 
        callback_data="verify_tasks"
    )
    
    markup.add(btn_telegram, btn_twitter, btn_tiktok, btn_verify)
    
    welcome_message = """
    🚀 Welcome to GoobaCoin Airdrop Bot!

To qualify for the airdrop, please complete these tasks:
1. Join our Telegram group
2. Follow our Twitter (@RealGoobaCoin)
3. Follow our TikTok (@realgoobacoin)

After completing all tasks, click "Verify All Tasks" below.
    """
    
    bot.send_message(
        message.chat.id, 
        welcome_message, 
        reply_markup=markup,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data == "verify_tasks")
def verify_tasks(call):
    # Store user ID in temporary data
    user_data[call.from_user.id] = {'step': 'twitter'}
    
    # Ask for Twitter username
    msg = bot.send_message(
        call.message.chat.id,
        "✏️ Please enter your *Twitter username* (without @):\n\n"
        "Example: `RealGoobaCoin`",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_twitter_username)

def process_twitter_username(message):
    # Basic Twitter username validation
    if not re.match(r'^[A-Za-z0-9_]{1,15}$', message.text):
        msg = bot.send_message(
            message.chat.id,
            "❌ Invalid Twitter username format. Please enter just your username (no @, spaces, or special characters).\n"
            "Example: `RealGoobaCoin`",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, process_twitter_username)
        return
    
    # Store Twitter username
    if message.from_user.id not in user_data:
        user_data[message.from_user.id] = {}
    user_data[message.from_user.id]['twitter'] = message.text
    user_data[message.from_user.id]['step'] = 'wallet'
    
    # Ask for SOL wallet address
    msg = bot.send_message(
        message.chat.id,
        "💰 Please enter your *SOLANA wallet address*:\n\n"
        "Example: `7vH5DZBj6N2X6L3q2J7W9x8Y2Z1R4T5Y6U7I8O9P0Q1W2E3R4T`",
        parse_mode='Markdown'
    )
    bot.register_next_step_handler(msg, process_wallet_address)

def process_wallet_address(message):
    # Basic SOL address validation
    if not re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', message.text):
        msg = bot.send_message(
            message.chat.id,
            "❌ Invalid SOLANA address. Please check and try again.\n"
            "Example: `7vH5DZBj6N2X6L3q2J7W9x8Y2Z1R4T5Y6U7I8O9P0Q1W2E3R4T`",
            parse_mode='Markdown'
        )
        bot.register_next_step_handler(msg, process_wallet_address)
        return
    
    # Store wallet address
    user_data[message.from_user.id]['wallet'] = message.text
    
    # Final success message
    success_message = """
    🎉 *Weldone! Hope you didn't cheat the system.*

✅ 5 SOL has been scheduled to your wallet: `{}`

⏳ *Please note:* It may take some time to process. 
Only the top 10 will be rewarded once the project hits it's expected heights and moons!

Thank you for participating in our airdrop!
    """.format(user_data[message.from_user.id]['wallet'])
    
    bot.send_message(
        message.chat.id,
        success_message,
        parse_mode='Markdown'
    )
    
    # Here you would save to database and process verification
    print(f"User {message.from_user.id} completed registration:")
    print(user_data[message.from_user.id])

# For Render.com deployment
if __name__ == '__main__':
    bot.polling()
