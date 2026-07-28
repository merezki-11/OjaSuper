def mock_speech_to_text(audio_file_path: str) -> str:
    \"\"\"
    Mocks the Whisper STT process.
    In the real implementation, this will load whisper.cpp and transcribe the audio.
    \"\"\"
    # For scaffolding, return a dummy string based on the filename or just a fixed string
    return "I sold 5 bags of rice and 2 bottles of oil for 15000 naira"
