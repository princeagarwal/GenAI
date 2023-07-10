import os

#### ----------------------------------------------------------------------------------------------
#### AZURE API
#### ----------------------------------------------------------------------------------------------

import azure.cognitiveservices.speech as speechsdk

def speech_synthesizer_bookmark_reached_cb(evt: speechsdk.SessionEventArgs):
    print('BookmarkReached event:')
    print('\tAudioOffset: {}ms'.format((evt.audio_offset + 5000) / 10000))
    print('\tText: {}'.format(evt.text))

def speech_synthesizer_synthesis_canceled_cb(evt: speechsdk.SessionEventArgs):
    print('SynthesisCanceled event')

def speech_synthesizer_synthesis_completed_cb(evt: speechsdk.SessionEventArgs):
    print('SynthesisCompleted event:')
    print('\tAudioData: {} bytes'.format(len(evt.result.audio_data)))
    print('\tAudioDuration: {}'.format(evt.result.audio_duration))

def speech_synthesizer_synthesis_started_cb(evt: speechsdk.SessionEventArgs):
    print('SynthesisStarted event')

def speech_synthesizer_synthesizing_cb(evt: speechsdk.SessionEventArgs):
    print('Synthesizing event:')
    print('\tAudioData: {} bytes'.format(len(evt.result.audio_data)))

def speech_synthesizer_viseme_received_cb(evt: speechsdk.SessionEventArgs):
    print('VisemeReceived event:')
    print('\tAudioOffset: {}ms'.format((evt.audio_offset + 5000) / 10000))
    print('\tVisemeId: {}'.format(evt.viseme_id))

def speech_synthesizer_word_boundary_cb(evt: speechsdk.SessionEventArgs):
    print('WordBoundary event:')
    print('\tBoundaryType: {}'.format(evt.boundary_type))
    print('\tAudioOffset: {}ms'.format((evt.audio_offset + 5000) / 10000))
    print('\tDuration: {}'.format(evt.duration))
    print('\tText: {}'.format(evt.text))
    print('\tTextOffset: {}'.format(evt.text_offset))
    print('\tWordLength: {}'.format(evt.word_length))

def generate_speech(config, text):

    os.environ["SPEECH_KEY"] = config['api_key']
    os.environ["SPEECH_REGION"] = config['region']

    speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))

    # Required for WordBoundary event sentences.
    speech_config.set_property(property_id=speechsdk.PropertyId.SpeechServiceResponse_RequestSentenceBoundary, value='true')

    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)

    # Subscribe to events
    speech_synthesizer.bookmark_reached.connect(speech_synthesizer_bookmark_reached_cb)
    speech_synthesizer.synthesis_canceled.connect(speech_synthesizer_synthesis_canceled_cb)
    speech_synthesizer.synthesis_completed.connect(speech_synthesizer_synthesis_completed_cb)
    speech_synthesizer.synthesis_started.connect(speech_synthesizer_synthesis_started_cb)
    speech_synthesizer.synthesizing.connect(speech_synthesizer_synthesizing_cb)
    speech_synthesizer.viseme_received.connect(speech_synthesizer_viseme_received_cb)
    speech_synthesizer.synthesis_word_boundary.connect(speech_synthesizer_word_boundary_cb)

    # The language of the voice that speaks.
    speech_synthesis_voice_name='hi-IN-MadhurNeural'

    ssml = f"""<speak version='1.0' xml:lang='hi-IN' xmlns='http://www.w3.org/2001/10/synthesis' xmlns:mstts='http://www.w3.org/2001/mstts'>
        <voice name='{speech_synthesis_voice_name}'>
            <mstts:viseme type='redlips_front'/>
                <mstts:express-as style="cheerful" styledegree="2">
                {text}
                </mstts:express-as>
        </voice>
    </speak>"""

    # Synthesize the SSML
    print("SSML to synthesize: \r\n{}".format(ssml))
    speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml).get()
    #stream = speechsdk.AudioDataStream(speech_synthesis_result)
    #stream.save_to_wav_file(f"""azure_result.wav""")

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("SynthesizingAudioCompleted result")
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

    return speech_synthesis_result.audio_data


#### ----------------------------------------------------------------------------------------------
#### BARK MODEL
#### ----------------------------------------------------------------------------------------------

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
from IPython.display import Audio

def generate_speech_bark(config, text):

    os.environ["SUNO_OFFLOAD_CPU"] = config["SUNO_OFFLOAD_CPU"]
    os.environ["SUNO_USE_SMALL_MODELS"] = config["SUNO_USE_SMALL_MODELS"]

    preload_models()

    audio_array = generate_audio(text)
    write_wav("bark_generation.wav", SAMPLE_RATE, audio_array)
    #Audio(audio_array, rate=SAMPLE_RATE)
    return audio_array