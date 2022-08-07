import asyncio
import random
import discord
from PIL import Image
import os
import numpy
from discord.ext import commands

le = 6
eleme = 9
# maximum option
# len 5 ele 5
# len 6 ele 4
# len 10 ele 3
# len 19 ele 2
reaction_list = ['\U00000030\U0000FE0F\U000020E3', '1️⃣', '2️⃣', '3️⃣', '\U00000034\U0000FE0F\U000020E3',
                 '\U00000035\U0000FE0F\U000020E3', '\U00000036\U0000FE0F\U000020E3', '\U00000037\U0000FE0F\U000020E3',
                 '\U00000038\U0000FE0F\U000020E3', '\U00000039\U0000FE0F\U000020E3']
number = ["０", "１", "２", "３", "４", "５", "６", "７", "８", "９"]
fragments = [-1, -2, -3, -4, -5, -6, -7, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
fdc = [12, 18, 13, 25, 19, 19, 14, 31, 25, 13, 19, 19]
pc = 1  #0은 가정용, 1은 노트북
path = ["C:/paolo/pibot/", "C:/yejun/python/discord/pi/"]
class ledder(commands.Cog, name="ledder"):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        count = 0

        def check(reaction,user):

            return user == message.author and  str(reaction.emoji) in reaction_list[1:count+1]

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
        await sendarray(message, content, num, "사다리타기\n",count)




        m2 = await message.channel.send("1~" + str(count) + "중 하나를 눌러주세요", reference=message)
        for i in reaction_list[1:count+1]:
            await m2.add_reaction(i)
        try:
            re = await self.client.wait_for(event='reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            await message.channel.send("시간이 지났습니다", reference=message)
            return

        ledderarray = numpy.array([line] * le)
        for i in range(1, le - 1):
            for hj in range(0, count - 1):
                ran = random.randrange(1, 3)  # 1,2
                if ran == 1:  # 4분의 1
                    ledderarray[i, hj * 3 + 2] = 1
                    ledderarray[i, hj * 3 + 3] = 1
        content = numpy.full((le, count * 3), fragments[0])
        # 맵 생성
        cnt = (int(reaction_list.index(str(re[0].emoji))) * 3) - 2
        i = 0
        j = cnt
        ab = True
        ii = []
        jj = []
        n = 0
        while True:
            if i == le - 1:
                ii.append(i)
                jj.append(j)
                n += 1
                break
            if ledderarray[i, (j + 1)] == 1:  # ↘
                ledderarray = xmove(ledderarray, i, j, 3)
                ii.append(i)
                jj.append(j)
                n += 1
                ii.append(i)
                jj.append(j + 1)
                n += 1
                ii.append(i)
                jj.append(j + 2)
                n += 1
                ii.append(i)
                jj.append(j + 3)
                n += 1
                content[i, j + 1] = 4
                content[i, j + 2] = 5
                j = j + 3
                ledderarray = ymove(ledderarray, i, j, 1)
                i = i + 1
            elif ledderarray[i, (j - 1)] == 1:
                ii.append(i)
                jj.append(j)
                n += 1
                ii.append(i)
                jj.append(j - 1)
                n += 1
                ii.append(i)
                jj.append(j - 2)
                n += 1

                content[i, j - 1] = 11
                content[i, j - 2] = 10
                ledderarray = xmove(ledderarray, i, j, -3)
                j = j - 3

            elif ledderarray[i + 1, j] == 1:
                ledderarray = ymove(ledderarray, i, j, 1)
                ii.append(i)
                jj.append(j)
                n += 1
                i = i + 1

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
                            continue
                            # content[i, j] = fragments[10]
                        elif ledderarray[0, j] == -1:  # 사다리 사이 두번째
                            continue
                            # content[i, j] = fragments[11]
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

        images = []
        a = 0
        # await sendarray(message=message, content=content, num=num, msg="사다리타기 결과\n")
        # region init
        new = Image.new("RGBA", ((count * 3 * 108), (le * 108)), 2000).convert('RGBA')
        for i in range(0, len(content)):
            for j in range(0, len(content[i])):
                if content[i][j] < 0:
                    img = Image.open(path[pc]+"image/image/black/" + str(content[i, j]) + ".png").convert('RGBA')
                else:
                    img = Image.open(path[pc]+"image/image/" + str(content[i, j]) + "/0.png").convert('RGBA')
                new.alpha_composite(img, ((j * 108), (i * 108)))
        # endregion
        a += 1
        images.append(new)
        for k in range(0, len(ii)):
            for n in range(0, fdc[content[ii[k], jj[k]]]):

                nn = images[a-1].copy()
                img = Image.open(path[pc]+"image/image/" + str(content[ii[k], jj[k]]) + "/" + str(n) + ".png").convert('RGBA')
                nn.alpha_composite(img, ((jj[k] * 108), (ii[k] * 108)))
                a += 1
                images.append(nn)


        for i in range(1,200):
            nn = images[a - 1].copy()
            images.append(nn)
        images[0].save(path[pc]+"image/cv2shape.gif", format='GIF',
                       append_images=images[1:],
                       save_all=True,
                       duration=32, loop=0)
        file = discord.File(path[pc]+"image/cv2shape.gif")
        await message.channel.send("결과", file=file)




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


async def sendarray(message, content, num, msg,count):
    # region pre
    new = Image.new("RGBA", ((count*3 *108), (3 * 108)), 2000).convert('RGBA')
    for i in range(0, len(content)):
        for j in range(0, len(content[i])):
            img = Image.open(path[pc] + "image/image/black/" + str(content[i, j]) + ".png").convert('RGBA')
            new.alpha_composite(img, ((j * 108), (i * 108)))
    new.save(path[pc]+"image/thumnail.png")
    file = discord.File(path[pc] + "image/thumnail.png")
    m1 = await message.channel.send(msg, file = file)
    return m1
    # endregion


def setup(client):
    client.add_cog(ledder(client))
