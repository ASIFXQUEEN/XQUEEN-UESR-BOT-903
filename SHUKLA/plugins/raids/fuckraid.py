from pyrogram import Client, filters
from SHUKLA.modules.mongo.raidzone import add_fuckraid_user, del_fuckraid_user
from SHUKLA.modules.mongo.protected import is_protected
from SHUKLA import app  # tumhara Pyrogram client
from SHUKLA.utils.helpers import eor  # edit_or_reply helper function

# Sirf sudo users ke liye decorator
def sudo_users_only(func):
    async def wrapper(client, message):
        # Yahan apni sudo list check kar sakte ho
        sudo_ids = [123456789]  # Apna sudo ID yahan daalo
        if message.from_user.id not in sudo_ids:
            await message.reply("You are not authorized to use this command.")
            return
        return await func(client, message)
    return wrapper


@app.on_message(filters.command(["fr", "rr", "rraid", "fuckraid"]) & filters.me)  # ya filters.user(sudo_ids)
@sudo_users_only
async def add_fuck_raid(client, message):
    try:
        aux = await eor(message, "**🔄 Processing ...**")
        if not message.reply_to_message:
            if len(message.command) != 2:
                return await aux.edit(
                    "**🤖 Reply to a user's message or give username/user_id.**"
                )
            user = message.text.split(None, 1)[1]
            if "@" in user:
                user = user.replace("@", "")
            fulluser = await app.get_users(user)
            user_id = fulluser.id
        else:
            user_id = message.reply_to_message.from_user.id

        if user_id == message.from_user.id:
            return await aux.edit(
                "**🤣 How Fool, You Want To Activate Reply Raid On Your Own ID❓**"
            )

        if await is_protected(user_id):
            return await aux.edit("❌ This user is protected by xqueen.")
        
        added = await add_fuckraid_user(user_id)
        if added:
            return await aux.edit(
                "**🤖 Successfully Added Reply Raid On This User.**"
            )
        else:
            return await aux.edit(
                "**🤖 Hey, Reply Raid Already Active On This User❗**"
            )
    except Exception as e:
        print(f"Error: `{e}`")
        await message.reply(f"Error: `{e}`")


@app.on_message(filters.command(["dfr", "drr", "drraid", "dfuckraid"]) & filters.me)
@sudo_users_only
async def del_fuck_raid(client, message):
    try:
        aux = await eor(message, "**🔄 Processing ...**")
        if not message.reply_to_message:
            if len(message.command) != 2:
                return await aux.edit(
                    "**🤖 Reply to a user's message or give username/user_id.**"
                )
            user = message.text.split(None, 1)[1]
            if "@" in user:
                user = user.replace("@", "")
            fulluser = await app.get_users(user)
            user_id = fulluser.id
        else:
            user_id = message.reply_to_message.from_user.id
        
        if user_id == message.from_user.id:
            return await aux.edit(
                "**🤣 How Fool, When I Activate Reply Raid On Your ID❓**"
            )

        if await is_protected(user_id):
            return await aux.edit("❌ This user is protected by xqueen.")
        
        removed = await del_fuckraid_user(user_id)
        if removed:
            return await aux.edit(
                "**🤖 Successfully Removed Reply Raid From This User.**"
            )
        else:
            return await aux.edit(
                "**🤖 Hey, Reply Raid Not Active On This User❗**"
            )
    except Exception as e:
        print(f"Error: `{e}`")
        await message.reply(f"Error: `{e}`")
