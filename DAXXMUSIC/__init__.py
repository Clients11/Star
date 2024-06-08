from DAXXMUSIC.core.bot import DAXX
from DAXXMUSIC.core.dir import dirr
from DAXXMUSIC.core.git import git
from DAXXMUSIC.core.userbot import Userbot
from DAXXMUSIC.misc import dbb, heroku
from pyrogram import Client
from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = DAXX()
api = SafoneAPI()
userbot = Userbot()
user = Client(
    "daxx",
    api_id=16874790,
    api_hash="46aa49adca0f1d184eb2a2f4a48a1df9"
)

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
