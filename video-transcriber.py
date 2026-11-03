import os
import re
from pathlib import Path
import whisper
###
### If you like content around Python automation, video editing, or AI, consider liking and subscribing at https://www.youtube.com/@jonislab
###

def format_timestamp(seconds: float) -> str:
    """Converts seconds into MM:SS format."""
    mins = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"


def transcribe_video_to_script(
    video_path: str,
    output_txt: str = "script.txt",
    model_size: str = "base",
    include_timestamps: bool = True,
):
    """Transcribes a video file and writes a script to a text file.
    Returns the raw transcript text so it can be passed to downstream processors.
    """
    print(f"Loading Whisper model '{model_size}'...")
    model = whisper.load_model(model_size)

    print(f"Transcribing '{video_path}'...")
    # Setting word_timestamps=False speeds up processing significantly
    result = model.transcribe(video_path, word_timestamps=False)

    segments = result.get("segments", [])
    if not segments:
        print("No speech detected.")
        return None

    # Automatically create parent directories if they don't exist
    Path(output_txt).parent.mkdir(parents=True, exist_ok=True)

    # 1. Write the primary script file (with or without timestamps based on flag)
    with open(output_txt, "w", encoding="utf-8") as f:
        if include_timestamps:
            for seg in segments:
                start_time = format_timestamp(seg["start"])
                text = seg["text"].strip()
                f.write(f"[{start_time}] {text}\n")
        else:
            f.write(result.get("text", "").strip() + "\n")

    print(f"Script saved to: {output_txt}")

    # 2. Return the clean, un-timed full text for the TTS reformatter
    return result.get("text", "")


def reformat_for_slow_tts(raw_text: str) -> str:
    # 1. Clean up excessive whitespace and newlines
    text = re.sub(r"\s+", " ", raw_text).strip()

    # 2. Split text into sentences using standard terminal punctuation (. ! ?)
    sentences = re.split(r"(?<=[.!?])\s+", text)

    formatted_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue

        # If a sentence is long (> 12 words), insert a comma before coordinating conjunctions mid-sentence
        words = sentence.split()
        if len(words) > 12:
            sentence = re.sub(
                r"\b(and|but|as|while|when)\b", r", \1", sentence, count=1
            )

        formatted_sentences.append(sentence)

    # 3. Rebuild with double line breaks for dramatic paragraph separation
    return "\n\n".join(formatted_sentences)


def process_script_file(file_path: str, raw_text_override: str = None):
    input_path = Path(file_path)

    # If raw text was passed directly, use it. Otherwise, read from disk.
    if raw_text_override is not None:
        raw_text = raw_text_override
    else:
        if not input_path.exists():
            print(f"Error: The file '{file_path}' was not found.")
            return

        with open(input_path, "r", encoding="utf-8") as f:
            raw_text = f.read()

    # Process and reformat the clean text (guaranteed no timecodes)
    optimized_text = reformat_for_slow_tts(raw_text)

    # Construct the output filename (e.g., transcription.txt -> transcription-qwen.txt)
    output_filename = f"{input_path.stem}-qwen{input_path.suffix}"
    output_path = input_path.with_name(output_filename)

    # Write the modified script to the new file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(optimized_text)

    print(f"Success! Reformatted script saved to:\n{output_path.resolve()}")


if __name__ == "__main__":
    # Configuration paths and options
    video_file = "D:\\your-video-path\\vid.mp4"
    transcription_output = "D:\\your-video-path\\transcription.txt"

    # Step 1: Transcribe the video file (capturing the raw un-timed text output)
    raw_transcript = transcribe_video_to_script(
        video_path=video_file,
        output_txt=transcription_output,
        model_size="base",  # Switch to 'small', 'medium', or 'large' for higher accuracy
        include_timestamps=True,  # Set to True/False for your main file; -qwen will stay clean
    )

    print("-" * 40)

    # Step 2: Pass the clean raw text directly into the Qwen text formatter
    if raw_transcript:
        process_script_file(transcription_output, raw_text_override=raw_transcript)
