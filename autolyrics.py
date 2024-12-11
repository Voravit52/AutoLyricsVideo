import requests
from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip, CompositeVideoClip
from moviepy.video.fx.all import lum_contrast
from PIL import Image, ImageDraw, ImageFont

# ฟังก์ชันดึงข้อมูลจาก Spotify API
def fetch_spotify_data(track_id):
    base_url = "https://api.paxsenix.biz.id"

    # ดึงเนื้อเพลง
    lyrics_response = requests.get(f"{base_url}/lyrics/spotify?id={track_id}")
    lyrics = lyrics_response.json().get('lyrics', '')

    # ดึงเพลง
    audio_response = requests.get(f"{base_url}/dl/spotify?url=https://open.spotify.com/track/{track_id}&serv=spotify")
    audio_url = audio_response.json().get('directUrl')

    # ดึง Canvas
    canvas_response = requests.get(f"{base_url}/spotify/canvas?id={track_id}")
    canvas_url = canvas_response.json().get('data', {}).get('canvasesList', [{}])[0].get('canvasUrl')

    return lyrics, audio_url, canvas_url

# ฟังก์ชันดาวน์โหลดไฟล์
def download_file(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as f:
        f.write(response.content)

# ฟังก์ชันสร้างภาพข้อความด้วย PIL
def create_text_image(text, image_size=(720, 1280), font_size=50, max_lines=10):
    img = Image.new('RGBA', image_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("font.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    # แบ่งข้อความตามขนาดที่เหมาะสม
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = f"{current_line} {word}".strip()
        if draw.textsize(test_line, font=font)[0] <= image_size[0] - 20:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # จำกัดจำนวนบรรทัดตาม max_lines
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] += "..."  # เพิ่ม "..." เพื่อบอกว่ามีข้อความต่อ

    # คำนวณตำแหน่งเริ่มต้นให้อยู่กลางภาพ
    text_height = font.getsize("Ay")[1]
    total_text_height = len(lines) * text_height
    y_offset = (image_size[1] - total_text_height) // 2

    # เขียนข้อความลงในภาพ
    for line in lines:
        text_width, _ = draw.textsize(line, font=font)
        text_position = ((image_size[0] - text_width) // 2, y_offset)
        draw.text(text_position, line, font=font, fill="white")
        y_offset += text_height

    return img

# ฟังก์ชันสร้างวิดีโอเนื้อเพลง
def create_lyric_video(lyrics, audio_file, canvas_file, output_file):
    lyric_lines = lyrics.splitlines()

    # โหลด Canvas และปรับความสว่าง
    canvas_clip = VideoFileClip(canvas_file).loop(duration=170)
    canvas_clip = lum_contrast(canvas_clip, lum=-1.0)  # ลดแสงเล็กน้อย

    # โหลดเพลง
    audio_clip = AudioFileClip(audio_file)

    # สร้างคลิปเนื้อเพลง
    text_clips = []
    for i, line in enumerate(lyric_lines):
        if "]" in line:
            timestamp, text = line.split("]", 1)
            timestamp = timestamp[1:]

            if timestamp.strip():
                try:
                    time_parts = timestamp.split(":")
                    minutes = float(time_parts[0])
                    seconds = float(time_parts[1])
                    start_time = minutes * 60 + seconds

                    # เวลาสิ้นสุดสำหรับบรรทัดนี้
                    if i + 1 < len(lyric_lines) and "]" in lyric_lines[i + 1]:
                        next_timestamp = lyric_lines[i + 1].split("]", 1)[0][1:]
                        next_time_parts = next_timestamp.split(":")
                        next_minutes = float(next_time_parts[0])
                        next_seconds = float(next_time_parts[1])
                        end_time = next_minutes * 60 + next_seconds
                    else:
                        end_time = audio_clip.duration

                    duration = end_time - start_time

                    # สร้างภาพข้อความ
                    text_image = create_text_image(text.strip())
                    text_image.save("temp_text.png")

                    # แปลงภาพข้อความเป็น ImageClip
                    text_clip = (ImageClip("temp_text.png")
                                 .set_position(('center', 'center'))
                                 .set_start(start_time)
                                 .set_duration(duration)
                                 .fadein(0.5)
                                 .fadeout(0.5))
                    text_clips.append(text_clip)
                except ValueError:
                    print(f"Warning: Invalid timestamp format: {timestamp}")

    # รวมคลิปทั้งหมด
    try:
        video = CompositeVideoClip([canvas_clip] + text_clips)
        video = video.set_audio(audio_clip)

        # เขียนวิดีโอออกไฟล์
        video.write_videofile(output_file, fps=24, codec='libx264', audio_codec='aac')
    except Exception as e:
        print(f"Error while creating video: {e}")

# โปรแกรมหลัก
def main():
    track_id = "xxxxxxxxxxx"  # Spotify Track ID
    lyrics, audio_url, canvas_url = fetch_spotify_data(track_id)

    print("Fetched lyrics:", lyrics)  # Debug

    # ดาวน์โหลดไฟล์เพลงและ Canvas
    download_file(audio_url, "audio.mp3")
    download_file(canvas_url, "canvas.mp4")

    # สร้างวิดีโอเนื้อเพลง
    create_lyric_video(lyrics, "audio.mp3", "canvas.mp4", "output_video.mp4")
    print("Lyric video created: output_video.mp4")

if __name__ == "__main__":
    main()
    
