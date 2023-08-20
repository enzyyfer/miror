#!/usr/bin/env python3
from signal import signal, SIGINT
from aiofiles.os import path as aiopath, remove as aioremove
from aiofiles import open as aiopen
from os import execl as osexecl
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from time import time
from sys import executable
from pyrogram.handlers import MessageHandler
from pyrogram.filters import command
from asyncio import create_subprocess_exec, gather

from bot import bot, botStartTime, LOGGER, Interval, DATABASE_URL, QbInterval, INCOMPLETE_TASK_NOTIFIER, scheduler
from .helper.ext_utils.fs_utils import start_cleanup, clean_all, exit_clean_up
from .helper.ext_utils.bot_utils import get_readable_file_size, get_readable_time, cmd_exec, sync_to_async
from .helper.ext_utils.db_handler import DbManger
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import sendMessage, editMessage, sendFile
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.button_build import ButtonMaker
from bot.helper.listeners.aria2_listener import start_aria2_listener
from .modules import authorize, clone, gd_count, gd_delete, cancel_mirror, gd_search, mirror_leech, status, torrent_search, torrent_select, ytdlp, rss, shell, eval, users_settings, bot_settings


async def stats(_, message):
    if await aiopath.exists('.git'):
        last_commit = await cmd_exec("git log -1 --date=short --pretty=format:'%cd <b>From</b> %cr'", True)
        last_commit = last_commit[0]
    else:
        last_commit = 'No UPSTREAM_REPO'
    total, used, free, disk = disk_usage('/')
    swap = swap_memory()
    memory = virtual_memory()
    
    stats = (
        f"🔗 <b>Latest Commit:</b> {last_commit}\n\n"
        f"⏲️ <b>Bot Uptime:</b> {get_readable_time(time() - botStartTime)}\n"
        f"⌛️ <b>System Uptime:</b> {get_readable_time(time() - boot_time())}\n\n"
        f"💾 <b>Total Disk Space:</b> {get_readable_file_size(total)}\n"
        f"💿 <b>Used Disk Space:</b> {get_readable_file_size(used)} | <b>Free Disk Space:</b> {get_readable_file_size(free)}\n\n"
        f"📤 <b>Uploaded Data:</b> {get_readable_file_size(net_io_counters().bytes_sent)}\n"
        f"📥 <b>Downloaded Data:</b> {get_readable_file_size(net_io_counters().bytes_recv)}\n\n"
        f"💻 <b>CPU Usage:</b> {cpu_percent(interval=0.5)}%\n"
        f"🧠 <b>RAM Usage:</b> {memory.percent}%\n"
        f"💽 <b>Storage Usage:</b> {disk}%\n\n"
        f"🔢 <b>Physical Cores:</b> {cpu_count(logical=False)}\n"
        f"🔢 <b>Total Cores:</b> {cpu_count(logical=True)}\n\n"
        f"💼 <b>SWAP Usage:</b> {get_readable_file_size(swap.total)} | <b>Used SWAP:</b> {swap.percent}%\n"
        f"📊 <b>Total Memory:</b> {get_readable_file_size(memory.total)}\n"
        f"📈 <b>Free Memory:</b> {get_readable_file_size(memory.available)}\n"
        f"📉 <b>Used Memory:</b> {get_readable_file_size(memory.used)}"
    )
    
    await sendMessage(message, stats)



async def start(client, message):
    buttons = ButtonMaker()
    buttons.ubutton("🔗 Sharing Bot", "https://t.me/sharinguserbot")
    buttons.ubutton("👤 Pemilik", "https://t.me/biduanonline")
    buttons.ubutton("👥 Grup Support", "https://t.me/naberalmirror")
    buttons.ubutton("💰 Donasi", "https://saweria.co/lyannn")
    
    reply_markup = buttons.build_menu(2)
    
    if await CustomFilters.authorized(client, message):
        start_string = (
            "🌟 Selamat datang di Bot Naberal Mirror! 🌟\n\n"
            "Bot ini dapat melakukan mirror ke Telegram dan beberapa fitur yang keren.\n"
            f"Ketik /{BotCommands.HelpCommand} untuk mendapatkan daftar perintah yang tersedia."
        )
        await sendMessage(message, start_string, reply_markup)
    else:
        await sendMessage(message, "⛔ Anda bukan pengguna yang diizinkan!\nDeploy bot Mirror Leech Anda sendiri untuk menikmati fiturnya.", reply_markup)


async def restart(_, message):
    pesan_restart = await sendMessage(message, "🔄 Sedang Merestart...")
    if scheduler.running:
        scheduler.shutdown(wait=False)
    for interval in [QbInterval, Interval]:
        if interval:
            interval[0].cancel()
    await sync_to_async(clean_all)
    proses1 = await create_subprocess_exec('pkill', '-9', '-f', 'gunicorn|aria2c|qbittorrent-nox|ffmpeg|rclone')
    proses2 = await create_subprocess_exec('python3', 'update.py')
    await gather(proses1.wait(), proses2.wait())
    async with aiopen(".restartmsg", "w") as f:
        await f.write(f"{pesan_restart.chat.id}\n{pesan_restart.id}\n")
    osexecl(executable, executable, "-m", "bot")



async def ping(_, message):
    start_time = int(round(time() * 1000))
    pesan_mulai = await sendMessage(message, "🏓 Memulai Ping")
    end_time = int(round(time() * 1000))
    await editMessage(pesan_mulai, f'🏓 Ping: {end_time - start_time} ms')



async def log(_, message):
    await sendFile(message, 'log.txt')

help_string = f'''
📚 **Menu Bantuan**

Catatan: Cobalah setiap perintah tanpa argumen untuk melihat detail lebih lanjut.

📂 /{BotCommands.MirrorCommand[0]} atau /{BotCommands.MirrorCommand[1]}: Memulai pemindaian ke Google Drive.
📂 /{BotCommands.QbMirrorCommand[0]} atau /{BotCommands.QbMirrorCommand[1]}: Memulai pemindaian ke Google Drive menggunakan qBittorrent.
📺 /{BotCommands.YtdlCommand[0]} atau /{BotCommands.YtdlCommand[1]}: Memulai pemindaian tautan yang didukung oleh yt-dlp.
📂 /{BotCommands.LeechCommand[0]} atau /{BotCommands.LeechCommand[1]}: Memulai mengecilkan ukuran ke Telegram.
📂 /{BotCommands.QbLeechCommand[0]} atau /{BotCommands.QbLeechCommand[1]}: Memulai mengecilkan ukuran menggunakan qBittorrent.
📺 /{BotCommands.YtdlLeechCommand[0]} atau /{BotCommands.YtdlLeechCommand[1]}: Mengecilkan ukuran tautan yang didukung oleh yt-dlp.
📂 /{BotCommands.CloneCommand} [tautan_drive]: Menyalin berkas/folder ke Google Drive.
📂 /{BotCommands.CountCommand} [tautan_drive]: Menghitung berkas/folder di Google Drive.
📂 /{BotCommands.DeleteCommand} [tautan_drive]: Menghapus berkas/folder dari Google Drive (Hanya Pemilik & Sudo).
👥 /{BotCommands.UserSetCommand} [kueri]: Pengaturan pengguna.
🤖 /{BotCommands.BotSetCommand} [kueri]: Pengaturan bot.
📂 /{BotCommands.BtSelectCommand}: Pilih berkas dari torrent berdasarkan gid atau balasan.
📂 /{BotCommands.CancelMirror}: Batalkan tugas berdasarkan gid atau balasan.
📂 /{BotCommands.CancelAllCommand} [kueri]: Batalkan semua tugas [status].
📂 /{BotCommands.ListCommand} [kueri]: Cari di Google Drive.
🔍 /{BotCommands.SearchCommand} [kueri]: Cari torrent dengan API.
📂 /{BotCommands.StatusCommand}: Menampilkan status semua unduhan.
📊 /{BotCommands.StatsCommand}: Menampilkan statistik mesin tempat bot dihosting.
🏓 /{BotCommands.PingCommand}: Periksa berapa lama waktu yang dibutuhkan untuk melakukan Ping ke Bot (Hanya Pemilik & Sudo).
🔑 /{BotCommands.AuthorizeCommand}: Menyetujui obrolan atau pengguna untuk menggunakan bot (Hanya Pemilik & Sudo).
🚫 /{BotCommands.UnAuthorizeCommand}: Membatalkan persetujuan obrolan atau pengguna untuk menggunakan bot (Hanya Pemilik & Sudo).
👥 /{BotCommands.UsersCommand}: menampilkan pengaturan pengguna (Hanya Pemilik & Sudo).
🔒 /{BotCommands.AddSudoCommand}: Tambahkan pengguna sudo (Hanya Pemilik).
🔓 /{BotCommands.RmSudoCommand}: Hapus pengguna sudo (Hanya Pemilik).
🔄 /{BotCommands.RestartCommand}: Memulai ulang dan memperbarui bot (Hanya Pemilik & Sudo).
📜 /{BotCommands.LogCommand}: Dapatkan file log bot. Berguna untuk mendapatkan laporan crash (Hanya Pemilik & Sudo).
🛠️ /{BotCommands.ShellCommand}: Jalankan perintah shell (Hanya Pemilik).
💡 /{BotCommands.EvalCommand}: Jalankan Kode Python Baris | Baris (Hanya Pemilik).
📝 /{BotCommands.ExecCommand}: Jalankan Perintah Dalam Eksekusi (Hanya Pemilik).
🧹 /{BotCommands.ClearLocalsCommand}: Bersihkan lokal {BotCommands.EvalCommand} atau {BotCommands.ExecCommand} (Hanya Pemilik).
📰 /{BotCommands.RssCommand}: Menu RSS.
'''



async def bot_help(_, message):
    await sendMessage(message, help_string)


async def restart_notification():
    if await aiopath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
    else:
        chat_id, msg_id = 0, 0

    async def send_incomplete_task_message(cid, msg):
        try:
            if msg.startswith('✅ Berhasil Merestart!'):
                await bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text=msg)
                await aioremove(".restartmsg")
            else:
                await bot.send_message(chat_id=cid, text=msg, disable_web_page_preview=True,
                                       disable_notification=True)
        except Exception as e:
            LOGGER.error(e)

    if INCOMPLETE_TASK_NOTIFIER and DATABASE_URL:
        if notifier_dict := await DbManger().get_incomplete_tasks():
            for cid, data in notifier_dict.items():
                msg = '✅ Berhasil Merestart!' if cid == chat_id else '🔄 Bot Telah Merestart!'
                for tag, links in data.items():
                    msg += f"\n\n📁 {tag}: "
                    for index, link in enumerate(links, start=1):
                        msg += f" <a href='{link}'>#{index}</a> |"
                        if len(msg.encode()) > 4000:
                            await send_incomplete_task_message(cid, msg)
                            msg = ''
                if msg:
                    await send_incomplete_task_message(cid, msg)

    if await aiopath.isfile(".restartmsg"):
        try:
            await bot.edit_message_text(chat_id=chat_id, message_id=msg_id, text='✅ Berhasil Merestart!')
        except:
            pass
        await aioremove(".restartmsg")



async def main():
    await gather(start_cleanup(), torrent_search.initiate_search_tools(), restart_notification())
    await sync_to_async(start_aria2_listener, wait=False)

    bot.add_handler(MessageHandler(
        start, filters=command(BotCommands.StartCommand)))
    bot.add_handler(MessageHandler(log, filters=command(
        BotCommands.LogCommand) & CustomFilters.sudo))
    bot.add_handler(MessageHandler(restart, filters=command(
        BotCommands.RestartCommand) & CustomFilters.sudo))
    bot.add_handler(MessageHandler(ping, filters=command(
        BotCommands.PingCommand) & CustomFilters.authorized))
    bot.add_handler(MessageHandler(bot_help, filters=command(
        BotCommands.HelpCommand) & CustomFilters.authorized))
    bot.add_handler(MessageHandler(stats, filters=command(
        BotCommands.StatsCommand) & CustomFilters.authorized))
    LOGGER.info("Bot Started!")
    signal(SIGINT, exit_clean_up)

bot.loop.run_until_complete(main())
bot.loop.run_forever()
