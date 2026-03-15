import os
import uuid
import numpy as np
from fastapi import APIRouter, UploadFile, File, HTTPException

from models.schemas import AnalysisResponse

router = APIRouter()

ALLOWED_EXTENSIONS = {".mp3", ".wav", ".flac", ".ogg", ".m4a"}
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB


def detect_key(y, sr):
    """Detect musical key using chroma features and Krumhansl-Schmuckler algorithm."""
    import librosa

    # Major and minor key profiles (Krumhansl-Schmuckler)
    major_profile = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09,
                               2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
    minor_profile = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53,
                               2.54, 4.75, 3.98, 2.69, 3.34, 3.17])

    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    chroma_mean = np.mean(chroma, axis=1)

    note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

    best_major_corr = -np.inf
    best_major_root = 0
    best_minor_corr = -np.inf
    best_minor_root = 0

    for root in range(12):
        # Rotate the profile, not the chroma
        rotated_major = np.roll(major_profile, root)
        rotated_minor = np.roll(minor_profile, root)

        # Correlate with chroma
        major_corr = float(np.corrcoef(chroma_mean, rotated_major)[0, 1])
        minor_corr = float(np.corrcoef(chroma_mean, rotated_minor)[0, 1])

        if major_corr > best_major_corr:
            best_major_corr = major_corr
            best_major_root = root

        if minor_corr > best_minor_corr:
            best_minor_corr = minor_corr
            best_minor_root = root

    # Return the best match (major or minor)
    if best_major_corr >= best_minor_corr:
        return f"{note_names[best_major_root]} Major"
    else:
        return f"{note_names[best_minor_root]} Minor"


@router.post("/api/analyze", response_model=AnalysisResponse)
async def analyze_audio(file: UploadFile = File(...)):
    import librosa

    # Validate extension
    filename = file.filename or "unknown"
    ext = os.path.splitext(filename)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
        )

    # Read file content
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 20MB.")

    # Save to temp file
    temp_path = f"/tmp/soundvault_{uuid.uuid4().hex}{ext}"
    try:
        with open(temp_path, "wb") as f:
            f.write(content)

        # Load with librosa (up to 60 seconds for analysis)
        y, sr = librosa.load(temp_path, duration=60, mono=True)

        # Get full duration
        duration_seconds = librosa.get_duration(path=temp_path)

        # Detect BPM
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        # Handle both scalar and array tempo values
        bpm = float(np.round(tempo, 1)) if np.ndim(tempo) == 0 else float(np.round(tempo[0], 1))

        # Detect Key
        key = detect_key(y, sr)

    except Exception as e:
        import traceback
        error_msg = f"Analysis failed: {str(e)}\n{traceback.format_exc()}"
        print(error_msg)  # Log to console for debugging
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return AnalysisResponse(
        bpm=bpm,
        key=key,
        duration_seconds=round(duration_seconds, 2),
        filename=filename,
    )
