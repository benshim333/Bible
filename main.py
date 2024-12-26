import requests
from gtts import gTTS
import moviepy.editor
from moviepy.video.fx.all import crop

# Fetch Bible Verses
def get_bible_verses(passage):
    response = requests.get(f"https://bible-api.com/{passage}")
    data = response.json()
    verses = data['text']
    return verses

# Convert Text to Speech
def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text, lang="en")
    tts.save(filename)
    print(f"Audio saved as {filename}")

# Main Program
if __name__ == "__main__":
    passages = ["Genesis 1:1-8", "Genesis 1:9-13", "Genesis 1:14-19", "Genesis 1:20-25", "Genesis 1:26-28", "Genesis 1:29-31"]

    cumulative_length = 0 # Start time in video
    video_clip = moviepy.editor.VideoFileClip("video.mp4")

    for i, passage in enumerate(passages):
        verses = get_bible_verses(passage)
        text_to_speech(verses, filename=f"audio_files/{i}.mp3")
        audio_clip = moviepy.editor.AudioFileClip(f"audio_files/{i}.mp3")
        sub_clip = video_clip.subclip(cumulative_length, cumulative_length + audio_clip.duration)
        cropped_clip = crop(sub_clip, x1=710, y1=0, x2=1210, y2=1080)
        final_clip = cropped_clip.set_audio(audio_clip)
        final_clip.write_videofile(f"video_files/{i}.mp4")
        print(f"{passage} completed")

        cumulative_length += audio_clip.duration # Keep track of position in video