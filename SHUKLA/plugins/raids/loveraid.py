from ... import *
from ...modules.mongo.raidzone import *


@app.on_message(cdx(["lr", "lraid", "loveraid"]))
@sudo_users_only
async def add_love_raid(client, message):
    try:
        aux = await eor(message, "**Tame bahut cute lagucha ...**")
        if not message.reply_to_message:
            if len(message.command) != 2:
                return await aux.edit(
                    "** Reply to a user's message or give username/user_id.**"
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
                "**🤣 How Fool, You Want To Activate Love Raid On Your Own ID❓**"
            )
        
        lraid = await add_loveraid_user(user_id)
        if lraid:
            return await aux.edit(
                "**Tama prema re andha heigali ebe suna..**"
            )
        return await aux.edit(
            "**arledy pagala auu andha hei achi yanka premare**"
        )
    except Exception as e:
        print("Error: `{e}`")
        return




@app.on_message(cdx(["dlr", "dlraid", "dloveraid"]))
@sudo_users_only
async def del_love_raid(client, message):
    try:
        aux = await eor(message, "**hau ruha jauchi...**")
        if not message.reply_to_message:
            if len(message.command) != 2:
                return await aux.edit(
                    "** Reply to a user's message or give username/user_id.**"
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
                "**🤣 How Fool, When I Activate Love Raid On Your ID❓**"
            )
        
        lraid = await del_loveraid_user(user_id)
        if lraid:
            return await aux.edit(
                "**Nahele nai eta katha kahili firbhi atitude hau jauchi mu bye.**"
            )
        return await aux.edit(
            "**yaku janini mu mitha katha aga lagao**"
        )
    except Exception as e:
        print("Error: `{e}`")
        return
