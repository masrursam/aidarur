import aiohttp
import asyncio
import json
import string
import random
from loguru import logger
import platform
import os

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear')

def printt(res):
    print(json.dumps(res, indent=4))

def random_int(length=10):
    return ''.join(random.choice('0123456789') for _ in range(length))

async def headers(token=''):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.6723.70 Safari/537.36',
        'Accept': '*/*',
        'Origin': 'https://my.aidapp.com',
        'Referer': 'https://my.aidapp.com/'
    }
    if token:
        header['Authorization'] = f'Bearer {token}'

    return header

async def create_wallet(session,kode_invite):
    url = f'https://back.aidapp.com/user-auth/login?strategy=WALLET&chainType=EVM&address=0x63dB5CAb3AaDDD3773fad8FB61FD44{random_int(10)}&token=MESSAGE_ETHEREUM_1740940044142:1740940044142&signature=0xc78864c879ecd9a5e9ac0add135ee0d23a91034e16482dab5d0025fe09f6dbea61382c379f2b9097b2a418fb0565bee22d1f2bb7f8a22dc83ffb59a6{random_int(10)}&inviter={kode_invite}'
    async with session.get(url, headers=await headers()) as res:
        try:
            req = await res.json()
            wallet = req['user']['evmAddress']
            token = req['tokens']['access_token']
            # print(f'wallet: {wallet}')
            # print(f'token: {token}')
            if token:
                await task(session,token)
                logger.success(f'wallet: {wallet} DONE')
        except Exception as e:
            logger.error('failed create account')

async def task(session,token):
    url = 'https://back.aidapp.com/questing/missions?filter%5Bdate%5D=2025-03-02T18:31:07.478Z&filter%5Bgrouped%5D=true&filter%5Bprogress%5D=true&filter%5Brewards%5D=true&filter%5Bstatus%5D=AVAILABLE&filter%5BcampaignId%5D=6b963d81-a8e9-4046-b14f-8454bc3e6eb2'
    async with session.get(url, headers=await headers(token=token)) as res:
        try:
            req = await res.json()
            tasks = req['data']
            for tugas in tasks:
                id_task = tugas['id']
                if tugas['id'] == 'f8edb0b4-ac7d-4a32-8522-65c5fb053725':
                    pass
                else:
                    await run_task(session,token,id_task)
        except Exception as e:
            logger.debug(e)

async def run_task(session,token,id_task):
    url = f'https://back.aidapp.com/questing/mission-activity/{id_task}'
    async with session.post(url,headers=await headers(token=token)) as res:
        try:
            await confirm_task(session,token,id_task)
        except Exception as e:
            logger.debug(e)

async def confirm_task(session,token,id_task):
    url = f'https://back.aidapp.com/questing/mission-reward/{id_task}'
    async with session.post(url,headers=await headers(token=token)) as req:
        try:
            # logger.success(await req.text())
            pass
        except Exception as e:
            logger.debug(e)

async def process():
    clear()
    kode_invite = input('masukan kode reff: ')
    #     kode_invite = 'RdJNTrPRiv_aNiT'
    loop = int(input('berapa reff: '))
    i=0
    while i < loop:
        async with aiohttp.ClientSession() as session:
            await create_wallet(session,kode_invite)
        i+=1

asyncio.run(process())