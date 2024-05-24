#import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./voiceAccountKey.json"

#export GOOGLE_APPLICATION_CREDENTIALS="/Users/priyal/Desktop/now/newcopy/cloudproject/voiceAccountKey.json"
import playsound # from python-vlc
import os

def synthesize_text(text):
    """Synthesizes speech from the input string of text."""
    from google.cloud import texttospeech

    client = texttospeech.TextToSpeechClient().from_service_account_json("./voiceAccountKey.json")
    #language.LanguageServiceClient.
    
    input_text = texttospeech.SynthesisInput(text=text) #"text is all mine")

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Standard-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )

    # The response's audio_content is binary.
    with open("./output.mp3", "wb") as out:
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

    
    #p = vlc.MediaPlayer("output.mp3")
    #p.play()
    #playsound.playsound('/Users/priyal/Desktop/now/newcopy/cloudproject/output.mp3', True)
   # os.system("afplay " + "/Users/priyal/Desktop/now/newcopy/cloudproject/output.mp3")

    os.system("afplay " + "./output.mp3")