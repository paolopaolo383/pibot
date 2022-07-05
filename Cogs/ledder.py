import asyncio
import random
import async_timeout
from unicodedata import name
import discord
from discord.ext import commands
import json
import numpy

le = 6
eleme = 5
# maximum option
# len 5 ele 5
# len 6 ele 4
# len 10 ele 3
# len 19 ele 2
reaction_list = ['\U00000030\U0000FE0F\U000020E3', '1️⃣', '2️⃣', '3️⃣', '\U00000034\U0000FE0F\U000020E3',
                 '\U00000035\U0000FE0F\U000020E3', '\U00000036\U0000FE0F\U000020E3', '\U00000037\U0000FE0F\U000020E3',
                 '\U00000038\U0000FE0F\U000020E3', '\U00000039\U0000FE0F\U000020E3']
number = ["０", "１", "２", "３", "４", "５", "６", "７", "８", "９"]
fragments = ["<:0_:990543928208015381>", "<:1_:990543929973805076>", "<:3_:990543933224402964>",
             "<:4_:990543934843387955>", "<:5_:990543937028628510>", "<:6_:990543938710569020>",
             "<:7_:990543940291817502>", "<:c1:990619679523471462>", "<:c2:990619681436074044>",
             "<:c3:990619683252219914>", "<:c4:990619684736999446>", "<:c5:990619686142107709>",
             "<:c6:990619688054714462>", "<:c7:990619689925378068>", "<:c8:990619691624067104>",
             "<:c9:990619693192740864>", "<:c0:993799593890431047>"]






class ledder(commands.Cog, name="ledder"):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        count = 0

        def check(msg):
            count = int(message.content.split(" ")[1])
            try:
                if message.author.id == msg.author.id and int(msg.content) > 0 and int(
                        msg.content) < count + 1 and message.channel.id == msg.channel.id:
                    return True
                else:
                    return False
            except ValueError:
                return False

        x = 0
        y = 0
        ledderarray = numpy.array([])
        line = []
        num = []
        col = []
        if message.content.startswith("사다리타기"):
            if len(message.content.split(" ")) == 2:
                try:
                    if int(message.content.split(" ")[1]) > 1 and int(message.content.split(" ")[1]) < eleme + 1:
                        count = int(message.content.split(" ")[1])
                        for i in range(1, count + 1):
                            line.append(-1)
                            line.append(1)
                            line.append(0)
                            col.append(fragments[0])
                            col.append(fragments[1])
                            col.append(fragments[0])
                            num.append(fragments[0])
                            num.append(reaction_list[i])
                            num.append(fragments[0])
                    else:
                        return
                except ValueError:
                    return

            else:
                return

        else:
            return

        ledderarray = numpy.array([line, line, line])

        # print

        content = numpy.array([col, col, col])
        leddermsg = await sendarray(message, content, num, "사다리타기\n")
        await message.channel.send("1~" + str(count) + "중 하나를 입력해주세요", reference=message)
        try:
            re = await self.client.wait_for(event='message', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send("시간이 지났습니다", reference=message)
            return

        ledderarray = numpy.array([line] * le)
        for i in range(1, le - 1):
            for hj in range(0, count - 1):
                ran = random.randrange(1, 3)  # 1,4
                if ran == 1:  # 4분의 1
                    ledderarray[i, hj * 3 + 2] = 1
                    ledderarray[i, hj * 3 + 3] = 1

        # 맵 생성
        cnt = (int(re.content) * 3) - 2
        i = 0
        j = cnt
        ab = True
        while True:
            if i == le - 1:
                break
            if ledderarray[i, (j + 1)] == 1:  # ↘
                ledderarray = xmove(ledderarray, i, j, 3)
                j = j + 3
                ledderarray = ymove(ledderarray, i, j, 1)
                i = i + 1
            elif ledderarray[i, (j - 1)] == 1:
                ledderarray = xmove(ledderarray, i, j, -3)
                j = j - 3

            elif ledderarray[i + 1, j] == 1:
                ledderarray = ymove(ledderarray, i, j, 1)
                i = i + 1

        content = numpy.full((le, count * 3), fragments[0])
        for i in range(0, le):
            for j in range(0, count * 3):
                if ledderarray[i, j] > 0:

                    if ledderarray[i, j] == 1:  # 안지나간 부분
                        if i == 0 or i == le - 1:
                            content[i, j] = fragments[1]
                        elif ledderarray[0, j] == 0:  # 사다리 사이 첫번째
                            content[i, j] = fragments[4]
                        elif ledderarray[0, j] == -1:  # 사다리 사이 두번째
                            content[i, j] = fragments[5]
                        else:  # 길
                            if ledderarray[i, j + 1] == 1 and ledderarray[i, j - 1] == 1:  # 위 양옆
                                content[i, j] = fragments[6]
                            elif ledderarray[i, j + 1] == 1:  # 오른쪽이랑 아래
                                content[i, j] = fragments[2]
                            elif ledderarray[i, j - 1] == 1:  # 왼쪽이랑 아래
                                content[i, j] = fragments[3]
                            else:  # 아래로만
                                content[i, j] = fragments[1]


                    elif ledderarray[i, j] == 2:
                        if i == 0 or i == le - 1:
                            content[i, j] = fragments[7]

                        elif ledderarray[0, j] == 0:  # 사다리 사이 첫번째
                            content[i, j] = fragments[10]
                        elif ledderarray[0, j] == -1:  # 사다리 사이 두번째
                            content[i, j] = fragments[11]
                        else:  # 길일때
                            if ledderarray[i, j + 1] > 0 and ledderarray[i, j - 1] > 0:  # 위 양옆
                                if ledderarray[i, j - 1] == 2 and ledderarray[i, j + 1] == 2:
                                    content[i, j] = fragments[13]
                                elif ledderarray[i, j - 1] == 2:
                                    content[i, j] = fragments[16]
                                else:
                                    content[i, j] = fragments[12]
                            elif ledderarray[i, j + 1] > 0 and not ledderarray[i, j - 1] > 0:  # 오른쪽
                                if ledderarray[i + 1, j] == 2:
                                    if ledderarray[i - 1, j] == 2:
                                        if content[i - 1, j] == fragments[8] or content[i - 1, j] == fragments[12]:
                                            content[i, j] = fragments[14]
                                        else:
                                            content[i, j] = fragments[8]
                                    else:
                                        content[i, j] = fragments[14]
                                else:
                                    content[i, j] = fragments[8]

                            elif not ledderarray[i, j + 1] > 0 and ledderarray[i, j - 1] > 0:  # 왼쪽
                                if ledderarray[i + 1, j] == 2:
                                    if ledderarray[i - 1, j] == 2:
                                        if content[i - 1, j] == fragments[9] or content[i - 1, j] == fragments[13]:  # c7도
                                            content[i, j] = fragments[15]
                                        else:
                                            content[i, j] = fragments[9]
                                    else:
                                        content[i, j] = fragments[15]
                                else:
                                    content[i, j] = fragments[9]
                            else:  # 아래로만
                                content[i, j] = fragments[7]

        await sendarray(message=message, content=content, num=num, msg="사다리타기 결과\n")


def xmove(array, i, j, num):
    if num < 0:
        for k in range(0, -1 * num + 1):
            array[i, j - k] = 2
    else:
        for k in range(0, num + 1):
            array[i, j + k] = 2
    return array


def ymove(array, i, j, num):
    for k in range(0, num + 1):
        array[i + k, j] = 2
    return array


async def sendarray(message, content, num, msg):
    for ele in range(len(num)):
        if not ele == 0 and not ele == (len(num) - 1):
            msg = msg + num[ele]
    for i in range(len(content)):
        msg = msg + "\n"
        for j in range(len(content[i])):
            if not j == 0 and not j == (len(content[i]) - 1):
                msg = msg + content[i, j]
    msg = msg + "\n"
    for ele in range(len(num)):
        if not ele == 0 and not ele == (len(num) - 1):
            msg = msg + num[ele]
    await message.channel.send(msg, reference=message)
    return msg


def setup(client):
    client.add_cog(ledder(client))
