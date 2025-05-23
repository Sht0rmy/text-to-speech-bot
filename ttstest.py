import os
import azure.cognitiveservices.speech as speechsdk

speech_key = "8XzIAGbE98S265cp8bc4jz02RuK0nERUTNv8MoSTCdw3p9PqP9SoJQQJ99BEAC5RqLJXJ3w3AAAYACOG5TBh".strip()
region = "https://westeurope.api.cognitive.microsoft.com".strip()

# This example requires environment variables named "SPEECH_KEY" and "ENDPOINT"
# Replace with your own subscription key and endpoint, the endpoint is like : "https://YourServiceRegion.api.cognitive.microsoft.com"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=region)
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

# The neural multilingual voice can speak different languages based on the input text.
speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Get text from the console and synthesize to the default speaker.
print("Enter some text that you want to speak >")
text = input()

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

