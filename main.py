import requests
import time

API_KEY = "your_API_KEY"
BASE_URL = "https://api.assemblyai.com/v2"

headers = {"authorization": API_KEY}

#1.upload audio file to assemblyAI
def upload_audio(filename):
    print("uploading audio file...")
    with open(filename, "rb")as f:
        response = requests.post(f"{BASE_URL}/upload",headers=headers, data = f)
        return response.json()["upload_url"]
    
#2.start transcription
def start_transcription(audio_url):
    data = {"audio_url": audio_url}
    response = requests.post(f"{BASE_URL}/transcript",headers=headers, json=data)
    return response.json()["id"]

#3.poll until transcrption is ready
def get_transcription(transcript_id):
    while True:
        response = requests.get(f"{BASE_URL}/transcript/{transcript_id}",headers=headers)
        result = response.json()
        if result["status"] == "completed":
            return result["text"]
        elif result["status"]== "error":
            return Exception(result["error"])
        time.sleep(5)

#Demo run
audio_url = upload_audio("meeting.mp3")
transcript_id = start_transcription(audio_url)
transcript_text = get_transcription(transcript_id)

print("TRANSCRIPT:")
print(transcript_text)

#simple summarization example
print("\nSUMMARY:")
for sentence in transcript_text.split(".")[:5]:
    print("-", sentence.strip())