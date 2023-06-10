import discord
from discord import option
from discord.ext import commands
import os
import random
import json
import datetime
from dotenv import load_dotenv
import traceback
from discord.ui import Button
import math


intents = discord.Intents.default()
intents.typing = False
intents.presences = False

now = datetime.datetime.now()
current_time = now.strftime("%Y%m%d.%H%M")

azzibotlink = "https://discord.com/api/oauth2/authorize?client_id=1020863208472444938&permissions=8&scope=bot"
azziserverlink = "https://discord.gg/bWysaCMFBm"

with open("azzidata.json", "r") as file:
    data = json.load(file)

data["version"] = f" alpha.{current_time}"

with open("azzidata.json", "w") as file:
    json.dump(data, file)

load_dotenv()
RED_COLOR = 0xFF0000
GREEN_COLOR = 0x00FF00

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix=commands.when_mentioned_or("아찌 ", "ㅇㅉ ", "아찌야 ", "ㅇㅉㅇ "), intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="테스트"))


@bot.command(name="안녕")
async def hello(ctx):
    await ctx.send("안녕하세요!")


@bot.command(name="너", aliases=["너말고", "너말구"])
async def nou(ctx, *, arg: str = ""):
    if arg.lower() == "말고" or arg.lower() == "말구":
        await ctx.send(random.choice(["왕 (넴)", "와왕! (네넵)", "왈 (넴)"]))
    else:
        raise commands.CommandNotFound()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(random.choice(["왕?", "우웅?", "왈?", "와왕?", "끼잉?", "그응?"]))

@bot.command()
async def test(ctx):
    button = Button(style=discord.ButtonStyle.link, label="테스트", url="https://discord.com/")
    view = discord.ui.View()
    view.add_item(button)

    await ctx.send("테스트티비", view=view)

@bot.slash_command(description="아찌에 대한 링크들")
@option(name="link", description="무슨 링크가 필요하신가요?", type=str, required=True, choices=["아찌를 우리서버로 입양할래!", "아찌 공식 디스코드 서버로 놀러갈래!"])
async def 링크들(ctx, link: str):
    if link == "아찌를 우리서버로 입양할래!":
        button = Button(style=discord.ButtonStyle.link, label="여기 입양 절차 서류!", url=azzibotlink)
    elif link == "아찌 공식 디스코드 서버로 놀러갈래!":
        button = Button(style=discord.ButtonStyle.link, label="여기 우리 서버야!", url=azziserverlink)
    view = discord.ui.View()
    view.add_item(button)
    await ctx.respond("여기있어!", view=view)


@bot.event
async def on_message(message):
    if message.content == "아찌야" or message.content == "아찌":
        await message.channel.send(random.choice(["왕 (넴)", "와왕! (네넵)", "왈 (넴)"]))

    elif int(message.author.id) in data["BanList"]:
        await message.channel.send("아르르르... (너에게서 나쁜냄새 난다!)")
    await bot.process_commands(message)


@bot.command(name="configs")
async def setin(ctx, arg: str, arg1: str, arg2: int = 0):
    try:
        with open("azzidata.json", "r") as file:
            data = json.load(file)
        if int(ctx.author.id) in data["AdminList"]:
            if arg == "set":
                if arg1 == "ban":
                    with open("azzidata.json", "r") as file:
                        data = json.load(file)

                    ban_number = arg2
                    data["BanList"].append(ban_number)

                    with open("azzidata.json", "w") as file:
                        json.dump(data, file)

                    await ctx.send(f"성공적으로 밴 했습니다 {arg2}")

                if arg1 == "unban":
                    with open("azzidata.json", "r") as file:
                        data = json.load(file)

                    ban_number = arg2
                    data["BanList"].remove(ban_number)

                    with open("azzidata.json", "w") as file:
                        json.dump(data, file)

                    await ctx.send(f"성공적으로 밴을 해제했습니다 {arg2}")

            elif arg == "show":
                if arg1 == "banList":
                    with open("azzidata.json", "r") as file:
                        data = json.load(file)

                    await ctx.send(data["BanList"])
        else:
            await ctx.send("와오아왕! (어디서 큰일날소리를!)")

    except Exception as e:
        error_traceback = traceback.format_exc()
        embed = discord.Embed(title="왈! 왈! (에러 났사와여!)", description=f"{error_traceback} in error {arg}", color=RED_COLOR)
        await ctx.respond(embed=embed)

@bot.command(name="config")
async def setin(ctx, arg: str, arg1: str, arg2: int = 0):
    ""
bot.remove_command("help")

@bot.command(hidden=True)
async def custom_help(ctx, *, command: str = None):
    # 아무런 동작을 하지 않고 빈 문자열을 반환합니다.
    pass

@bot.slash_command(description="debug bot (dev only)", guild_ids=[1022437977433047050])
async def debug(ctx, arg: str):
    try:
        with open("azzidata.json", "r") as file:
            data = json.load(file)

        if int(ctx.author.id) not in data["AdminList"]:
            await ctx.respond("넌 주인이 아니잖아 아르르르르르르를")
            return None

        elif arg == "shutdown":
            embed = discord.Embed(title="shutdown", description="셧다운 명령을 보냈습니다", color=RED_COLOR)
            await ctx.respond(embed=embed)
            exit(0)

        elif arg == "version":
            des = data["version"]
        elif arg == "BanList":
            des = data["BanList"]
        elif arg == "AdminList":
            des = data["AdminList"]
        elif arg == "os.getenv('TOKEN')":
            raise Exception("GivenToken")
        else:
            try:
                des = await eval(arg)
            except TypeError:
                des = eval(arg)

        embed = discord.Embed(title=arg, description=str(des), color=GREEN_COLOR)
        await ctx.respond(embed=embed)

        with open("azzidata.json", "w") as file:
            json.dump(data, file)

    except Exception as e:
        error_traceback = traceback.format_exc()
        embed = discord.Embed(title="왈! 왈! (에러 났사와여!)", description=f"{error_traceback} in error: {arg}", color=RED_COLOR)
        await ctx.respond(embed=embed)




bot.run(os.getenv('TOKEN'))
