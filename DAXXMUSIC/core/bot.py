from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus

import config

from ..logging import LOGGER


class DAXX(Client):
    def init(self):
        LOGGER(name).info(f"Starting Bot...")
        super().init(
            name="DAXXMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(name).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )

        except Exception as ex:
            LOGGER(name).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).name}."
            )

        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(name).error(
                "Please promote your bot as an admin in your log group/channel."
            )

        LOGGER(name).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()
