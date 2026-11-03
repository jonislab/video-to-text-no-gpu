# video-to-text
Python no GPU script to transcribe the video scripts
# Whisper Video Transcriber & Slow-TTS Script Formatter

An automated Python tool that uses **OpenAI Whisper** to transcribe video files into clean text scripts with optional timestamps, and features an intelligent reformatting engine designed specifically to optimize text for Text-to-Speech (TTS) engines (such as Qwen-TTS). It automatically structures long sentences, inserts strategic pauses, and cleans up spacing for natural-sounding narration pacing.

---

## Features
- **Video Transcription:** Leverages OpenAI Whisper (`base`, `small`, `medium`, `large`) to transcribe audio directly from video files.
- **Timestamped Transcripts:** Generates clean, readable timecodes (e.g., `[01:23]`) alongside your spoken dialogue.
- **TTS Pacing Optimization:** Automatically cleans whitespace, splits long sentences (> 12 words) at natural conjunctions (`and`, `but`, `as`, `while`, `when`), and structures paragraphs with double line breaks for dramatic, natural-sounding TTS pacing.
- **Hardware Acceleration Support:** Fully compatible with NVIDIA CUDA GPU acceleration or CPU-only PyTorch execution.

---

## Prerequisites
Before you begin, ensure you have **Python 3.8+** installed on your system.

---

## Step-by-Step Installation Guide

### Step 1: Download or Clone the Repository
Click the green **Code** button at the top right of this GitHub page, select **Download ZIP**, and extract the files to a folder on your computer.

### Step 2: Install Dependencies (Choose CPU or CUDA/GPU)
Open your terminal, Command Prompt, or PowerShell, navigate to the project directory, and choose **one** option below:

#### Option A: For NVIDIA GPU (CUDA) Users — *Recommended for Speed*
If you have a compatible NVIDIA graphics card, run:
```bash
pip install torch torchvision torchaudio
pip install openai-whisper
```

#### Option B: For CPU-Only Users
If you are running on a standard CPU, install PyTorch using the CPU wheel index first:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install openai-whisper
```

### Step 3: Install and Configure FFmpeg
This script relies on FFmpeg for audio/video extraction.
1. Download FFmpeg for Windows from [Gyan.dev FFmpeg Builds](https://www.gyan.dev/ffmpeg/builds/).
2. Extract the ZIP file.
3. Locate the **`bin`** folder (containing `ffmpeg.exe`) and copy its file path.
4. Add it to your Windows System PATH:
   * Open Windows Search and type: **“Edit the system environment variables”**.
   * Click **Environment Variables**, select `Path` under System variables, and click **Edit**.
   * Click **New**, paste your FFmpeg `bin` path, and click **OK** to save.

---

## Usage

1. Open the script and configure your file paths in the `if __name__ == "__main__":` block:
   ```python
   if __name__ == "__main__":
       # Update these paths to match your local directory structure
       video_file = r"C:\path\to\your\video.mp4"
       transcription_output = r"C:\path\to\your\output\transcription.txt"

       raw_transcript = transcribe_video_to_script(
           video_path=video_file,
           output_txt=transcription_output,
           model_size="base",  # Options: tiny, base, small, medium, large
           include_timestamps=True,
       )

       if raw_transcript:
           process_script_file(transcription_output, raw_text_override=raw_transcript)
   ```
2. Run the script from your terminal:
   ```bash
   python video_transcriber.py
   ```
3. The script will generate two files:
   - Your primary timestamped transcript (`transcription.txt`)
   - An optimized, comma-spaced version tailored for TTS engines (`transcription-qwen.txt`)

---

## License
This project is licensed under the [MIT License](LICENSE).
