import discord
from discord.ext import commands
#import youtube_dl

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True

# Token de autenticação do bot 
TOKEN = "MTE2NDI4MjM4MjU2NDczMjk0OA.GxY1tH.krRJdzC2kuRzZMR4tW6_nXjtcU7rj"

# Crie uma instância do bot com as intenções definidas
bot = commands.Bot(command_prefix=">", case_insensitive = True ,intents=intents)

# Evento que é acionado quando o bot se conecta ao servidor
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    #logging.info(f'Bot conectado como {bot.user.name}')


@bot.command()
async def test(ctx):
    await ctx.send('Bot de testes ativo!')

# Inicie o bot
bot.run(TOKEN)

"""
@bot.command()
async def farm(ctx):
    author_nickname = ctx.author.nick if ctx.author.nick is not None else ctx.author.name
    category = discord.utils.get(ctx.guild.categories, name='farm')
    #await ctx.guild.create_text_channel(author_nickname, category=category)
    await ctx.message.delete()
    novo_canal = await ctx.guild.create_text_channel(author_nickname, category=category)
    mensagem_orientacao = f"Bem-vindo a sua aba de farm '{author_nickname}'! Você pode salvar seus comprovantes de farm aqui. \nOs responsáveis farão a conferência assim que possivel."
    await novo_canal.send(mensagem_orientacao)
    logging.info(f'COMMAND: FARM - {ctx.author}')

@bot.command()
async def play(ctx, url):
    channel = ctx.author.voice.channel
    if not channel:
        await ctx.send('Você precisa estar em um canal de voz para reproduzir áudio.')
        return

    voice_client = await channel.connect()
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        URL = info['formats'][0]['url']
        voice_client.play(discord.FFmpegPCMAudio(URL), after=lambda e: print('done', e))
    await ctx.send(f'Reproduzindo {url}')

@bot.command()
async def leave(ctx):
    voice_client = ctx.voice_client
    await voice_client.disconnect()"""

