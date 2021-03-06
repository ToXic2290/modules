import io
import time

from PIL import Image
from telethon.errors import (ChatAdminRequiredError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.functions.messages import EditChatAdminRequest
from telethon.tl.types import ChatAdminRights, ChatBannedRights

from .. import loader, utils

DEMOTE_RIGHTS = ChatAdminRights(post_messages=None,
                                add_admins=None,
                                invite_users=None,
                                change_info=None,
                                ban_users=None,
                                delete_messages=None,
                                pin_messages=None,
                                edit_messages=None)

UNMUTE_RIGHTS = ChatBannedRights(until_date=None,
                                 view_messages=None,
                                 send_messages=False,
                                 send_media=False,
                                 send_stickers=False,
                                 send_gifs=False,
                                 send_games=False,
                                 send_inline=False,
                                 embed_links=False)

BANNED_RIGHTS = ChatBannedRights(until_date=None,
                                 view_messages=True,
                                 send_messages=True,
                                 send_media=True,
                                 send_stickers=True,
                                 send_gifs=True,
                                 send_games=True,
                                 send_inline=True,
                                 embed_links=True)

UNBAN_RIGHTS = ChatBannedRights(until_date=None,
                                view_messages=None,
                                send_messages=None,
                                send_media=None,
                                send_stickers=None,
                                send_gifs=None,
                                send_games=None,
                                send_inline=None,
                                embed_links=None)

@loader.tds
class AdminToolsMod(loader.Module):
    """ToX security"""
    strings = {'name': 'ToX security',
               'not_pic': '<b>This isn`t an pic/sticker.</b>',
               'wait': '<b>????????????????...</b>',
               'pic_so_small': '<b>The image is too small, try another one.</b>',
               'pic_changed': '<b>Chat pic changed.</b>',
               'promote_none': '<b>No one to promote.</b>',
               'who': '<b>Who is it?</b>',
               'not_admin': '<b>?? ???? ??????????:(</b>',
               'promoted': '<b>{} promoted to admin rights.\nRank: {}</b>',
               'wtf_is_it': '<b>What is it?</b>',
               'this_isn`t_a_chat': '<b>This isn`t a chat!</b>',
               'demote_none': '<b>No one to demote.</b>',
               'demoted': '<b>{} demoted to admin rights.</b>',
               'pinning': '<b>??????????????????...</b>',
               'pin_none': '<b>?? ??????????????? ?????? ?? ???????????? ?????????? ???? ???????????????????</b>',
               'unpinning': '<b>??????????????????...</b>',
               'unpin_none': '<b>???????????? ????????????????????</b>',
               'no_rights': '<b>I don`t have rights.</b>',
               'pinned': '<b>??????, ????????????????)</b>',
               'unpinned': '<b>????????, ????????????????)</b>',
               'can`t_kick': '<b>Can`t kick.</b>',
               'kicking': '<b>????????????...</b>',
               'kick_none': '<b>???????????? ???? ????????????</b>',
               'kicked': '<b>{} ?????? ???????????? ???? ????????..)</b>',
               'kicked_for_reason': '<b>{} ???????????? ???? ???????? ????\nReason: {}.</b>',
               'banning': '<b>????????...</b>',
               'banned': '<b>{} ???????????????? ?????? (???? ????????), ?????? ??????????????</b>',
               'banned_for_reason': '<b>{} ???????????????? ?????? ????\nReason: {}</b>',
               'ban_none': '<b>???????????? ???? ??????????????</b>',
               'unban_none': '<b>???????????? ???? ????????????????</b>',
               'unbanned': '<b>{} ?????? ???? ?? ????????, ???????????????? ????????????</b>',
               'mute_none': '<b>No one to mute.</b>',
               'muted': '<b>{} ???????????????? ??????, ???????? ????????????????) </b>',
               'no_args': '<b>???????????????? ????????????????.</b>',
               'unmute_none': '<b> ?????? ???? ?? ???????? ???? ????????</b>',
               'unmuted': '<b>{} ???????????? ?????????? ??????????????????????????</b>',
               'no_reply': '<b>?????? ????????????!!!</b>',
               'del_u_search': '<b>?????????? ?????????????????? ??????????????????</b>',
               'del_u_kicking': '<b>???????????? ?????????????????? ????????????????...\nOh~, I can do it?!</b>'}

  
    async def kickcmd(self, message):
        """?????????????????? ???? ????????????\n .kick <@ ?????? ????????????>."""
        if message.is_private:
            return await utils.answer(message, self.strings('this_isn`t_a_chat', message))
        try:
            args = utils.get_args_raw(message).split(' ')
            reason = utils.get_args_raw(message)
            reply = await message.get_reply_message()

            chat = await message.get_chat()
            if not chat.admin_rights and not chat.creator:
                return await utils.answer(message, self.strings('not_admin', message))

            if not chat.admin_rights.ban_users:
                return await utils.answer(message, self.strings('no_rights', message))

            if reply:
                user = await message.client.get_entity(reply.sender_id)
                args = utils.get_args_raw(message)
                if args:
                    reason = args
            else:
                user = await message.client.get_entity(args[0] if not args[0].isnumeric() else int(args[0]))
                if args:
                    if len(args) == 1:
                        args = utils.get_args_raw(message)
                        user = await message.client.get_entity(args if not args.isnumeric() else int(args))
                        reason = False
                    elif len(args) >= 2:
                        reason = utils.get_args_raw(message).split(' ', 1)[1]

            await utils.answer(message, self.strings('kicking', message))
            try:
                await message.client.kick_participant(message.chat_id, user.id)
            except UserAdminInvalidError:
                return await utils.answer(message, self.strings('no_rights', message))
            if not reason:
                return await utils.answer(message, self.strings('kicked', message).format(user.first_name))
            if reason:
                return await utils.answer(message,
                                          self.strings('kicked_for_reason', message).format(user.first_name,
                                                                                            reason))

            return await utils.answer(message, self.strings('kicked', message).format(user.first_name))
        except ValueError:
            return await utils.answer(message, self.strings('no_args', message))

    async def bancmd(self, message):
        """???????????? ??????\n .ban <@ ?????? ????????????>."""
        if message.is_private:
            return await utils.answer(message, self.strings('this_isn`t_a_chat', message))
        try:
            args = utils.get_args_raw(message).split(' ')
            reason = utils.get_args_raw(message)
            reply = await message.get_reply_message()

            chat = await message.get_chat()
            if not chat.admin_rights and not chat.creator:
                return await utils.answer(message, self.strings('not_admin', message))

            if not chat.admin_rights.ban_users:
                return await utils.answer(message, self.strings('no_rights', message))

            if reply:
                user = await message.client.get_entity(reply.sender_id)
                args = utils.get_args_raw(message)
                if args:
                    reason = args
            else:
                user = await message.client.get_entity(args[0] if not args[0].isnumeric() else int(args[0]))
                if args:
                    if len(args) == 1:
                        args = utils.get_args_raw(message)
                        user = await message.client.get_entity(args if not args.isnumeric() else int(args))
                        reason = False
                    elif len(args) >= 2:
                        reason = utils.get_args_raw(message).split(' ', 1)[1]
            try:
                await utils.answer(message, self.strings('banning', message))
                await message.client(EditBannedRequest(message.chat_id, user.id,
                                                       ChatBannedRights(until_date=None, view_messages=True)))
            except UserAdminInvalidError:
                return await utils.answer(message, self.strings('no_rights', message))
            if not reason:
                return await utils.answer(message, self.strings('banned', message).format(user.first_name))
            if reason:
                return await utils.answer(message,
                                          self.strings('banned_for_reason', message).format(user.first_name,
                                                                                            reason))
            return await utils.answer(message, self.strings('banned', message).format(user.first_name))
        except ValueError:
            return await utils.answer(message, self.strings('no_args', message))

    async def unbancmd(self, message):
        """?????????? ??????\n .unban <@ ?????? ????????????>."""
        if message.is_private:
            return await utils.answer(message, self.strings('this_isn`t_a_chat', message))
        try:
            reply = await message.get_reply_message()

            chat = await message.get_chat()
            if not chat.admin_rights and not chat.creator:
                return await utils.answer(message, self.strings('not_admin', message))

            if not chat.admin_rights.ban_users:
                return await utils.answer(message, self.strings('no_rights', message))

            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                args = utils.get_args_raw(message)
                if not args:
                    return await utils.answer(message, self.strings('unban_none', message))
                user = await message.client.get_entity(args if not args.isnumeric() else int(args))
            await message.client(
                EditBannedRequest(message.chat_id, user.id, ChatBannedRights(until_date=None, view_messages=False)))

            return await utils.answer(message, self.strings('unbanned', message).format(user.first_name))
        except ValueError:
            return await utils.answer(message, self.strings('no_args', message))

    async def mutecmd(self, message):
        """???????????? ??????\n .mute <@ ?????? ????????????> <time (1m, 1h, 1d)>."""
        if not message.is_private:
            args = utils.get_args_raw(message).split()
            reply = await message.get_reply_message()
            timee = False

            try:
                if reply:
                    user = await message.client.get_entity(reply.sender_id)
                    args = utils.get_args_raw(message)
                    if args:
                        timee = args
                else:
                    user = await message.client.get_entity(args[0] if not args[0].isnumeric() else int(args[0]))
                    if args:
                        if len(args) == 1:
                            args = utils.get_args_raw(message)
                            user = await message.client.get_entity(args if not args.isnumeric() else int(args))
                            timee = False
                        elif len(args) >= 2:
                            timee = utils.get_args_raw(
                                message).split(' ', 1)[1]
            except ValueError:
                return await utils.answer(message, self.strings('no_args', message))

            if timee:
                n = ''
                t = ''

                for _ in timee:
                    if _.isdigit():
                        n += _
                    else:
                        t += _

                text = f"<b>{n}"

                if t == "m":
                    n = int(n) * 60
                    text += " ??????.</b>"

                elif t == "h":
                    n = int(n) * 3600
                    text += " ??????.</b>"

                elif t == "d":
                    n = int(n) * 86400
                    text += " ????.</b>"

                else:
                    return await utils.answer(message, self.strings('no_args', message))

                try:
                    tm = ChatBannedRights(
                        until_date=time.time() + int(n), send_messages=True)
                    await message.client(EditBannedRequest(message.chat_id, user.id, tm))
                    return await utils.answer(message, self.strings('muted', message).format(user.first_name) + text)
                except UserAdminInvalidError:
                    return await utils.answer(message, self.strings('no_rights', message))
            else:
                try:
                    tm = ChatBannedRights(until_date=True, send_messages=True)
                    await message.client(EditBannedRequest(message.chat_id, user.id, tm))
                    return await message.edit('<b>{} ???????????? ?? ????????.</b>'.format(user.first_name))
                except UserAdminInvalidError:
                    return await utils.answer(message, self.strings('no_rights', message))
        else:
            await utils.answer(message, self.strings('this_isn`t_a_chat', message))

    async def unmutecmd(self, message):
        """?????????? ??????\n .unmute <@ ?????? ????????????>."""
        if message.is_private:
            return await utils.answer(message, self.strings('this_isn`t_a_chat', message))
        try:
            reply = await message.get_reply_message()

            chat = await message.get_chat()
            if not chat.admin_rights and not chat.creator:
                return await utils.answer(message, self.strings('not_admin', message))

            if not chat.admin_rights.ban_users:
                return await utils.answer(message, self.strings('no_rights', message))

            if reply:
                user = await message.client.get_entity(reply.sender_id)
            else:
                args = utils.get_args_raw(message)
                if not args:
                    return await utils.answer(message, self.strings('unmute_none', message))
                user = await message.client.get_entity(args if not args.isnumeric() else int(args))
            await message.client(EditBannedRequest(message.chat_id, user.id, UNMUTE_RIGHTS))

            return await utils.answer(message, self.strings('unmuted', message).format(user.first_name))
        except ValueError:
            return await utils.answer(message, self.strings('no_args', message))


