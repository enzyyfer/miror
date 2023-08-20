#!/usr/bin/env python3

YT_HELP_MESSAGE = """
📺 <b>Kirim tautan bersama dengan baris perintah</b>:
<code>/cmd</code> link -s -n nama baru -opt x:y|x1:y1

📝 <b>Dengan membalas tautan</b>:
<code>/cmd</code> -n nama baru -z kata sandi -opt x:y|x1:y1

🆕 <b>Nama Baru</b>: -n
<code>/cmd</code> link -n nama baru
Catatan: Jangan tambahkan ekstensi file

🌟 <b>Tombol Kualitas</b>: -s
Jika kualitas default ditambahkan dari opsi yt-dlp menggunakan format dan Anda perlu memilih kualitas untuk tautan tertentu atau tautan dengan fitur multi tautan.
<code>/cmd</code> link -s

📜 <b>Ekstrak/Zip</b>: -e -z
<code>/cmd</code> link -e kata sandi (ekstrak dengan kata sandi terlindungi)
<code>/cmd</code> link -z kata sandi (zip dengan kata sandi terlindungi)
<code>/cmd</code> link -z kata sandi -e (ekstrak dan zip dengan kata sandi terlindungi)
<code>/cmd</code> link -e kata sandi -z kata sandi (ekstrak dengan kata sandi terlindungi dan zip dengan kata sandi terlindungi)
Catatan: Ketika keduanya ekstrak dan zip ditambahkan dengan perintah, itu akan diekstrak terlebih dahulu dan kemudian di-zip, jadi selalu ekstrak terlebih dahulu

🎬 <b>Pilihan</b>: -opt
<code>/cmd</code> link -opt playliststart:^10|fragment_retries:^inf|matchtitle:S13|writesubtitles:true|live_from_start:true|postprocessor_args:{"ffmpeg": ["-threads", "4"]}|wait_for_video:(5, 100)
Catatan: Tambahkan `^` sebelum angka atau pecahan, beberapa nilai harus berupa angka dan beberapa nilai harus berupa string.
Misalnya, playlist_items:10 bekerja dengan string, jadi tidak perlu menambahkan `^` sebelum angka tetapi playlistend hanya bekerja dengan bilangan bulat sehingga Anda harus menambahkan `^` sebelum angka seperti contoh di atas.
Anda dapat menambahkan tuple dan dict juga. Gunakan tanda kutip ganda di dalam dict.

🔗 <b>Multi tautan hanya dengan membalas ke tautan pertama</b>: -i
<code>/cmd</code> -i 10(jumlah tautan)

📦 <b>Multi tautan dalam direktori upload yang sama hanya dengan membalas ke tautan pertama</b>: -m
<code>/cmd</code> -i 10(jumlah tautan) -m nama folder

☁️ <b>Unggah</b>: -up
<code>/cmd</code> link -up <code>rcl/gdl</code> (Untuk memilih konfigurasi/token.pickle rclone, remote & path/ gdrive id atau Tg id/nama pengguna)
Anda dapat langsung menambahkan jalur unggah: -up remote:dir/subdir atau -up (Gdrive_id) atau -up id/nama pengguna
Jika DEFAULT_UPLOAD adalah `rc`, maka Anda dapat melalui up: `gd` untuk mengunggah menggunakan alat gdrive ke GDRIVE_ID.
Jika DEFAULT_UPLOAD adalah `gd`, maka Anda dapat melalui up: `rc` untuk mengunggah ke RCLONE_PATH.
Jika Anda ingin menambahkan jalur atau gdrive secara manual dari konfigurasi/token Anda (diunggah dari pengaturan pengguna), tambahkan <code>mrcc:</code> untuk rclone dan <code>mtp:</code> sebelum jalur/gdrive_id tanpa spasi
<code>/cmd</code> link -up <code>mrcc:</code>main:dump atau -up <code>mtp:</code>gdrive_id atau -up b:id/nama pengguna(leeched oleh bot) atau -up u:id/nama pengguna(leeched oleh pengguna)
DEFAULT_UPLOAD tidak berpengaruh pada perintah leech.

🔄 <b>Bendera Rclone</b>: -rcf
<code>/cmd</code> link -up path|rcl -rcf --buffer-size:8M|--drive-starred-only|key|key:value
Ini akan menggantikan semua bendera lain kecuali --exclude
Lihat semua <a href='https://rclone.org/flags/'>RcloneFlags</a> di sini.

📦 <b>Pengunduhan Massal</b>: -b
Pengunduhan massal dapat digunakan melalui pesan teks dan dengan membalas ke file teks yang berisi tautan yang dipisahkan oleh baris baru.
Anda hanya dapat menggunakannya dengan membalas ke pesan(teks/file).
Semua opsi harus bersamaan dengan tautan!
Contoh:
tautan1 -n nama baru -up remote1:path1 -rcf |key:value|key:value
tautan2 -z -n nama baru -up remote2:path2
tautan3 -e -n nama baru -opt ytdlpoptions
Catatan: Anda tidak dapat menambahkan argumen -m untuk beberapa tautan saja, lakukanlah untuk semua tautan atau gunakan multi tanpa bulk!
Membalas contoh ini dengan perintah ini <code>/cmd</code> -b(bulk)
Anda dapat mengatur awal dan akhir tautan dari bulk dengan -b start:end atau hanya akhir dengan -b :end atau hanya awal dengan -b start. Awal default adalah dari nol(tautan pertama) hingga inf.

Periksa di sini semua <a href='https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md'>SITUS</a> yang didukung
Periksa semua opsi api yt-dlp dari <a href='https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py#L184'>FILE</a> ini atau gunakan <a href='https://t.me/mltb_official_channel/177'>script</a> ini untuk mengonversi argumen cli ke opsi api.
"""

MIRROR_HELP_MESSAGE = """
<code>/cmd</code> link -n nama baru

<b>Dengan membalas ke tautan/file</b>:
<code>/cmd</code> -n nama baru -z -e -up tujuan unggah

🆕 <b>Nama Baru</b>: -n
<code>/cmd</code> link -n nama baru
Catatan: Tidak berlaku untuk torrent.

🔒 <b>Otentikasi tautan langsung</b>: -au -ap
<code>/cmd</code> link -au nama_pengguna -ap kata_sandi

📜 <b>Ekstrak/Zip</b>: -e -z
<code>/cmd</code> link -e kata sandi (ekstrak dengan kata sandi terlindungi)
<code>/cmd</code> link -z kata sandi (zip dengan kata sandi terlindungi)
<code>/cmd</code> link -z kata sandi -e (ekstrak dan zip dengan kata sandi terlindungi)
<code>/cmd</code> link -e kata sandi -z kata sandi (ekstrak dengan kata sandi terlindungi dan zip dengan kata sandi terlindungi)
Catatan: Ketika keduanya ekstrak dan zip ditambahkan dengan perintah, itu akan diekstrak terlebih dahulu dan kemudian di-zip, jadi selalu ekstrak terlebih dahulu

📌 <b>Pemilihan Bittorrent</b>: -s
<code>/cmd</code> link -s atau dengan membalas ke file/tautan

⏳ <b>Penyemaian Bittorrent</b>: -d
<code>/cmd</code> link -d rasio:waktu atau dengan membalas ke file/tautan
Untuk menentukan rasio dan waktu seed, tambahkan -d rasio:waktu. Contoh: -d 0.7:10 (rasio dan waktu) atau -d 0.7 (hanya rasio) atau -d :10 (hanya waktu) di mana waktu dalam menit.

🔗 <b>Multi tautan hanya dengan membalas ke tautan pertama/file</b>: -i
<code>/cmd</code> -i 10(jumlah tautan/file)

📦 <b>Multi tautan dalam direktori upload yang sama hanya dengan membalas ke tautan pertama/file</b>: -m
<code>/cmd</code> -i 10(jumlah tautan/file) -m nama_folder (multi pesan)
<code>/cmd</code> -b -m nama_folder (pesan/file bulk)

☁️ <b>Unggah</b>: -up
<code>/cmd</code> link -up <code>rcl/gdl</code> (Untuk memilih konfigurasi/token.pickle rclone, remote & path/ gdrive id atau Tg id/nama pengguna)
Anda dapat langsung menambahkan jalur unggah: -up remote:dir/subdir atau -up (Gdrive_id) atau -up id/nama pengguna
Jika DEFAULT_UPLOAD adalah `rc`, maka Anda dapat melalui up: `gd` untuk mengunggah menggunakan alat gdrive ke GDRIVE_ID.
Jika DEFAULT_UPLOAD adalah `gd`, maka Anda dapat melalui up: `rc` untuk mengunggah ke RCLONE_PATH.
Jika Anda ingin menambahkan jalur atau gdrive secara manual dari konfigurasi/token Anda (diunggah dari pengaturan pengguna), tambahkan <code>mrcc:</code> untuk rclone dan <code>mtp:</code> sebelum jalur/gdrive_id tanpa spasi
<code>/cmd</code> link -up <code>mrcc:</code>main:dump atau -up <code>mtp:</code>gdrive_id atau -up b:id/nama pengguna(leeched oleh bot) atau -up u:id/nama pengguna(leeched oleh pengguna)
DEFAULT_UPLOAD tidak berpengaruh pada perintah leech.

🔄 <b>Bendera Rclone</b>: -rcf
<code>/cmd</code> link|path|rcl -up path|rcl -rcf --buffer-size:8M|--drive-starred-only|key|key:value
Ini akan menggantikan semua bendera lain kecuali --exclude
Lihat semua <a href='https://rclone.org/flags/'>RcloneFlags</a> di sini.

📦 <b>Pengunduhan Massal</b>: -b
Pengunduhan massal dapat digunakan melalui pesan teks dan dengan membalas ke file teks yang berisi tautan yang dipisahkan oleh baris baru.
Anda hanya dapat menggunakannya dengan membalas ke pesan(teks/file).
Semua opsi harus bersamaan dengan tautan!
Contoh:
tautan1 -n nama baru -up remote1:path1 -rcf |key:value|key:value
tautan2 -z -n nama baru -up remote2:path2
tautan3 -e -n nama baru -opt ytdlpoptions
Catatan: Anda tidak dapat menambahkan argumen -m untuk beberapa tautan saja, lakukanlah untuk semua tautan atau gunakan multi tanpa bulk!
Membalas contoh ini dengan perintah ini <code>/cmd</code> -b(bulk)
Anda dapat mengatur awal dan akhir tautan dari bulk dengan -b start:end atau hanya akhir dengan -b :end atau hanya awal dengan -b start. Awal default adalah dari nol(tautan pertama) hingga inf.

🔗 <b>Tautan TG</b>:
Perlakukan tautan seperti tautan langsung apa pun
Beberapa tautan memerlukan akses pengguna jadi pastikan Anda harus menambahkan USER_SESSION_STRING untuknya.
Tiga jenis tautan:
Publik: <code>https://t.me/channel_name/message_id</code>
Pribadi: <code>tg://openmessage?user_id=xxxxxx&message_id=xxxxx</code>
Super: <code>https://t.me/c/channel_id/message_id</code>

<b>CATATAN:</b>
1. Perintah yang dimulai dengan <b>qb</b> HANYA untuk torrent.
"""

RSS_HELP_MESSAGE = """
Gunakan format ini untuk menambahkan URL umpan:
Judul1 tautan (wajib)
Judul2 tautan -c perintah -inf xx -exf xx
Judul3 tautan -c perintah -d rasio:waktu -z kata sandi

-c perintah -up mrcc:remote:path/subdir -rcf --buffer-size:8M|key|key:value
-inf
