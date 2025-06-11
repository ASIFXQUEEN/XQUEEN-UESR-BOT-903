from ... import app, SUDO_USER, OWNER_USERNAME
from ... import *
from pyrogram import filters
from pyrogram import filters,enums
from pyrogram.types import ChatPermissions
from pyrogram import Client, filters
from pyrogram import Client, filters

@app.on_message(filters.command("banall", prefixes=[".", "/", "!"]) & filters.me)
async def ban_all(client, msg):  # Make sure 'client' is passed here
    chat_id = msg.chat.id

    # Use correct method to get your own info in the chat
    me = await client.get_chat_member(chat_id, "me")

    # DEBUG LOGGING (will show in Heroku logs)
    print(f"[DEBUG] Status: {me.status}")
    print(f"[DEBUG] Privileges: {getattr(me, 'privileges', None)}")

    # Allow both creator and admin
    if me.status not in ("administrator", "creator"):
        return await msg.reply("💡 Baby mujhe admin to bana pehle...")

    # If not creator, check for restrict permission
    if me.status != "creator":
        if not getattr(me, "privileges", None):
            return await msg.reply("👀 Baby mujhe full admin powers do...")
        if not me.privileges.can_restrict_members:
            return await msg.reply("😭 Baby mujhe ban karne ka haq nahi mila...")

    # Start banning users
    banned = 0
    async for member in client.get_chat_members(chat_id):
        try:
            if (
                not member.user.is_self
                and member.status not in ("administrator", "creator")
            ):
                await client.ban_chat_member(chat_id, member.user.id)
                banned += 1
        except Exception as e:
            print(f"[ERROR] Failed to ban {member.user.id}: {e}")
            continue

    await msg.reply(f"✅ Baby ban done: {banned} members gaya 🚫")
    

#........................................................................................................................#



@app.on_message(cdz(["kickall"])  & (filters.me | filters.user(SUDO_USER))
     )
async def ban_all(_,msg):
    chat_id=msg.chat.id    
    bot=await app.get_chat_member(chat_id,OWNER_USERNAME)
    bot_permission=bot.privileges.can_restrict_members==True    
    if bot_permission:
        async for member in app.get_chat_members(chat_id):       
            try:
                    await app.ban_chat_member(chat_id, member.user.id)
                    await msg.reply_text(f"𝐖ʟᴄ 𝐁ᴀʙʏ 😒❤️ {member.user.mention}")
                    await app.unban_chat_member(chat_id,member.user.id)                    
            except Exception:
                pass
    else:
        await msg.reply_text(" 𝐎𝐇 𝐍𝐎 𝐁𝐀𝐁𝐘 ") 
        
        
#........................................................................................................................#


@app.on_message(cdz(["unmuteall"])  & (filters.me | filters.user(SUDO_USER))
     )
async def unmute_all(_,msg):
    chat_id=msg.chat.id   
    x = 0
    bot=await app.get_chat_member(chat_id,OWNER_USERNAME)
    bot_permission=bot.privileges.can_restrict_members==True 
    if bot_permission:
        banned_users = []
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.RESTRICTED):
            banned_users.append(m.user.id)       
            try:
                    await app.restrict_chat_member(chat_id,banned_users[x], ChatPermissions(can_send_messages=True,can_send_media_messages=True,can_send_polls=True,can_add_web_page_previews=True,can_invite_users=True))
                    await msg.reply_text(f"ᴜɴᴍᴜᴛɪɴɢ ᴀʟʟ ᴍᴇᴍʙᴇʀs {m.user.mention}")
                    x += 1
                                        
            except Exception as e:
                print(e)
    else:
        await msg.reply_text("ᴇɪᴛʜᴇʀ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs")

  
  
#........................................................................................................................#


@app.on_message(cdz(["unbanall"])  & (filters.me | filters.user(SUDO_USER))
     )
async def unban_all(_,msg):
    chat_id=msg.chat.id   
    x = 0
    bot=await app.get_chat_member(chat_id,OWNER_USERNAME)
    bot_permission=bot.privileges.can_restrict_members==True 
    if bot_permission:
        banned_users = []
        async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BANNED):
            banned_users.append(m.user.id)       
            try:
                    await app.unban_chat_member(chat_id,banned_users[x])
                    await msg.reply_text(f"ᴜɴʙᴀɴɪɴɢ ᴀʟʟ ᴍᴄ ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ {m.user.mention}")
                    x += 1
                                        
            except Exception:
                pass
    else:
        await msg.reply_text("ᴇɪᴛʜᴇʀ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ sᴜᴅᴏ ᴜsᴇʀs")
  
        
              
__NAME__ = "Bᴀɴ"
__MENU__ = """
`.banll` ** ban all user **
`.unbanall` **unban all user**
`.kickall` **kickall all user**
`.unmuteall` **unmute all user**
"""      
