import discord
from discord.ext import commands
from discord.ext.audiorec import NativeVoiceClient  # important!
from pydub import AudioSegment
from secrets import token  # bot's secret token

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
    channel = ctx.voice_client.channel
    user = ctx.voice_client.user

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
