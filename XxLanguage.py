import logging

from .. import loader, utils

logger = logging.getLogger(__name__)


@loader.tds
class MorzeMod(loader.Module):
    """Конвертация текста в шифр и наоборот.
    
    by @ToXicUse """

    strings = {"name": "Tss..."}

    @loader.unrestricted
    async def xxcmd(self, message):
        """.xx [реплай или текст]"""
        de = {
            "А": "7 ",
            "Б": "@ ",
            "В": "& ",
            "Г": "- ",
            "Д": ": ",
            "Е": "1 ",
            "Ж": "+ ",
            "З": "× ",
            "И": "= ",
            "Й": "; ",
            "К": "π ",
            "Л": "∆ ",
            "М": "0 ",
            "Н": "_ ",
            "О": "• ",
            "П": "# ",
            "Р": "¶ ",
            "С": "( ",
            "Т": "< ",
            "У": "/ ",
            "Ф": "[ ",
            "Х": "* ",
            "Ц": "> ",
            "Ч": "~ ",
            "Ш": "! ",
            "Щ": "] ",
            "Ъ": ") ",
            "Ы": "% ",
            "Ь": "| ",
            "Э": "t ",
            "Ю": "? ",
            "Я": "^ ",
        }

        reply = await message.get_reply_message()
        text = utils.get_args_raw(message)

        if reply and not text:
            text = reply.raw_text
        if not text:
            return await utils.answer(
                message, "<code>Вы не ввели текст или не сделали реплай.</code>"
            )
        x = ""
        for word in text.split():

            for letter in word.upper():
                x += de[letter]
            x += " "
        await message.edit(x)

    @loader.unrestricted
    async def xrucmd(self, message):
        """.xru [реплай или текст]"""

        en = {
            "7": "А",
            "@": "Б",
            "&": "В",
            "-": "Г",
            ":": "Д",
            "1": "Е",
            "+": "Ж",
            "×": "З",
            "=": "И",
            ";": "Й",
            "π": "К",
            "∆": "Л",
            "0": "М",
            "_": "Н",
            "•": "О",
            "#": "П",
            "¶": "Р",
            "(": "С",
            "<": "Т",
            "/": "У",
            "[": "Ф",
            "*": "Х",
            ">": "Ц",
            "~": "Ч",
            "!": "Ш",
            "]": "Щ",
            ")": "Ъ",
            "%": "Ы",
            "|": "Ь",
            "t": "Э",
            "?": "Ю",
            "^": "Я",
        }

        reply = await message.get_reply_message()
        text = utils.get_args_raw(message)

        if reply and not text:
            text = reply.raw_text
        if not text:
            return await utils.answer(
                message, "<code>Вы не ввели текст или не сделали реплай.</code>"
            )
        x = ""
        for word in text.split("  "):

            for letter in word.split():
                x += en[letter].lower()
            x += " "
        await message.edit(x)