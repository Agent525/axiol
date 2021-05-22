import os
from pymongo import MongoClient

#Config
TOKEN = os.environ.get("TOKEN")
DEFAULT_PREFIX = "."

#Mongo Client
MONGOCLIENT = MongoClient(os.environ.get("MONGO_URL"))
#Databases
DATABASE = MONGOCLIENT["Axiol"]
LEVELDATABASE = MONGOCLIENT["Leveling"]
#Collections
PREFIXES = DATABASE["Prefixes"]
REACTIONROLES = DATABASE["Reaction Roles"]
VERIFY = DATABASE["Verify"]

#Colours
CMAIN = 0xFF006A #Everything
CRED = 0xFF0000 #Error or alert
CGREEN = 0x15ff00 #Success
CORANGE = 0xFF4400 #Inform or warning
CBLUE = 0x00AEFF #Data
CTEAL = 0x00EEFF #Data

#Emojis
LOGO = "<:Logo:845663121477206036>"
ACCEPT = "<:Accept:845661274930675762>"
DECLINE = "<:Decline:845661271830822943>"
ENABLE = "<:Enable:845661277317103646>"
DISABLE = "<:Disable:845661276105080852>"
SETTINGS = "<:Settings:845661273110872116>"