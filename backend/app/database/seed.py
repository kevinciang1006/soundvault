import random
from sqlalchemy.orm import Session
from models.schemas import Pack, Sample


PACKS_DATA = [
    {"name": "Tokyo Trap Vol. 1", "creator": "KxngProd", "genre": "Trap", "cover_color": "#6366f1", "cover_color_2": "#8b5cf6", "abbrev": "TTR", "code": "TKYO"},
    {"name": "Deep House Essentials", "creator": "WaveForge", "genre": "House", "cover_color": "#06b6d4", "cover_color_2": "#0891b2", "abbrev": "DHE", "code": "DHSE"},
    {"name": "Lo-Fi Dreams", "creator": "CloudBeats", "genre": "R&B", "cover_color": "#f59e0b", "cover_color_2": "#d97706", "abbrev": "LFD", "code": "LOFI"},
    {"name": "Techno Warehouse", "creator": "BerlinKit", "genre": "Techno", "cover_color": "#1a1a2e", "cover_color_2": "#16213e", "abbrev": "TWH", "code": "TWHS"},
    {"name": "Boom Bap Classics", "creator": "OldSoul", "genre": "Hip Hop", "cover_color": "#dc2626", "cover_color_2": "#b91c1c", "abbrev": "BBC", "code": "BOOM"},
    {"name": "Future Bass Elements", "creator": "NeonSynth", "genre": "Pop", "cover_color": "#ec4899", "cover_color_2": "#db2777", "abbrev": "FBE", "code": "FBAS"},
    {"name": "Ambient Textures", "creator": "SilentDrift", "genre": "Ambient", "cover_color": "#059669", "cover_color_2": "#047857", "abbrev": "AMB", "code": "AMBT"},
    {"name": "Drum & Bass Fury", "creator": "BreakCore", "genre": "Drum & Bass", "cover_color": "#7c3aed", "cover_color_2": "#6d28d9", "abbrev": "DBF", "code": "DNBF"},
    {"name": "Vocal Chops Vol. 2", "creator": "VoxLab", "genre": "Trap", "cover_color": "#0ea5e9", "cover_color_2": "#0284c7", "abbrev": "VCV", "code": "VCLP"},
    {"name": "808 Arsenal", "creator": "SubFreq", "genre": "Trap", "cover_color": "#111827", "cover_color_2": "#1f2937", "abbrev": "808", "code": "ARSL"},
]

GENRE_BPM_RANGES = {
    "Trap": (130, 160),
    "House": (120, 130),
    "R&B": (70, 95),
    "Techno": (130, 150),
    "Hip Hop": (85, 100),
    "Pop": (100, 130),
    "Ambient": (60, 90),
    "Drum & Bass": (160, 180),
}

KEYS = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B",
        "Cm", "C#m", "Dm", "D#m", "Em", "Fm", "F#m", "Gm", "G#m", "Am", "A#m", "Bm"]

SAMPLE_TYPES_WEIGHTED = (
    ["loop"] * 6 + ["one_shot"] * 2 + ["vocal"] * 1 + ["fx"] * 1
)

SAMPLE_DESCS = {
    "loop": ["drums", "melody", "bass", "chord", "arp", "groove", "bounce", "swing"],
    "one_shot": ["kick", "snare", "hihat", "clap", "perc", "tom", "crash", "shaker"],
    "vocal": ["chop", "adlib", "hook", "phrase", "breathe", "echo", "slice", "layer"],
    "fx": ["riser", "sweep", "impact", "transition", "glitch", "reverb", "noise", "whoosh"],
}


def seed_database(db: Session):
    pack_count = db.query(Pack).count()
    if pack_count > 0:
        return

    random.seed(42)

    created_packs = []
    for pack_data in PACKS_DATA:
        pack = Pack(
            name=pack_data["name"],
            creator=pack_data["creator"],
            genre=pack_data["genre"],
            sample_count=6,
            cover_color=pack_data["cover_color"],
            cover_color_2=pack_data["cover_color_2"],
        )
        db.add(pack)
        db.flush()
        created_packs.append((pack, pack_data))

    samples_created = []
    for pack, pack_data in created_packs:
        genre = pack.genre
        bpm_min, bpm_max = GENRE_BPM_RANGES.get(genre, (100, 140))

        for i in range(6):
            sample_type = SAMPLE_TYPES_WEIGHTED[i % len(SAMPLE_TYPES_WEIGHTED)]
            if i < 4:
                sample_type = "loop"
            elif i == 4:
                sample_type = "one_shot"
            else:
                sample_types_remaining = ["vocal", "fx", "one_shot"]
                sample_type = random.choice(sample_types_remaining)

            bpm = random.randint(bpm_min, bpm_max)
            key = random.choice(KEYS)
            desc = random.choice(SAMPLE_DESCS.get(sample_type, ["sample"]))
            duration = round(random.uniform(1.0, 16.0), 2)
            is_premium = random.random() < 0.30
            play_count = random.randint(0, 5000)

            type_abbrev = {
                "loop": "LPP",
                "one_shot": "OSS",
                "vocal": "VCL",
                "fx": "FXX",
            }.get(sample_type, "SMP")

            filename = f"{pack_data['abbrev']}_{pack_data['code']}_{bpm}_{type_abbrev}_{desc}_{key}.wav"

            sample = Sample(
                pack_id=pack.id,
                pack_name=pack.name,
                pack_creator=pack.creator,
                filename=filename,
                genre=genre,
                sample_type=sample_type,
                bpm=float(bpm),
                key=key,
                duration_seconds=duration,
                is_premium=is_premium,
                play_count=play_count,
            )
            db.add(sample)
            samples_created.append(sample)

    db.commit()
    print(f"Seeded {len(created_packs)} packs and {len(samples_created)} samples.")
