
# Lyric Video Generator

## 🔄 เปลี่ยนภาษา | Switch Language
[ภาษาไทย](#การใช้งานภาษาไทย) | [English](#usage-in-english)

---

## Usage in English

### **Overview**
This script generates a lyric video using:
1. **Lyrics**: Retrieved from the Spotify API.
2. **Audio**: Downloaded from a Spotify track.
3. **Canvas**: A video background fetched from Spotify.

The output is a synchronized lyric video with audio and background visuals.

---

### **Requirements**
1. Python 3.x installed.
2. The following Python libraries:
   - `requests`
   - `moviepy`
   - `Pillow`

3. **FFmpeg** installed and added to your system PATH (required by `moviepy`).

#### Install Dependencies
```bash
pip install requests moviepy pillow
```

---

### **How to Use**
1. **Edit the `track_id`**  
   Replace the `track_id` variable in the script with your desired Spotify track ID. For example:
   ```python
   track_id = "0AGhwXsWpVOwjHY5yf4dtD"
   ```

2. **Run the script**  
   Run the script using:
   ```bash
   python script_name.py
   ```

3. **Output File**  
   The script will generate a lyric video named `output_video.mp4` in the current directory.

---

## การใช้งานภาษาไทย

### **ภาพรวม**
สคริปต์นี้สร้างวิดีโอเนื้อเพลงโดย:
1. **เนื้อเพลง**: ดึงจาก Spotify API
2. **ไฟล์เพลง**: ดาวน์โหลดจาก Spotify Track
3. **Canvas**: ดึงวิดีโอพื้นหลังจาก Spotify

ผลลัพธ์คือวิดีโอเนื้อเพลงที่ซิงค์กับเสียงเพลงและพื้นหลังแบบ Canvas

---

### **สิ่งที่ต้องเตรียม**
1. ติดตั้ง Python 3.x
2. ติดตั้งไลบรารี Python เหล่านี้:
   - `requests`
   - `moviepy`
   - `Pillow`

3. ติดตั้ง **FFmpeg** และเพิ่มลงใน PATH ของระบบ (จำเป็นสำหรับ `moviepy`)

#### คำสั่งติดตั้งไลบรารี
```bash
pip install requests moviepy pillow
```

---

### **วิธีการใช้งาน**
1. **แก้ไข `track_id`**  
   เปลี่ยนค่า `track_id` ในสคริปต์เป็น Spotify Track ID ที่ต้องการ เช่น:
   ```python
   track_id = "0AGhwXsWpVOwjHY5yf4dtD"
   ```

2. **รันสคริปต์**  
   ใช้คำสั่ง:
   ```bash
   python script_name.py
   ```

3. **ผลลัพธ์**  
   สคริปต์จะสร้างวิดีโอเนื้อเพลงชื่อ `output_video.mp4` ในไดเรกทอรีปัจจุบัน
