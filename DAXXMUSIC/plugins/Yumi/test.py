import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from DAXXMUSIC import app

approved_cards = []
declined_cards = []

@app.on_message(filters.command("chk"))
async def check_cards(client, message):
    global approved_cards, declined_cards
    approved_cards = []
    declined_cards = []

    cards = message.text.split()[1:]  # Get card numbers from the message
    if len(cards) > 3:
        await message.reply("You can only check up to 3 cards at a time.")
        return

    for i, card in enumerate(cards):
        parts = card.strip().split('|')
        if len(parts) == 4:
            card_number, exp_month, exp_year, cvc = parts
            is_approved = random.random() > 0.5  # 50% chance of approval
            response_type = random.choice([
                "Approved\nPayment Completed", 
                "Approved\nInsufficient Funds", 
                "CVV LIVE", 
                "Your card's security code is invalid."
            ])
            result = (
                f"𝗖𝗮𝗿𝗱: {card_number}|{exp_month}|{exp_year}|{cvc}\n"
                f"𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth\n"
                f"𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {response_type}"
            )
            if "Approved" in response_type:
                approved_cards.append(f"𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅\n{result}")
            else:
                declined_cards.append(f"𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌\n{result}")
            await message.reply(f"Checking card {i+1}/{len(cards)}\n{result}")
            await asyncio.sleep(random.uniform(2, 4))  # Simulate realistic processing time
        else:
            await message.reply(f"Invalid format: {card}")

    approved_count = len(approved_cards)
    declined_count = len(declined_cards)

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"View Approved Cards ({approved_count})", callback_data="view_approved")],
            [InlineKeyboardButton(f"View Declined Cards ({declined_count})", callback_data="view_declined")]
        ]
    )

    await message.reply(
        f"Processing Complete!\nTotal Cards: {len(cards)}\nApproved: {approved_count}\nDeclined: {declined_count}",
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("view_approved"))
async def view_approved(client, callback_query):
    global approved_cards
    if approved_cards:
        approved_text = "\n\n".join(approved_cards)
        approved_cards = []  # Clear approved cards after displaying
        await callback_query.message.reply(f"Approved Cards:\n{approved_text}")
    else:
        await callback_query.message.reply("No approved cards.")
    await update_buttons(callback_query)

@app.on_callback_query(filters.regex("view_declined"))
async def view_declined(client, callback_query):
    global declined_cards
    if declined_cards:
        declined_text = "\n\n".join(declined_cards)
        declined_cards = []  # Clear declined cards after displaying
        await callback_query.message.reply(f"Declined Cards:\n{declined_text}")
    else:
        await callback_query.message.reply("No declined cards.")
    await update_buttons(callback_query)

async def update_buttons(callback_query):
    global approved_cards, declined_cards
    approved_count = len(approved_cards)
    declined_count = len(declined_cards)
    
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"View Approved Cards ({approved_count})", callback_data="view_approved")],
            [InlineKeyboardButton(f"View Declined Cards ({declined_count})", callback_data="view_declined")]
        ]
    )
    
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()
