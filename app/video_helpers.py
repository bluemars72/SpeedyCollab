import os
import re
from moviepy import (VideoFileClip, TextClip, AudioFileClip,
                     CompositeVideoClip, concatenate_videoclips)
from moviepy.video.fx import *
from pydub import AudioSegment

import librosa
import soundfile as sf
import tempfile

def clean_temp_folder(path, pattern=None):
    if not os.path.exists(path):
        print(f"Path {path} does not exist.")
        return

    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        if os.path.isfile(file_path):
            if pattern is None or re.match(pattern, filename):
                os.remove(file_path)
                print(f"Deleted: {file_path}")

def put_text_on_video(clip, text_to_write, font_size,
                      duration=None, font=None, color=None):
    if not duration:
        duration = clip.duration
    if not font:
        font="C:\\Windows\\Fonts\\Arial.ttf"
    if not color:
        color = 'red'

    # Generate a text clip. You can customize the font, color, etc.

    txt_clip = TextClip(
        font=font,
        text=text_to_write,
        font_size=font_size,
        color=color,
        stroke_color="black",
        stroke_width=8,
        horizontal_align="top"
    ).with_duration(duration).with_position('center')

    # Overlay the text clip on the first video clip
    final_video = CompositeVideoClip([clip, txt_clip])

    return final_video

def speed_up_video_with_pitch(input_clip, speed_amount=2):
    semitones= -11

    clip = input_clip

    new_clip = MultiplySpeed(factor=speed_amount).apply(clip)

    # Step 1: Extract audio to temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        audio_path = temp_audio.name
        new_clip.audio.write_audiofile(audio_path, codec='pcm_s16le')  # uncompressed WAV

    # Step 2: Load with librosa
    y, sr = librosa.load(audio_path, sr=None)

    # Step 3: Pitch shift
    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)
    y_shifted = librosa.util.normalize(y_shifted)

    # Step 4: Write to new temp file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_shifted:
        shifted_path = temp_shifted.name
        sf.write(shifted_path, y_shifted, sr)

    # Step 5: Load shifted audio into moviepy
    new_audio = AudioFileClip(shifted_path)

    # Step 6: Replace audio and write final video
    new_clip.audio = new_audio
    # final.write_videofile(output_file, audio_codec='aac')

    final_video = CompositeVideoClip([new_clip])

    return final_video

def double_and_concat(input_clip, output_file):

    sped_up_clip = speed_up_video_with_pitch(input_clip, speed_amount=2)

    # Here is where we apply effects

    #inverted = InvertColors().apply(sped_up_clip)


    #quad_clip = clips_array([[sped_up_clip, sped_up_clip],
    #                        [sped_up_clip, sped_up_clip]])

    new_clip = concatenate_videoclips([sped_up_clip,
                                       sped_up_clip])

    print("Clip is doubled and concat, now write to: ", output_file)

    new_clip.write_videofile(output_file, audio_codec='aac')

    new_clip.close()
    sped_up_clip.close()

    return output_file


def adjust_audio_pitch(audio_file_path, output_path, semitones):
    # Load with librosa
    y, sr = librosa.load(audio_file_path, sr=None)

    # Shift pitch while preserving tempo
    y_shifted = librosa.effects.pitch_shift(y, sr=sr, n_steps=semitones)

    # Save to temp wav file
    sf.write("temp_shifted.wav", y_shifted, sr)

    # Optionally load into pydub again
    shifted = AudioSegment.from_wav("temp_shifted.wav")
    shifted.export(output_path, format="mp3")  # or 'wav', 'flac', etc.
    return output_path