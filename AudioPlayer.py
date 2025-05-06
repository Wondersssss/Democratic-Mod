import os
import discord
import asyncio

async def playAudio(file: str, vc: discord.VoiceClient, interaction: discord.Interaction) -> discord.VoiceClient:
    """Optimized WAV audio playback with robust error handling"""
    try:
        # Verify the WAV file exists
        if not os.path.exists(file):
            raise FileNotFoundError(f"WAV file not found: {os.path.abspath(file)}")
        
        # Validate WAV file header
        if not await validate_wav_file(file):
            raise ValueError("Invalid WAV file format")

        # Configure FFmpeg specifically for WAV
        ffmpeg_options = {
            'options': '-ac 2 -ar 48000 -loglevel warning',
            'before_options': '-guess_layout_max 0'  # Better channel handling
        }

        # Create audio source with WAV-specific settings
        audio_source = discord.FFmpegPCMAudio(
            executable="ffmpeg",
            source=file,
            **ffmpeg_options
        )

        # Apply safe volume level
        audio = discord.PCMVolumeTransformer(audio_source, volume=0.8)

        def after_play(error):
            if error:
                print(f"WAV playback error: {error}")
                asyncio.create_task(
                    interaction.followup.send("Error playing WAV audio", ephemeral=True)
                )

        # Ensure clean playback state
        if vc.is_playing():
            vc.stop()

        vc.play(audio, after=after_play)
        print(f"Playing WAV file: {os.path.basename(file)}")
        return vc

    except Exception as e:
        print(f"WAV processing failed: {type(e).__name__}: {e}")
        await cleanup_voice(vc)
        raise RuntimeError(f"WAV playback error: {e}") from e

async def validate_wav_file(file_path: str) -> bool:
    """Validate basic WAV file structure"""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(12)
            if header[0:4] != b'RIFF' or header[8:12] != b'WAVE':
                return False
            return True
    except Exception:
        return False

async def cleanup_voice(vc: discord.VoiceClient):
    """Safely disconnect from voice channel"""
    try:
        if vc and vc.is_connected():
            await vc.disconnect()
            print("Voice connection cleaned up")
    except Exception as e:
        print(f"Voice cleanup error: {e}")
async def cleanup_voice(vc: discord.VoiceClient) -> None:
    """Safely disconnect from voice channel"""
    try:
        if vc and vc.is_connected():
            await vc.disconnect()
            print("Disconnected from voice channel")
    except Exception as e:
        print(f"Error during voice cleanup: {e}")