import os
import tempfile
import azure.cognitiveservices.speech as speechsdk
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters, CommandHandler
from config import AZURE_SPEECH_KEY, AZURE_REGION, TELEGRAM_BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Send me any text and I’ll reply with a voice message using Azure TTS.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        await update.message.reply_text("Please send some text.")
        return

    # Clean and validate the key and region
    key = AZURE_SPEECH_KEY.strip()
    region = AZURE_REGION.strip()

    try:
        # Azure Speech SDK setup
        speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
        speech_config.set_speech_synthesis_output_format(
            speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
        )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            audio_path = f.name

        audio_config = speechsdk.AudioConfig(filename=audio_path)
        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config
        )
        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            await update.message.reply_voice(voice=open(audio_path, 'rb'))
        else:
            await update.message.reply_text("TTS synthesis failed.")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")
    finally:
        if 'audio_path' in locals() and os.path.exists(audio_path):
            os.remove(audio_path)

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
