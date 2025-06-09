from ... import *
from ...modules.mongo.streams import *
from pyrogram import filters
from pytgcalls.types.input_stream import AudioPiped
from pytgcalls.types.stream import StreamAudioEnded

@app.on_message(cdx(["join", "joinvc"]) & ~filters.private)
@sudo_users_only
async def join_vc(client, message):
    chat_id = message.chat.id
    try:
        a = await call.get_call(chat_id)
        if a:
            return await eor(message, "**Already Joined VC!**")

        await call.join(chat_id, AudioPiped("input.mp3"))  # Replace with a valid audio
        await eor(message, "**✅ Joined VC!**")
    except Exception as e:
        print(f"VC Join Error: {e}")
        await eor(message, "❌ **Failed to join VC.**")

@app.on_message(cdz(["cjoin", "cjoinvc"]))
@sudo_users_only
async def join_vc_(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")

    try:
        a = await call.get_call(chat_id)
        if a:
            return await eor(message, "**Already Joined VC!**")

        await call.join(chat_id, AudioPiped("input.mp3"))  # Replace with a valid audio
        await eor(message, "**✅ Joined VC!**")
    except Exception as e:
        print(f"VC Join Error: {e}")
        await eor(message, "❌ **Failed to join VC.**")
