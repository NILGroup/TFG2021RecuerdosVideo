from pathlib import Path

temp_path = Path("../temp")
chunk_video_path = Path(__file__).parent / temp_path / "chunks_video"
input_video_path = Path(__file__).parent / temp_path / "input_video"
normalized_audio_path = Path(__file__).parent / temp_path / "normalized_audio"
output_email_path = Path(__file__).parent / temp_path / "output_email"
chunks_audio_path = Path(__file__).parent / temp_path / "chunks_audio"