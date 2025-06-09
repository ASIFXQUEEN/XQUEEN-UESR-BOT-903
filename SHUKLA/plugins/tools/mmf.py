import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from pyrogram import filters
from pyrogram.types import Message
from ... import app, SUDO_USER


@app.on_message(filters.command(["m", "mmf"], ".") & (filters.me | filters.user(SUDO_USER)))
async def mmf(_, message: Message):
    chat_id = message.chat.id
    reply_message = message.reply_to_message

    if not reply_message or not reply_message.photo:
        return await message.reply_text("**Reply to an image with `.mmf your_text` to create meme.**")

    if len(message.text.split()) < 2:
        return await message.reply_text("**Give me text after `.mmf` to memify.**\n\nExample: `.mmf Upper text ; Bottom text`")

    msg = await message.reply_text("**Memifying this image! ✊🏻**")
    text = message.text.split(None, 1)[1]

    file_path = await app.download_media(reply_message)

    meme = await drawText(file_path, text)
    if meme:
        await app.send_document(chat_id, document=meme)
        os.remove(meme)
    else:
        await message.reply_text("Failed to generate meme 😔")

    await msg.delete()


async def drawText(image_path, text):
    try:
        img = Image.open(image_path).convert("RGB")
    except Exception:
        return None

    os.remove(image_path)

    i_width, i_height = img.size

    # Font Path
    if os.name == "nt":
        font_path = "arial.ttf"
    else:
        font_path = "./font/Montserrat.ttf"

    font_size = int(i_height * 0.08)
    try:
        m_font = ImageFont.truetype(font_path, font_size)
    except:
        m_font = ImageFont.load_default()

    if ";" in text:
        upper_text, lower_text = text.split(";", 1)
    else:
        upper_text, lower_text = text, ""

    draw = ImageDraw.Draw(img)

    def draw_centered_text(y, line):
        text_width, text_height = draw.textsize(line, font=m_font)
        x = (i_width - text_width) / 2
        # Outline
        for dx in [-2, 2]:
            for dy in [-2, 2]:
                draw.text((x + dx, y + dy), line, font=m_font, fill="black")
        # Main text
        draw.text((x, y), line, font=m_font, fill="white")

    current_h = 20
    wrap_chars = max(15, i_width // (font_size // 2))

    # Upper text
    for line in textwrap.wrap(upper_text.strip(), width=wrap_chars):
        draw_centered_text(current_h, line)
        current_h += font_size + 10

    # Bottom text
    if lower_text:
        lower_lines = textwrap.wrap(lower_text.strip(), width=wrap_chars)
        total_height = len(lower_lines) * (font_size + 10)
        current_h = i_height - total_height - 20
        for line in lower_lines:
            draw_centered_text(current_h, line)
            current_h += font_size + 10

    output = "memify.webp"
    img.save(output, "webp")
    return output


__NAME__ = "Mᴍғ"
__MENU__ = """
`.mmf` - **Make meme from an image.**\n
**Usage:** Reply to image with `.mmf Your text here` or `.mmf Top ; Bottom`
"""
