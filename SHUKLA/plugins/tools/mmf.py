import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message
from ... import app, SUDO_USER


@app.on_message(filters.command(["m", "mmf"], ".") & (filters.me | filters.user(SUDO_USER)))
async def mmf(_, message: Message):
    reply = message.reply_to_message
    if not reply or not (reply.photo or reply.sticker):
        return await message.reply_text("**Reply to a photo or sticker with `.mmf Your text`**")

    if len(message.text.split()) < 2:
        return await message.reply_text("**Give me text after `.mmf` to memify.**\nExample: `.mmf Top text ; Bottom text`")

    msg = await message.reply_text("**Memifying this image! ✊🏻**")
    text = message.text.split(None, 1)[1]

    file_path = await app.download_media(reply)

    meme = await drawText(file_path, text)
    if meme:
        await app.send_document(message.chat.id, document=meme)
        os.remove(meme)
    else:
        await message.reply_text("Failed to generate meme 😔")

    await msg.delete()


async def drawText(image_path, text):
    try:
        img = Image.open(image_path).convert("RGB")
    except:
        return None

    os.remove(image_path)
    i_width, i_height = img.size

    # Font
    font_path = "./font/Montserrat.ttf" if os.name != "nt" else "arial.ttf"
    font_size = int(i_height * 0.08)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except:
        font = ImageFont.load_default()

    if ";" in text:
        top_text, bottom_text = text.split(";", 1)
    else:
        top_text, bottom_text = text, ""

    draw = ImageDraw.Draw(img)

    def draw_centered(y, txt):
        w, h = draw.textsize(txt, font=font)
        x = (i_width - w) / 2
        for dx in [-2, 2]:
            for dy in [-2, 2]:
                draw.text((x + dx, y + dy), txt, font=font, fill="black")
        draw.text((x, y), txt, font=font, fill="white")

    wrap_width = max(20, i_width // (font_size // 2))

    # Top text center
    current_h = i_height // 4
    for line in textwrap.wrap(top_text.strip(), width=wrap_width):
        draw_centered(current_h, line)
        current_h += font_size + 10

    # Bottom text center
    if bottom_text:
        bottom_lines = textwrap.wrap(bottom_text.strip(), width=wrap_width)
        total_h = len(bottom_lines) * (font_size + 10)
        current_h = i_height - total_h - 40
        for line in bottom_lines:
            draw_centered(current_h, line)
            current_h += font_size + 10

    output = "memify.webp"
    img.save(output, "webp")
    return output


__NAME__ = "Mᴍғ"
__MENU__ = """
`.mmf` - Reply to a sticker or image with text to generate meme.
Example: `.mmf Hello ; Bye`
"""
