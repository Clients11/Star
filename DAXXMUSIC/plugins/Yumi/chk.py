import re
import emoji
from pyrogram import Client, filters
from pyrogram.types import Message
from DAXXMUSIC import app



# Define the credit card validation function
def daxx(card_number):
    card_number = re.sub(r'\D', '', card_number)
    if not card_number.isdigit():
        return "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"

    digits = list(map(int, card_number))
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    total = sum(odd_digits)
    for digit in even_digits:
        total += sum(divmod(digit * 2, 10))

    return "𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅" if total % 10 == 0 else "𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌"

def get_credit_card_info(card_number):
    card_number = card_number.replace(' ', '')
    result = daxx(card_number)
    gateway = "Braintree Auth"

    return f"""
𝗖𝗮𝗿𝗱: {card_number}
𝐆𝐚𝐭𝐞𝐰𝐚𝐲: {gateway}
𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {result}
"""

# Create the bot instance
#app = Client("credit_card_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Handler for the .chk command
@app.on_message(filters.command("chk"))
async def check_credit_cards(client: Client, message: Message):
    card_numbers = message.text.split()[1:]  # Extract card numbers from the message
    if len(card_numbers) > 10:
        await message.reply("You can only check up to 10 card numbers at a time.")
        return

    results = []
    for card_number in card_numbers:
        info = get_credit_card_info(card_number)
        results.append(info)

    results_text = "\n".join(results)
    await message.reply(results_text)
