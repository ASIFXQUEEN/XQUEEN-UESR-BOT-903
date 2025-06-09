import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message
from ... import app, SUDO_USER  # Update this if not 3-dot relative

@app.on_message(filters.command(["m", "mmf"], ".") & (filters.me | filters.user(SUDO_USER)))
async def mmf(_, message: Message):
    chat_id = message.chat.id
    reply = message.reply_to_message

    if len(message.text.split()) < 2:
        return await message.reply_text("**Give me text after /mmf to memify.**")

    if not reply or not reply.media:
        return await message.reply_text("**Reply to an image or sticker to memify.**")

    msg = await message.reply_text("**Memifying this image! ✊🏻**")
    text = message.text.split(None, 1)[1]

    try:
        file_path = await app.download_media(reply)
    except Exception as e:
        return await msg.edit(f"**Media download failed:** `{e}`")

    if not file_path:
        return await msg.edit("**Couldn't download the media.**")

    meme_path = await drawText(file_path, text)

    if not os.path.exists(meme_path):
        return await msg.edit("**Failed to create meme.**")

    try:
        await app.send_document(chat_id, document=meme_path)
    except Exception as e:
        await msg.edit(f"**Sending meme failed:** `{e}`")
        return

    await msg.delete()
    os.remove(meme_path)


async def drawText(image_path, text):
    try:
        img = Image.open(image_path).convert("RGB")
    except Exception:
        return None

    os.remove(image_path)

    i_width, i_height = img.size

    # Font setup
    if os.name == "nt":
        font_path = "arial.ttf"
    else:
        font_path = "./font/Montserrat.ttf"

    try:
        m_font = ImageFont.truetype(font_path, int((70 / 640) * i_width))
    except:
        m_font = ImageFont.load_default()

    # Split upper/lower
    if ";" in text:
        upper_text, lower_text = text.split(";", 1)
    else:
        upper_text, lower_text = text, ""

    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5

    def draw_outlined_text(center_x, y, line, font, draw_obj):
        w, h = draw_obj.textsize(line, font=font)
        x = (center_x - w) / 2
        shadow_color = (0, 0, 0)
        text_color = (255, 255, 255)
        # Outline
        for dx in [-2, 2]:
            for dy in [-2, 2]:
                draw_obj.text((x + dx, y + dy), line, font=font, fill=shadow_color)
        draw_obj.text((x, y), line, font=font, fill=text_color)

    # Top text
    for line in textwrap.wrap(upper_text, width=15):
        draw_outlined_text(i_width, int((current_h / 640) * i_width), line, m_font, draw)
        current_h += m_font.getsize(line)[1] + pad

    # Bottom text
    if lower_text:
        for line in textwrap.wrap(lower_text, width=15):
            h_offset = m_font.getsize(line)[1]
            y = i_height - h_offset - int((20 / 640) * i_width)
            draw_outlined_text(i_width, y, line, m_font, draw)

    output = "memify.webp"
    img.save(output, "webp")
    return output
