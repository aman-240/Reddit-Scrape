import discord
import os
import threading
import time
import requests
import aiohttp
import asyncio
from discord.ext import commands
from reddit_scrape import RedditPost
from mongoRUN import GuildData

my_secret = '<BOT SECRET>'

intents = discord.Intents().all()
client = commands.Bot(intents=intents, command_prefix='!')
url = "https://www.reddit.com/r/marvelmemes/new/"
my_cookies = 'loid=0000000000eumj97lp.2.1632678874000.Z0FBQUFBQmhVTFBhbEN3SXpsekhNb2hNNU9pYzFGUFE3aFdFSGhFWFhTZ2Vad1lFOEJlSENDVFJoekkxTnVFSjA2eFpQSER3LXVRZGxhQkFINkljcnowSXNVdnZMNE5NZTdndElyeENQT0E1SXdveXJQUGNyQlppMWhiQk9ORVZPZmF0T2pxbS03RDI; token_v2=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NzQzNjI4ODEsInN1YiI6IjExNjM3NjQzNjU3NTctNG00Vl9XSnFhekNXTmxtaHBobk9QVzF4XzN1RldnIiwibG9nZ2VkSW4iOnRydWUsInNjb3BlcyI6WyIqIiwiZW1haWwiLCJwaWkiXX0.bUhAD5bS4kip_-gIR291lCLoXVzeqfag2dxmAgt5xU8; csv=2; edgebucket=mJwRppYILrOV8gGFzt; recent_srs=t5_35mye%2Ct5_2vm97%2Ct5_2qh22%2Ct5_2qh3k%2Ct5_gawb2%2Ct5_39d7x%2Ct5_3erjs%2Ct5_388p4%2Ct5_2risk%2Ct5_2slr8; G_ENABLED_IDPS=google; session_tracker=ermjrnjkhnadkrprrl.0.1674276967627.Z0FBQUFBQmp5M0JuSnY2YU5TdGhiM3Ffd3EtaVh5a3dGTHczN2tnVTN3YzR6Vm5TRlZPY2JmOVNacTh6d3BoZ2lwTDE5QXJjUmJfZlJTemdfSjlMYUhYRURqdDREbmlHdzdyVUV1SktSQjlfM010S2hrWmlQQWRMRVZDUjlZSlM0V2lWeHg1NEJnS0k; session=77e0e6861022e7df473678c7a0832ff0de75cbc1gAWVSQAAAAAAAABKTnDLY0dB2PLZ5IinX32UjAdfY3NyZnRflIwoNDhkMDk1N2I0MTkwNGIwNjM4YTNlY2FhZGVhNzJhMjUwMjQzYzdiZZRzh5Qu; pc=9t; USER=eyJwcmVmcyI6eyJ0b3BDb250ZW50VGltZXNEaXNtaXNzZWQiOjAsImNvbGxhcHNlZFRyYXlTZWN0aW9ucyI6eyJmYXZvcml0ZXMiOmZhbHNlLCJtdWx0aXMiOmZhbHNlLCJtb2RlcmF0aW5nIjpmYWxzZSwic3Vic2NyaXB0aW9ucyI6ZmFsc2UsInByb2ZpbGVzIjpmYWxzZX0sIm5pZ2h0bW9kZSI6dHJ1ZSwiZ2xvYmFsVGhlbWUiOiJSRURESVQiLCJ0b3BDb250ZW50RGlzbWlzc2FsVGltZSI6bnVsbH19; g_state={"i_l":0}; reddit_session=1163764365757%2C2023-01-21T04%3A50%3A01%2C2e50f9ac3518d0f6992f8386c5c1ab812ae8b2ea; session_tracker=ermjrnjkhnadkrprrl.0.1674277625570.Z0FBQUFBQmp5M0w1Nmkzc21CVllKdmRLZzlfOUIwa0EtTGRGOVNDNXdHWXc2LUVncnRibktkVlF3WjJoTVBEQUdwbzlGUUlCbkczYkw0RVlGSGJNRHRvYjRnbF9sQ0Vna29EMTJ0ZTh6eGVaZ013NG44MDh3SkVpV3ZHeWplcmlZeXM0YkpudDU1QlI'
my_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0'
headers = {
    'User-Agent': my_user_agent,
    'Accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Connection': 'keep-alive',
    'Cookie': my_cookies,
    'TE': 'trailers'
}


def send_embed(url, image_url, timestamp, meme_title):
    split_array = url.split("/")
    r_index = split_array.index("r")
    name_of_subreddit = split_array[r_index + 1]
    send_embed = discord.Embed(title=name_of_subreddit,
                               description='',
                               color=0xff4500,
                               url=url)
    send_embed.add_field(
        name="Meme Title", value=f"`{meme_title}`", inline=True)
    send_embed.add_field(
        name="Time Stamp", value=f"`{timestamp}`", inline=True)
    send_embed.set_image(url=image_url)
    return send_embed


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    
@client.command()
async def start(ctx):
    global task
    task = client.loop.create_task(redditScrape())
    await ctx.reply("Fetching Subreddit Content...")

@client.command()
async def stop(ctx):
    task.cancel()
    await ctx.reply("Stopped Fetching Subreddit Content...")

def fetch_data(session, urls):
    task = []
    for url_ in urls:        
        task.append(session.get(url=url_, headers=headers))
    return task

async def redditScrape():
    while True:
        for guild in client.guilds:
            guild_data = GuildData(guild.id)
            if guild_data.find_guild_data():
                reddit_url = guild_data.fetch_reddit_urls()
                async with aiohttp.ClientSession() as session:
                    results = await asyncio.gather(*fetch_data(session, reddit_url))
                    for i, result in enumerate(results):
                        response_dict = RedditPost(url=url).post_info(html_file=await result.text())
                        if response_dict == False:
                            pass
                        else:
                            if RedditPost.check_repeat(reddit_url=reddit_url[i],image_url=response_dict['Image URL'],guild_id=guild.id):
                                pass
                            else:
                                RedditPost.update_reddit_data(reddit_url=reddit_url[i],image_url=response_dict['Image URL'],guild_id=guild.id)
                                channel_id = GuildData(
                                    guild.id).find_channel_id(guild.id)
                                await client.get_channel(channel_id).send(
                                    embed=send_embed(url=reddit_url[i],
                                                    image_url=response_dict['Image URL'],
                                                    timestamp=response_dict['Timestamp'],
                                                    meme_title=response_dict['Title']))
        await asyncio.sleep(15)


@client.command()
@commands.has_permissions(administrator=True)
async def dru(ctx, reddit_url):
    guild_data = GuildData(ctx.guild.id)
    if guild_data.find_guild_data():
        guild_data.delete_reddit_url(reddit_url)
        guild_data.delete_reddit_data(reddit_url)
        await ctx.reply(
            f"Deleted the reddit url from the database: `{reddit_url}`")
    else:
        await ctx.reply("No data found in the database")


# add the reddit url to the database
@client.command()
@commands.has_permissions(administrator=True)
async def aru(ctx, reddit_url):
    guild_data = GuildData(ctx.guild.id)
    numLinks = len(guild_data.fetch_reddit_urls())
    checkChannel = guild_data.find_channel_id(ctx.guild.id)
    if checkChannel is not None: #Check if channel exists
        if numLinks >= 3:
            await ctx.reply("You can only have 3 links per server")
            return
        else:
            if guild_data.find_guild_data():
                guild_data.update_guild_data(reddit_url, ctx.channel.id)
                guild_data.update_in_insert(reddit_url=reddit_url)
                await ctx.reply(
                    f"Updated the reddit url to the database: `{reddit_url}`")
            else:
                guild_data.insert_guild_data(reddit_url, ctx.channel.id)
                guild_data.insert_reddit_data(reddit_url=reddit_url, image_url="")
                await ctx.reply(
                    f"Added the reddit url to the database: `{reddit_url}`")

   
# show the reddit url from the database
@client.command()
@commands.has_permissions(administrator=True)
async def sru(ctx):
    guild_data = GuildData(ctx.guild.id)
    if guild_data.find_guild_data():
        reddit_url = guild_data.fetch_reddit_urls()
        await ctx.reply(f"Reddit url from the database: `{reddit_url}`")
    else:
        await ctx.reply("No data found in the database")

def ratelimit_checker():
    while True:
        time.sleep(60)
        res = requests.get('https://discord.com/api/v6/users/@me',
                           headers={'Authorization': f'Bot {my_secret}'})
        print(res.text)
        if res.status_code == 200:
            pass
        else:
            os.system('kill 1')


def count():
    while True:
        print("I am alive")
        time.sleep(3)
    

threading.Thread(target=ratelimit_checker).start()
threading.Thread(target=count).start()
client.run(my_secret)