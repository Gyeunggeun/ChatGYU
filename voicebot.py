import discord
from discord.ext import commands
from discord.ext.audiorec import NativeVoiceClient  # important!
from pydub import AudioSegment
from secrets import token  # bot's secret token

intents = discord.Intents().all()
client = commands.Bot(command_prefix="!", intents=intents)
client.remove_command('help')


@client.event
async def on_ready():
    print('im ready')


@client.command()
async def help(ctx):
    embedVar = discord.Embed(title="here are my commands!",
                             description="user **!join** to start the recording\nuser **!stop** to stop the recording", color=0x546e7a)
    await ctx.send(embed=embedVar)


@client.command()
async def join(ctx: commands.Context):
    channel: discord.VoiceChannel = ctx.author.voice.channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(channel)
    await channel.connect(cls=NativeVoiceClient)
    await ctx.invoke(client.get_command('rec'))


@client.command()
async def test(ctx):
    await ctx.send('hello im alive!')


@client.command()
async def rec(ctx):
    ctx.voice_client.record(lambda e: print(f"Exception: {e}"))
    embedVar = discord.Embed(title="Started the Recording!",
                             description="use !stop to stop!", color=0x546e7a)
    await ctx.send(embed=embedVar)


@client.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client.is_recording():
        return
    await ctx.send(f'Stopping the Recording')

    wav_bytes = await ctx.voice_client.stop_record()

    name = str(ctx.author.id) + '-' + str(ctx.message.id) + '.wav'
    with open(name, 'wb') as f:
        f.write(wav_bytes)
    await ctx.voice_client.disconnect()

    # Extract user's voice from the recorded file
    user_voice = AudioSegment.from_wav(name).set_channels(1)
    for member in ctx.author.voice.channel.members:
        if member != ctx.author:
            continue
        filename = str(member.id) + '-' + str(ctx.message.id) + '.wav'
        start = member.voice.state.start_time.timestamp() - ctx.message.created_at.timestamp()
        end = member.voice.state.end_time.timestamp() - ctx.message.created_at.timestamp()
        start = int(start * 1000)
        end = int(end * 1000)
        user_voice[start:end].export(filename, format='wav')

client.run(token)

@client.command()
async def stop(ctx: commands.Context):
    if not ctx.voice_client.is_recording():
        return
    await ctx.send(f'Stopping the Recording')

    # Stop recording and get the raw WAV bytes
    wav_bytes = await ctx.voice_client.stop_record()

    # Disconnect from the voice channel
    await ctx.voice_client.disconnect()

    # Get the channel and user specified in the join command
    channel = ctx.guild.get_channel(450458486656991234)
    user = ctx.guild.get_member(426350448694525952)

    # Load the recorded audio as a PyDub AudioSegment
    audio = AudioSegment.from_wav(io.BytesIO(wav_bytes))

    # Extract the audio of the specified user
    user_voice = audio.filter_by_user(user.id, channel=channel.id)

    # Export the extracted audio as a WAV file
    filename = f'{user.name}_{user.id}_{channel.name}_{channel.id}.wav'
    user_voice.export(filename, format='wav')

    # Send the extracted audio file to the user
    with open(filename, 'rb') as f:
        await user.send(file=discord.File(f))

