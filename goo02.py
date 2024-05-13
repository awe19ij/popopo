import os
import re
from pydub import AudioSegment
from google.cloud import speech
from google.oauth2 import service_account
import nltk
from nltk.tokenize import word_tokenize
import difflib

# NLTK punkt 데이터셋 다운
nltk.download('punkt')

# Google 키
credentials = service_account.Credentials.from_service_account_file(
    'C:\\Users\\iseo\\Desktop\\aibase03\\rapid-bricolage-422612-b7-1a1d95d2c15f.json'
)

# Google 클라이언트 초기화
client = speech.SpeechClient(credentials=credentials)

expected_text = "제 장점은 체계적으로 일을 처리하는 능력입니다. 이를 통해 정확하고 효율적으로 업무를 수행할 수 있습니다. 반면 제 단점은 너무 완벽을 추구하는 경향이 있어서 이로 인해 스트레스를 받기도 합니다. 하지만 이 점을 인지하고 상황에 따른 유연성을 기르려고 노력하고 있습니다."

file_name = "C:\\Users\\iseo\\Desktop\\aibase03\\fast.wav"

# WAV 스테레오 > 모노 wav+모노밖에 분석안댐 / 이외는 좀 마니 귀찮 / 마이크  모노 스테레오 타입 미리 확인하고 사는게 나을지도
sound = AudioSegment.from_wav(file_name)
sound = sound.set_channels(1)
audio_content = sound.raw_data

audio = speech.RecognitionAudio(content=audio_content)
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=48000,
    language_code='ko-KR',
    enable_automatic_punctuation=True
)

# 긴 음성 인식 짤라먹기 방지
operation = client.long_running_recognize(config=config, audio=audio)
response = operation.result(timeout=90)

# 문장 단위 비교
received_text = " ".join([result.alternatives[0].transcript for result in response.results])
expected_sentences = re.split(r'[.!?]', expected_text)
received_sentences = re.split(r'[.!?]', received_text)

print('Comparison Result:')
for expected_sentence, received_sentence in zip(expected_sentences, received_sentences):
    # 편집 거리 유사성 계산
    similarity = difflib.SequenceMatcher(None, expected_sentence, received_sentence).ratio()
    print(f"Expected: {expected_sentence}")
    print(f"Received: {received_sentence}")
    print(f"Similarity: {similarity:.2f}")

    # 유사성이 높은 문장에 대한 단어 비교
    if similarity > 0.6:
        expected_words = word_tokenize(expected_sentence)
        received_words = word_tokenize(received_sentence)
        print("\nWord Comparison:")
        for ew, rw in zip(expected_words, received_words):
            print(f"Expected: {ew}, Received: {rw}, Match: {ew == rw}")
# 최종본 요놈