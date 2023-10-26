import discord
from discord.ext import commands
#from discord_components import DiscordComponents, Button, ButtonStyle
import asyncio
import logging
import datetime

#import youtube_dl
#from discord_slash import SlashCommand
#from discord.ext import voice

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.members = True
intents.message_content = True

# Token de autenticação do bot 
TOKEN = ""

#configuração do arquivo de .log
logging.basicConfig(filename='massaricobot.log', level=logging.INFO,
                    format='%(asctime)s:%(levelname)s:%(message)s')

#Crie uma instância do bot com as intenções definidas
bot = commands.Bot(command_prefix=">", case_insensitive = True ,intents=intents)
"""DiscordComponents(bot)"""
last_member = None

# Evento que é acionado quando o bot se conecta ao servidor
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user.name}')
    logging.info(f'Bot conectado como {bot.user.name}')

#evento - ao membro entrar no discord
@bot.event
async def on_member_join(member):
    mensagem_privada = f"Bem-vindo aos VERMELHOS, {member.name}! Esperamos que você se divirta conosco, de uma olhada nas #REGRAS."
    await member.send(mensagem_privada)

    canal_bem_vindos = discord.utils.get(member.guild.channels, name="📢│ʙᴇᴍ-ᴠɪɴᴅᴏs")
    if canal_bem_vindos is not None:
        mensagem_canal = f"Bem-vindo, {member.name}! Leia as regras em #regras e divirta-se!"
        await canal_bem_vindos.send(mensagem_canal)

    canal_pedido = discord.utils.get(member.guild.channels, name="✅│ᴘᴇᴅɪʀ-sᴇᴛ")
    if canal_pedido is not None:
        mensagem_canal = f"{member.mention}, favor preencher o formulário para receber as permissões necessárias.\nNome: \nId: \nApelido: \nTel: \nRecrutador: @" 
        await canal_pedido.send(mensagem_canal)


#evento - ao membro sair do discord
@bot.event
async def on_member_remove(member):
    canal_saida = discord.utils.get(member.guild.channels, name="❌│ǫᴜɪᴛ-sᴇʀᴠᴇʀ")
    if canal_saida is not None:
        mensagem_canal = f"O vacilão(a) {member.mention} rodou, casa caiu."
        await canal_saida.send(mensagem_canal)

    user1 = bot.get_user("""02""")  
    user2 = bot.get_user("""01""")

    if user1 is not None:#caixa
        mensagem_user1 = f"Eae meu 02! usuário {member.name} saiu do servidor, verifique no painel da FAC se está ativo ainda."
        await user1.send(mensagem_user1)

    if user2 is not None:#tchulla
        mensagem_user2 = f"Eae meu 01! usuário {member.name} saiu do servidor, verifique no painel da FAC se está ativo ainda."
        await user2.send(mensagem_user2)

@bot.event
async def on_member_join(member):
    global last_member
    last_member = member
    #print(f'Último membro a entrar: {member.name}')

@bot.event
async def on_message(message):
    if message.author.id == 0000:  # Substitua SEU_ID_DE_USUARIO pelo ID do usuário específico
        emoji = '\U0001F308'  # Emoji de arco-íris
        await message.add_reaction(emoji)
    await bot.process_commands(message)

# Comandos

#clona a mensagem da pessoa e envia como se fosse o bot falando 
@bot.command()
async def m(ctx):
    content = ' '.join(ctx.message.content.split(' ')[1:])  # Exclui a primeira palavra do comando
    await ctx.message.delete()  # Deleta a mensagem original
    await ctx.send(content)  # Envia o conteúdo copiado de volta para o canal
    logging.info(f'COMMAND: NOTE - {ctx.author.nick}')

#limpa o canal de voz (APAGA TUDO) usar com sabedoria.
@bot.command()
async def limpar(ctx):
    await ctx.channel.purge()

#lista os comandos do Massarico bot
@bot.command()
async def comandos(ctx):
    await ctx.send(f'Olá {ctx.author.nick}, esses são os comandos: \n >massarico: Descobre ai.\n >note: escreve a mensagem que quiser (como se fosse o bot). \n >versao: Versão do bot. \n >info: Descrição para a aba de abertura de farm. \n >farm: Abre a aba der farm. \n Existe outros comandos ocultos também rsrs')
    await ctx.message.delete()
    logging.info(f'COMMAND: COMANDOS - {ctx.author.nick}')

#é massarico
@bot.command()
async def massarico(ctx):
    await ctx.message.delete()
    await ctx.send(f'Olá {ctx.author.nick}, esse é o BOT oficial dos Vermelhos! author: Jhon')
    logging.info(f'COMMAND: MASSARICO - {ctx.author.nick}')

#versão para informação
@bot.command()
async def versao(ctx):
    await ctx.message.delete()
    await ctx.send(f'Olá {ctx.author.mention}, versão 1.5.7 - author: @c.jhonat4n')
    logging.info(f'COMMAND: VERSAO - {ctx.author.nick}')

#mensagem inicial que fica na aba de abertura de farm
@bot.command()
async def info(ctx):
    await ctx.send(f'Olá, para abrir sua aba de farm, insira o comando: >farm')
    await ctx.message.delete()
    logging.info(f'COMMAND: INFO - {ctx.author.nick}')

#para abrir o canal de farm
@bot.command()
async def farm(ctx):
    author_nickname = ctx.author.nick if ctx.author.nick is not None else ctx.author.name
    category = discord.utils.get(ctx.guild.categories, name='farm')
    overwrites_private = None
    for channel in ctx.guild.channels:  # Procura por um canal com configurações de permissões específicas
        if channel.name == '💬│ᴄʜᴀᴛ-ɢᴇʀᴇɴᴄɪᴀ':
            overwrites_private = channel.overwrites
    if overwrites_private is not None:
        overwrites_private[ctx.author] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
    await ctx.message.delete()
    novo_canal = await ctx.guild.create_text_channel(author_nickname, category=category, overwrites=overwrites_private)
    mensagem_orientacao = f"Bem-vindo a sua aba de farm, {ctx.author.mention}! Você pode salvar seus comprovantes de farm aqui. \nOs responsáveis farão a conferência assim que possível."
    await novo_canal.send(mensagem_orientacao)
    logging.info(f'COMMAND: FARM - {ctx.author.nick}')

#para pedir set automação
@bot.command()
async def set(ctx):
    global last_member
    await ctx.message.delete()
    if last_member is not None:
        await ctx.send(f"{last_member.mention}, favor preencher o formulário para receber as permissões necessárias.\nNome: \nId: \nApelido: \nTel: \nRecrutador: @{ctx.author} ")
    else:
        await ctx.send(f"Calabreso, favor preencher o formulário para receber as permissões necessárias.\nNome: \nId: \nApelido: \nTel: \nRecrutador: @{ctx.author} ")

#faz a baguncinha no canal de voz
@bot.command()
async def banv(ctx, apelido):
    await ctx.message.delete()
    voice_channel = ctx.author.voice.channel
    logging.info(f'COMMAND: BANV - {ctx.author}')

    if not voice_channel:
        await ctx.send("Você não está em um canal de voz.")
        return
    member_to_disconnect = discord.utils.get(voice_channel.members, nick=apelido)

    if not member_to_disconnect:
        await ctx.send(f"'{apelido}' não encontrado em '{voice_channel.name}'.")
        return
    await member_to_disconnect.move_to(None)
    #await ctx.send(f"'{apelido}' desconectado de '{voice_channel.name}'.")

# Comando para desconectar todos os membros do canal de voz do autor
@bot.command()
async def banido(ctx):
    logging.info(f'BANIDO {ctx.author}')
    await ctx.message.delete()
    author = ctx.author
    voice_state = author.voice
    if voice_state and voice_state.channel:
        # Verifique se o autor está em um canal de voz
        voice_channel = voice_state.channel
        #voice_client = await voice_channel.connect()
        #voice_client.play(discord.FFmpegPCMAudio('banido.mp3'))
        
        # Aguardar até que o áudio seja reproduzido
        #while voice_client.is_playing():
        #    await asyncio.sleep(1)

        #Desconectar o bot após a reprodução do áudio
        #    voice_client.stop()
        #await voice_client.disconnect()

        for member in voice_channel.members:
            # Itera sobre os membros do canal de voz
            await member.move_to(None)

        #await ctx.send(f"Todos os membros foram desconectados do canal de voz '{voice_channel.name}'.") #MENSAGEM DE OK
    #else:
        #await ctx.send("Você não está em um canal de voz ou o bot não tem permissão para desconectar membros.") #MENSAGEM DE ERRO

# Comando para tocar musica #implementar#
@bot.command()
async def p(ctx):
    await ctx.send(f"Desculpe, {ctx.author.mention} ainda não tô lançando a braba, mas em breve vou estar! 🎶 Me aguarde!")

#teste de ponto - não funcional ainda
service_started = None
service_paused = None
total_pause_duration = datetime.timedelta(0)

@bot.command()
async def start(ctx):
    global service_started
    service_started = datetime.datetime.now()
    await ctx.send(f"Registro de entrada: {service_started}")

@bot.command()
async def pause(ctx):
    global service_paused, service_started, total_pause_duration
    service_paused = datetime.datetime.now()
    await ctx.send(f"Registro de pausa: {service_paused}")
    total_pause_duration += service_paused - service_started

@bot.command()
async def resume(ctx):
    global service_started, service_paused
    service_started = datetime.datetime.now()
    await ctx.send(f"Retorno do modo de pausa: {service_started}")

@bot.command()
async def end(ctx):
    global total_pause_duration
    service_ended = datetime.datetime.now()
    time_in_service = service_ended - service_started - total_pause_duration
    await ctx.send(f"Registro de saída: {service_ended}, Tempo em serviço (excluindo pausas): {time_in_service}")

@bot.command()
async def buttons(ctx):
    await ctx.send(
        "Selecione uma opção:",
        components=[
            discord.ui.Button(style=discord.ButtonStyle.green, label="Iniciar"),
            discord.ui.Button(style=discord.ButtonStyle.red, label="Pausa"),
            discord.ui.Button(style=discord.ButtonStyle.green, label="Retomar"),
            discord.ui.Button(style=discord.ButtonStyle.grey, label="Finalizar"),
        ]
    )

@bot.event
async def on_button_click(interaction):
    if interaction.component.custom_id == "start":
        await start(interaction)
    elif interaction.component.custom_id == "pause":
        await pause(interaction)
    elif interaction.component.custom_id == "resume":
        await resume(interaction)
    elif interaction.component.custom_id == "end":
        await end(interaction)

# Inicie o bot
bot.run(TOKEN)