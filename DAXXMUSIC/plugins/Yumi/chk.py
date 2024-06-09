import os
import re
import emoji
from pyrogram import Client, filters
from pyrogram.types import Message
from DAXXMUSIC import app



# Define the credit card validation function
def daxx(card_number):
    card_number = re.sub(r'\D', '', card_number)
    if not card_number.isdigit():
        return emoji.emojize(":x:")

    digits = list(map(int, card_number))
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]

    total = sum(odd_digits)
    for digit in even_digits:
        total += sum(divmod(digit * 2, 10))

    return emoji.emojize("""
     Result  ➠ 𝗔𝗽𝗽𝗿𝗼𝘃𝗲𝗱 ✅ 
     Response: Approved $15 ✅ 
     Seller Message:Payment complete.
     ⊗ Status  ➠ Live 🟢
     ⊗ GATEWAY- STRIPE AUTH  ♻️""") if total % 10 == 0 else emoji.emojize("""
     Result  ➠   DECLINED ❌
     Response: card_declined ❌
     Seller Message: Payment incomplete.
     ⊗ Status  ➠ Dead 🚫
     ⊗ GATEWAY- STRIPE AUTH  ♻️""")

def get_credit_card_info(card_number):
    card_length = len(card_number)

    mii = card_number[0]

    mii_categories = {
        '0': "ISO/TC 68 and other future industry assignments",
        '1': "Airlines",
        '2': "Airlines and other future industry assignments",
        '3': "Travel and Entertainment",
        '4': "Banking and Financial",
        '5': "Banking and Financial",
        '6': "Merchandising and Banking/Financial",
        '7': "Petroleum and other future industry assignments",
        '8': "Healthcare, Telecommunications, and other future industry assignments",
        '9': "National Assignment",
    }

    # Get Bank Name and Bank Country
    bank_info = {
        '377750': ('Banco Internacional del Perú (Interbank)', 'Country'),
        '377753': ('Banco Internacional del Perú (Interbank)', 'Country'),
        '370244': ('Venezuela.', 'Country'),
        '404586': ('Visa Platinum Transaero Card', 'Country'),
        '411016': ('Venezuela.', 'Country'),
        '411298': ('Visa Credit Card', 'Country'),
        '411773': ('Preferred Customer)', 'Country'),
        '411911': ('Live Fresh Platinum Visa Credit Card', 'Country'),
        '411986': ('Visa Credit Card', 'Country'),
        '412984-85': ('Visa Debit Card', 'Country'),
        '414049': ('Visa Electron', 'Country'),
        '414051': ('Visa Orange Debit Card', 'Country'),
        '4143**': ('Visa Card', 'Country'),
        '4146**': ('Salute Visa Card', 'Country'),
        '414716': ('Alaska Airlines Signature Visa Credit Card', 'Country'),
        '414720': ('Chase Sapphire or Holiday Inn Priority Club Rewards Visa Credit Card', 'Country'),
        '414746 3': ('PremierMiles Visa Signature Credit Card', 'Country'),
        '414746 4': ('Dividend Visa Signature Credit Card', 'Country'),
        '414983': ('Visa Check Card', 'Country'),
        '415055': ('Visa Cleo', 'Country'),
        '415461': ('Visa Debit', 'Country'),
        '415929': ('Visa Credit Card', 'Country'),
        '415981': ('Visa Debit Card', 'Country'),
        '416039': ('Visa Electron', 'Country'),
        '416451': ('Visa Electron', 'Country'),
        '416896': ('Visa Electron', 'Country'),
        '417008-11': ('Business Visa Card', 'Country'),
        '4172**': ('Visa Gold Card', 'Country'),
        '418224': ('Visa Loaded Card', 'Country'),
        '418236': ('KEB VISA Signature Card', 'Country'),
        '418238': ('Visa Platinum Debit Card', 'Country'),
        '4185**': ('Visa Card', 'Country'),
        '4188500**': ('Visa Card', 'Country'),
        '419661': ('Visa credit Card', 'Country'),
        '4241**': ('Bank of nova scotia Perú -Scotiabank', 'Country'),
        '421355': ('Banco Internacional del Peru Debit Card (Peru)', 'Country'),
        '421494': ('Visa Debit Card', 'Country'),
        '421689': ('VISA Debit (Electronic)', 'Country'),
        '422189': ('Visa credit card', 'Country'),
        '433445': ('Visa Electron', 'Country'),
        '433507': ('Visa', 'Country'),
        '4377': ('Indonesia, Visa, Platinum Card', 'Country'),
        '4391': ('Platinum (Thailand)', 'Country'),
        '440210': ('Visa Silver', 'Country'),
        '440211': ('Visa Gold', 'Country'),
        '440752': ('Visa Classic', 'Country'),
        '440753': ('Visa Electron', 'Country'),
        '445093': ('VISA Credit Card', 'Country'),
        '445094': ('VISA Credit Card', 'Country'),
        '4458': ('Plus (interbank network) Cash Card for use with savings accounts', 'Country'),
        '446155': ('mBank Visa Electron', 'Country'),
        '446157': ('mBank Visa Electron', 'Country'),
        '446157': ('mBank Visa Classic Debit Card', 'Country'),
        '446158': ('mBank Visa Electron', 'Country'),
        '446153': ('mBank Visa Gold Credit Card', 'Country'),
        '446261': ('Visa Debit Card (for Personal and Business Accounts)', 'Country'),
        '446268': ('Visa Debit', 'Country'),
        '446272': ('Platinum Account Visa Debit Card', 'Country'),
        '446274': ('Premier Visa Debit Card (with £250 Cheque guarantee limit)', 'Country'),
        '446277': ('Business Banking Visa Debit Card', 'Country'),
        '446278': ('Visa debit card', 'Country'),
        '446279': ('Visa debit card', 'Country'),
        '446291': ('Visa Gold debit card', 'Country'),
        '4465**': ('Visa Credit Card', 'Country'),
        '4470**': ('Visa debit Card', 'Country'),
        '447817': ('Visa Gold Transaero Card', 'Country'),
        '448336': ('Visa credit card', 'Country'),
        '448445': ('Visa Credit Card', 'Country'),
        '4488': ('Visa Credit Card', 'Country'),
        '449533': ('Classic, Debit, Visa', 'Country'),
        '443438': ('Visa Debit Card', 'Country'),
        '448336': ('mBank Visa Classic', 'Country'),
        '4508': ('Popular Bank (NY) a Branch of Banco Popular Dominicano', 'Country'),
        '4510': ('Visa', 'Country'),
        '4512': ('Visa', 'Country'),
        '451291': ('Visa Credit Card', 'Country'),
        '451503': ('VISA', 'Country'),
        '4516': ('VISA', 'Country'),
        '4519': ('Client Card (ATM/INTERAC)', 'Country'),
        '4535': ('Visa Card', 'Country'),
        '4536': ('Interac Debit Card', 'Country'),
        '4537': ('Visa Card', 'Country'),
        '4538': ('Visa Card', 'Country'),
        '453801': ('Visa Gold', 'Country'),
        '453826': ('Visa Infinite', 'Country'),
        '453904': ('Visa Electron', 'Country'),
        '453978': ('Connect Visa Debit Card', 'Country'),
        '453979': ('Connect Visa Debit Card', 'Country'),
        '453997': ('Visa Card', 'Country'),
        '453998': ('Visa Card', 'Country'),
        '4542': ('Japan', 'Country'),
        '454312': ('Visa Credit Card', 'Country'),
        '454313': ('Visa Debit Card', 'Country'),
        '454434': ('Visa Debit Card', 'Country'),
        '454495': ('Visa Credit Card', 'Country'),
        '4544': ('Visa', 'Country'),
        '4545': ('Venezuela.', 'Country'),
        '454749': ('Visa Charge Card', 'Country'),
        '4549': ('Visa credit and debit cards', 'Country'),
        '455025': ('Visa', 'Country'),
        '455701': ('GOLD VISA Credit Card', 'Country'),
        '455702': ('Credit Card', 'Country'),
        '4563': ('Visa Credit Card', 'Country'),
        '456403': ('Visa Debit Card', 'Country'),
        '456406': ('Visa Debit Card', 'Country'),
        '456443': ('BASIC BLACK VISA CREDIT CARD (Australia)', 'Country'),
        '456445': ('VISA DEBIT CARD (now Commonwealth Bank Australia)', 'Country'),
        '456738': ('Visa Debit Card (UK)', 'Country'),
        '4568': ('Visa Debit Card', 'Country'),
        '4580XX': ('Visa Card (Leumi Bank)', 'Country'),
        '4580XX': ('Visa Card (Discount Bank and other partners)', 'Country'),
        '458440': ('VISA Debit Card', 'Country'),
        '4773': ('platinum (Thailand)', 'Country'),
        '477548': ('Visa debit (Estonia)', 'Country'),
        '477596': ('Visa Debit Card', 'Country'),
        '4779': ('Visa Debit Card', 'Country'),
        '477915': ('Visa Debit Card', 'Country'),
        '478200': ('VISA CLASSIC -DEBIT', 'Country'),
        '480152': ('MyECount.com Verizon Wireless rebate debit card', 'Country'),
        '4809': ('Visa Platinum Check Card', 'Country'),
        '4828': ('Visa Debit Card', 'Country'),
        '482870': ('Visa Debit Card', 'Country'),
        '483542': ('Visa Debit Card', 'Country'),
        '483561': ('Visa Debit Card', 'Country'),
        '483583': ('Dual Currency (JPY/USD) Credit Card', 'Country'),
        '484427': ('Top-up card (managed by RBS)', 'Country'),
        '484432': ('Visa Electron Card', 'Country'),
        '4854': ('Visa Debit Card', 'Country'),
        '486236': ('Visa Platinum Credit Card', 'Country'),
        '486430': ('Visa Card', 'Country'),
        '486483': ('Commercial Visa credit Card', 'Country'),
        '4867': ('Visa Card', 'Country'),
        '4868': ('Bank N.A. Check Card', 'Country'),
        '486990': ('Visa Business Check Card', 'Country'),
        '486993': ('Visa Business Check Card', 'Country'),
        '4888**': ('Visa Credit Card', 'Country'),
        '4890': ('Visa Virtual, Visa Card (Virtual Visa Prepaid) and Visa Plastic (Visa Prepaid)', 'Country'),
        '4931': ('American Airlines (Dominican Republic)', 'Country'),
        '525241': ('United Airlines Mileage Plus', 'Country'),
        '526418 Vietcombank': ('MasterCard Debit Card', 'Country'),
        '526781': ('MasterCard unembossed Credit card (Slovakia)', 'Country'),
        '526790': ('MasterCard Debit Card', 'Country'),
        '531207': ('Aeroflot bonus', 'Country'),
        '585048': ('ATM Card', 'Country'),
        '589732': ('DTV2009.GOV', 'Country'),
        '601021': ('Ontario government', 'Country'),
        '6051': ('USA & Canada', 'Country'),
        '606095': ('Europe', 'Country'),
        '606263': ('Brazil', 'Country'),
        '606484': ('Karum Group LLC', 'Country'),
        '606934': ('Korea', 'Country'),
        '607120': ('Korea', 'Country'),
        '621041': ('Debit (HK)', 'Country'),
        '622409': ('Debit (HK)', 'Country'),
        '622410': ('Debit (HK)', 'Country'),
        '622492': ('Debit (HK)', 'Country'),
        '625040': ('HKD Account (HK)', 'Country'),
        '625041': ('CNY Account (HK)', 'Country'),
        '625042': ('HKD Account (HK)', 'Country'),
        '625043': ('CNY Account (HK)', 'Country'),
        '63191': ('Bhs credit card', 'Country'),
        '6759xx': ('Maestro (formerly Switch) debit cards', 'Country'),
        '676165': ('CSOB Bank (CZ)', 'Country'),
        '676280': ('Sberbank (RU)', 'Country'),
        '676378': ('Maestro PayPass', 'Country'),
        '676398': ('Maestro PayPass', 'Country'),
        '676481': ('Maestro debit card', 'Country'),
        '676509': ('Maestro debit card', 'Country'),
        '676613': ('Maestro debit card', 'Country'),
        '6767xx': ('Solo; xx indicates the bank in the UK national sort code system.', 'Country'),
        '676953': ('Maestro debit card', 'Country'),
        '676969': ('Maestro debit card', 'Country'),
        '6771': ('Laser debit card', 'Country'),
        '677518': ('Moscow Metro Express Card/Maestro debit card', 'Country'),
        '677574': ('Maestro debit card', 'Country'),
        '677594': ('Maestro debit card', 'Country'),
    }

    bin_iin = card_number[:6]
    if bin_iin in bank_info:
        bank_name, bank_country = bank_info[bin_iin]
    else:
        bank_name, bank_country = "----", "----"

    pan = card_number[6:-1]
    network_brand = "Unknown Network/Brand"

    network_patterns = {
        '4': "Visa",
        '5': "Mastercard",
        '6': "Discover",
    }

    if card_number[0] in network_patterns:
        network_brand = network_patterns[card_number[0]]

    return {
        "𝗚𝗔𝗧𝗘𝗪𝗔𝗬- 𝗦𝗧𝗥𝗜𝗣𝗘 𝗔𝗨𝗧𝗛 $𝟭𝟱♻️": daxx(card_number),
        "𝗠𝗜𝗜": mii + " - " + mii_categories.get(mii, "Unknown Category"),
        "𝗕𝗔𝗡𝗞 𝗡𝗔𝗠𝗘": bank_name,
        "𝗕𝗔𝗡𝗞 𝗖𝗢𝗨𝗡𝗧𝗥𝗬": bank_country,
        "𝗕𝗜𝗡": bin_iin,
        "𝗣𝗔𝗡": pan,
        "𝗕𝗥𝗔𝗡𝗗": network_brand,
    }

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
        result = "\n".join([f"{key}: {value}" for key, value in info.items()])
        results.append(result)

    results_text = "\n\n".join(results)
    results_file = "credit_card_results.txt"
    with open(results_file, "w") as f:
        f.write(results_text)

    await message.reply_document(results_file)
    os.remove(results_file)
