from asyncio.queues import QueueEmpty
from pyrogram import filters

from ... import *
from ...modules.mongo.streams import *
from ...modules.utilities import queues


@app.on_message(cdx(["stp"]) & ~filters.private)
@sudo_users_only
async def stop_stream(client, message):
    chat_id = message.chat.id
    try:
        a = await call.get_call(chat_id)
        if a.status in ["playing", "paused"]:
            try:
                queues.clear(chat_id)
            except QueueEmpty:
                pass
            await call.change_stream(chat_id)
            await eor(message, "**Stream Stopped!**")
        elif a.status == "not_playing":
            await eor(message, "**Nothing Playing!**")
    except Exception as e:
        if "not joined" in str(e).lower():
            await eor(message, "**I am Not in VC!**")
        else:
            print(f"Error: {e}")


@app.on_message(cdz(["cstp"]))
@sudo_users_only
async def stop_stream_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")
    try:
        a = await call.get_call(chat_id)
        if a.status in ["playing", "paused"]:
            try:
                queues.clear(chat_id)
            except QueueEmpty:
                pass
            await call.change_stream(chat_id)
            await eor(message, "**Stream Stopped!**")
        elif a.status == "not_playing":
            await eor(message, "**Nothing Playing!**")
    except Exception as e:
        if "not joined" in str(e).lower():
            await eor(message, "**I am Not in VC!**")
        else:
            print(f"Error: {e}")


@app.on_message(cdz(["end"]) & ~filters.private)
@sudo_users_only
async def close_stream_(client, message):
    chat_id = message.chat.id
    try:
        a = await call.get_call(chat_id)
        if a.status in ["not_playing", "playing", "paused"]:
            try:
                queues.clear(chat_id)
            except QueueEmpty:
                pass
            await call.leave_group_call(chat_id)
            await eor(message, "**Stream Ended!**")
    except Exception as e:
        if "not joined" in str(e).lower():
            await eor(message, "**I am Not in VC!**")
        else:
            print(f"Error: {e}")


@app.on_message(cdz(["cend"]))
@sudo_users_only
async def close_stream_chat(client, message):
    user_id = message.from_user.id
    chat_id = await get_chat_id(user_id)
    if chat_id == 0:
        return await eor(message, "**🥀 No Stream Chat Set❗**")
    try:
        a = await call.get_call(chat_id)
        if a.status in ["not_playing", "playing", "paused"]:
            try:
                queues.clear(chat_id)
            except QueueEmpty:
                pass
            await call.leave_group_call(chat_id)
            await eor(message, "**Stream Ended!**")
    except Exception as e:
        if "not joined" in str(e).lower():
            await eor(message, "**I am Not in VC!**")
        else:
            print(f"Error: {e}")
