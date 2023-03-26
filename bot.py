import discord
from gyugyu import TOKEN

macro_dict = {
    1: "아 억까야",
    2: "로아도 안하는 새끼가",
    3: "그런 사람 아닙니다~",
    4: "인생 망했어",
    5: "나 말 안해",
    6: "빠큐 빠큐",
    7: "나 섭섭해",
    8: "해줘",
    9: "응애",
    10: "각성기~ (빗나감)",
    11: "아 씨발 못 박았어 아 인생 좆망했어"
}


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        await self.change_presence(status=discord.Status.online, activity=discord.Game("카던"))

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == '!상규야 꺼져':
            await message.channel.send('상규 꿈 꿔~')
            await self.close()
            return

        if message.content == '!상규야':
            # 매크로 목록 출력
            macro_list = '\n'.join([f"{key}: {value}" for key, value in macro_dict.items()])
            response = f"매크로 목록:\n{macro_list}"
            await message.channel.send(response)
        elif message.content.startswith('!상규야 '):
            try:
                # 매크로 번호 추출 및 해당 매크로 전송
                macro_num = int(message.content[5:])
                response = macro_dict[macro_num]
                await message.channel.send(response)
            except ValueError:
                # 매크로 번호가 정수형이 아닌 경우 예외 처리
                await message.channel.send("아 억까 좀 그만 해")
            except KeyError:
                # 매크로 번호가 매크로 목록에 없는 경우 예외 처리
                await message.channel.send("없어 새끼야")


intents = discord.Intents.default()
intents.messages = True
client = MyClient(intents=intents)
client.run(TOKEN)

