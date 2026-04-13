import guitarpro
from parse_metadata import extract_techniques

def extract_metadata(filepath):
    song = guitarpro.parse(filepath)
    return {
        "title": song.title,
        "artist": song.artist,
        "tempo": song.tempo,
        "tracks": [t.name for t in song.tracks],
        "num_measures": len(song.tracks[0].measures),
        "techniques": extract_techniques(song),
    }

def metadata_to_prompt(meta):
    parts = []
    if meta.get("tempo"):
        parts.append(f"Tempo: {meta['tempo']} BPM")
    
    # filter out generic track names
    real_tracks = [t for t in meta.get("tracks", []) 
                   if not t.lower().startswith("track")]
    if real_tracks:
        parts.append(f"Instruments: {', '.join(real_tracks[:3])}")
    
    if meta.get("techniques"):
        parts.append(f"Techniques: {', '.join(meta['techniques'])}")
    if meta.get("num_measures"):
        parts.append(f"Length: {meta['num_measures']} measures")
    return ". ".join(parts) + "."

if __name__ == "__main__":
    meta = extract_metadata("frankOcean.gp5")
    prompt = metadata_to_prompt(meta)
    print(prompt)