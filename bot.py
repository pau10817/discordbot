import discord
from discord.ext.commands import Bot
from discord.ext import commands
import requests as rq
from bs4 import BeautifulSoup as bs

# 디스코드 클라이언트를 생성합니다.
Client = discord.Client()
client = commands.Bot(command_prefix=None)

# 디소코드 봇 시작시 봇의 name과 id를 출력합니다.
@client.event
async def on_ready():
    print("Bot Online!")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.event
async def on_message(message):
    if message.content.startswith('!message'):  # 디스코드에서 입력된 문자열이 !message로 시작하는지 체크합니다.
        counter = 0
        # 메세지를 입력받은 채널로 메세지를 전송합니다.
        tmp = await client.send_message(message.channel, '최근 100개의 메시지를 체크중입니다...')
        # 최근 백개의 메시지의 로그를 확인합니다.
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:    # 백개의 메시지 중에서 명령어를 입력한 유저의 메시지 개수를 셉니다.
                counter += 1
        await client.edit_message(tmp, '너의 메시지는 {}개 입니다.'.format(counter))  # 보냈던 메시지를 수정하여 메시지 개수를 전송합니다.

    elif message.content.startswith('!실시간'):    # 디스코드에서 입력된 문자열이 !실시간으로 시작하는지 체크합니다.
        # 11월 18일자 requests를 이용한 네이버 실시간 검색어 출력 코드입니다.
        content = ''
        req = rq.get("https://datalab.naver.com")
        html = req.text
        soup = bs(html, 'html.parser')

        keyword_rank = soup.find('div', {'class':'rank_inner v2'})
        date = keyword_rank.find('strong', {'class':'rank_title v2'}).text
        rank = keyword_rank.find_all('a', {'class':'list_area'})

        content += date + '\r\n'
        for l in rank:
            number = l.find('em').text
            keyword = l.find('span').text
            content += number + " " + keyword + '\r\n'
        await client.send_message(message.channel, content)

    elif message.content.startswith('!test'):
            content = message.content.split()
            print(content)
            await client.send_message(message.channel, content[1])

client.run('MzgzNzk1MzcyODMwNDkwNjU2.DPpfXA.Rp3RpxQBexipqbb2cCh4R5WLXvs')
