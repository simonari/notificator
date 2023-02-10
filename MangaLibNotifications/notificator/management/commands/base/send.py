import telegram.constants

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from .db.getters import objects


async def compose_message(m, pi):
    base_url = "https://mangalib.me"

    text = f"<b>{m.name_ru}</b>\n" \
             f"\n" \
             f"<b>Том: {m.last_volume}</b>\n" \
             f"<b>Глава: {m.last_ch if m.last_ch % 1 != 0 else int(m.last_ch)}</b>\n"

    img = m.cover_img

    url = f"{base_url}/{m.salt}/v{m.last_volume}/c{m.last_ch}?ui={pi}"

    return text, img, url


async def new_chapter(bot, ti, mi, pi):
    m = await objects.manga_obj(mi)

    text, img, url = await compose_message(m, pi)

    await bot.sendPhoto(ti, img,
                        caption=text,
                        parse_mode=telegram.constants.ParseMode.HTML,
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton(text="Читать", url=url)]
                        ]))