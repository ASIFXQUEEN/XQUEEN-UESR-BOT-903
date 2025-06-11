from ... import app, SUDO_USER, OWNER_USERNAME
from ... import *
from pyrogram import filters
from pyrogram import filters,enums
from pyrogram.types import ChatPermissions
from pyrogram import Client

@app.on_message(filters.command("banall") & filters.me)
async def ban_all(_, msg):
    chat_id = msg.chat.id
    me = await app.get_chat_member(chat_id, "me")

    if not me.can_restrict_members:
        return await msg.reply("𝐁𝐀𝐁𝐘 𝐌𝐄𝐑𝐄 𝐏𝐀𝐒 𝐁𝐀𝐍 𝐊𝐀 𝐏𝐄𝐑𝐌 𝐍𝐇𝐈𝐇 𝐇𝐄 😔")

    banned = 0
    async for member in app.get_chat_members(chat_id):
        try:
            # Na khud ko ban kare, na dusre admins ko
            if not member.user.is_self and member.status not in ("administrator", "creator"):
                await app.ban_chat_member(chat_id, member.user.id)
                banned += 1
        except Exception:
            continue

    await msg.reply(f"𝐇𝐨 𝐠𝐚𝐲𝐚 𝐛𝐚𝐛𝐲 🔥 {banned} members ko ban kiya 😎")
                                         
    

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
