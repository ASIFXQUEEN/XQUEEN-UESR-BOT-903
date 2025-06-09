from ... import *
from ...modules.mongo.raidzone import *


@app.on_message(cdx(["lr", "lraid", "loveraid"]))
@sudo_users_only
async def add_love_raid(client, message):
    try:
        aux = await eor(message, "**Tama prema re Andha heigali Ebe Suna Prema bhara Katha**")
        if not message.reply_to_message:
            if len(message.command) != 2:
                return await aux.edit(
                    "**Reply de nahele tag kare.**"
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
                "**Ebe pura tama prema re pagal heigali Mitha mitha katha suna**"
            )
        return await aux.edit(
            "**Mu ARLEDY yara premare andhaa achii**"
        )
    except Exception as e:
        print("Error: `{e}`")
        return




@app.on_message(cdx(["dlr", "dlraid", "dloveraid"]))
@sudo_users_only
async def del_love_raid(client, message):
    try:
        aux = await eor(message, "**🔄 Processing ...**")
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
                "**Nahele nai ete katha kahili na impress hele nai bye.**"
            )
        return await aux.edit(
            "**janini aku sry**"
        )
    except Exception as e:
        print("Error: `{e}`")
        return

