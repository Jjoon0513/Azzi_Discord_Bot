import discord
from discord import option
from discord.ext import commands, tasks
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

@tasks.loop(hours=1)
async def giveallsnack():
    now = datetime.datetime.now()
    if now.minute == 0 and now.second == 0:
        with open("azzisnack.json", "r") as file:
            data = json.load(file)

        for user_id in data["snack_count"]:
            data["snack_count"][user_id] += 3

        with open("azzisnack.json", "w") as file:
            json.dump(data, file)


with open("azzidata.json", "r") as file:
    data = json.load(file)

data["version"] = "azzi.alpha.0"

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
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="아찌 알파.0 테스트"))
    await giveallsnack()

@bot.command(name="status")
async def status(ctx):
    await ctx.send("online")


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

@bot.command(name="내간식확인", aliases=["내 간식 확인"])
async def mysnackcheck(ctx):
    with open("azzisnack.json", "r") as file:
        data = json.load(file)
    with open("azzisnackid.json", "r") as file:
        data1 = json.load(file)

    snackid = data1["snack_count"].get(str(ctx.author.id), 0)
    snacks = data["snack_count"].get(str(ctx.author.id), 0)
    username = ctx.author.name
    await ctx.send(f"**{username}**님의 간식은 **{snacks}**개 남았고 한 **{snackid}**개 정도 준거 같네요!")

@bot.command(name="간식확인", aliases=["간식 확인"])
async def snackcheck(ctx):
    with open("azzidata.json", "r") as file:
        data = json.load(file)
    snack = data["breakfast"]
    await ctx.send(f"아찌는 지금 간식을 {snack}개 정도 먹었어요!")

@bot.command(name="간식주기", aliases=["간식 주기"])
async def breakfast(ctx):
    with open("azzidata.json", "r") as file:
        data = json.load(file)
    with open("azzisnack.json", "r") as file:
        data1 = json.load(file)
    with open("azzisnackid.json", "r") as file:
        data2 = json.load(file)

    data["breakfast"] += 1

    if str(ctx.author.id) not in data1["snack_count"]:
        data1["snack_count"][str(ctx.author.id)] = 10

    if data1["snack_count"][str(ctx.author.id)] == 0:
        await ctx.send("아쉽지만 남은 간식을 다 준거 같네요! 간식은 매 정각마다 3개씩 들어와요!")
        return

    data1["snack_count"][str(ctx.author.id)] -= 1
    data2["snack_count"][str(ctx.author.id)] += 1

    with open("azzidata.json", "w") as file:
        json.dump(data, file)
    with open("azzisnack.json", "w") as file:
        json.dump(data1, file)
    with open("azzisnackid.json", "w") as file:
        json.dump(data2, file)
    embed = discord.Embed(title="훔냠냠!", color=GREEN_COLOR, description=f"아찌는 간식을 {data['breakfast']}번 먹었습니다!")
    await ctx.send(embed=embed)


command = ["아찌를 우리서버로 입양할래!", "아찌 공식 디스코드 서버로 놀러갈래!", "아찌의 소스코드가 궁굼해!"]
azzibotlink = "https://discord.com/api/oauth2/authorize?client_id=1020863208472444938&permissions=8&scope=bot"
azziserverlink = "https://discord.gg/bWysaCMFBm"
azzicodelink = "https://github.com/Jjoon0513/azzidiscord"

@bot.slash_command(description="아찌에 대한 링크들")
@option(name="link", description="무슨 링크가 필요하신가요?", type=str, required=True, choices=command)
async def 링크들(ctx, link: str):
    if link == "아찌를 우리서버로 입양할래!":
        button = Button(style=discord.ButtonStyle.link, label="여기 입양 절차 서류!", url=azzibotlink)
    elif link == "아찌 공식 디스코드 서버로 놀러갈래!":
        button = Button(style=discord.ButtonStyle.link, label="여기 우리 서버야!", url=azziserverlink)
    elif link == "아찌의 소스코드가 궁굼해!":
        button = Button(style=discord.ButtonStyle.link, label="여기 소스코드야!", url=azzicodelink)
    view = discord.ui.View()
    view.add_item(button)
    await ctx.respond("여기있어!", view=view)

async def reporter(user, userid, report):
    channelid = 1122895798783451167
    channel = bot.get_channel(channelid)
    await channel.send(f"- {user}({userid})님의 버그 리포트가 도착했어요!")
    await channel.send(f">>> {report}")
@bot.slash_command(name="버그리포트", description="버그리포트")
@option(name="report", description="무슨 버그가 있나요? (만약 장난일경우 심하면 밴!)", type=str, required=True)
async def report(ctx, report: str):
    username = ctx.user
    userid = ctx.user.id
    await reporter(username, userid, report)
    await ctx.respond("감사함니다! 검토해보고 수정하겠습니다!")

@bot.event
async def on_message(message):
    if message.content == "아찌야" or message.content == "아찌":
        await message.channel.send(random.choice(["왕 (넴)", "와왕! (네넵)", "왈 (넴)"]))

    elif int(message.author.id) in data["BanList"]:
        await message.channel.send("아르르르... (너에게서 나쁜냄새 난다!)")
    await bot.process_commands(message)


commmand1 = ["banlist", "adminlist"]
@bot.slash_command(description="appned Admin or Ban in List (dev only)")
@option(name="type", description="set ban or set admin", type=str, required=True, choices=commmand1)
@option(name="int", description="ID", type=str, required=True, choices=command)
async def appned(ctx, type: str, id: int):
    with open("azzidata.json", "r") as file:
        data = json.load(file)

    if int(ctx.author.id) not in data["AdminList"]:
        await ctx.respond("넌 주인이 아니잖아 아르르르르르르를")
        return None

    if type == "banlist":
        data["BanList"].append(id)
    elif type == "adminlist":
        data["AdminList"].append(id)

    with open("azzidata.json", "w") as file:
        json.dump(data, file)

    await ctx.respond(f"{type}에 {id}가 추가되었습니당")

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
