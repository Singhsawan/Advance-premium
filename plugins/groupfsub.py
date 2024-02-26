from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.users_chats_db import db
from utils import save_group_settings, get_settings
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from pyrogram import enums
from info import ADMINS

@Client.on_message(filters.group & filters.command("set_fsub"))
async def f_sub_cmd(bot, message):
    m = await message.reply("<b>Please Wait...</b>")

    chat_type = message.chat.type
    
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘ, ᴛʀʏ ɪᴛ ɪɴ ʏᴏᴜʀ ᴏᴡɴ ɢʀᴏᴜᴘ.</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and str(userid) not in ADMINS:
        await message.reply_text("<b>Only group owner can use this command 😂</b>")
        return

    try:
        f_sub = int(message.command[1])
    except (IndexError, ValueError):
        return await m.edit("<b>❌ Incorrect format!\nUse `/fsub ChannelID`</b>")

    try:
        c_link = await bot.export_chat_invite_link(grpid)
    except Exception as e:
        text = f"❌ Error: `{str(e)}`\n\nMake sure I'm admin in that channel & this group with all permissions"
        return await m.edit(text)

    await save_group_settings(grpid, 'f_sub', f_sub)
    await m.edit(f"<b>✅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴀᴛᴛᴀᴄʜᴇᴅ ꜰᴏʀᴄᴇꜱᴜʙ ᴛᴏ [{title}]({c_link})!\n\n➥ ꜰᴏʀᴄᴇꜱᴜʙ ᴄʜᴀɴɴᴇʟ ☞  <code>{f_sub}</code></b>", disable_web_page_preview=True)

@Client.on_message(filters.group & filters.command("remove_fsub"))
async def remove_fsub_cmd(bot, message):
    m = await message.reply("<b>Please Wait...</b>")

    chat_type = message.chat.type
    
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("<b>ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴʟʏ ɪɴ ɢʀᴏᴜᴘ, ᴛʀʏ ɪᴛ ɪɴ ʏᴏᴜʀ ᴏᴡɴ ɢʀᴏᴜᴘ.</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    
    if user.status not in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and str(userid) not in ADMINS:
        await message.reply_text("<b>Only group owner can use this command 😂</b>")
        return
    try:
        await save_group_settings(grpid, 'f_sub', None)
        await m.edit(f"<b>✅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ꜰᴏʀᴄᴇꜱᴜʙ ꜰʀᴏᴍ [{title}]!</b>")
    except Exception as e:
        await m.edit(f"❌ Error: `{str(e)}`")
