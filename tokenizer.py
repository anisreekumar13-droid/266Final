import guitarpro
from parse_metadata import extract_techniques

DURATION_MAP = {
    1: "whole",
    2: "half",
    4: "quarter",
    8: "eighth",
    16: "sixteenth",
    32: "thirty_second"
}

def encode_song(filepath):
    song = guitarpro.parse(filepath)
    all_tokens = []

    all_tokens.append(f"tempo:{song.tempo}")

    for track in song.tracks:
        all_tokens.append("new_track")
        for measure in track.measures:
            all_tokens.append("new_measure")
            for voice in measure.voices:
                for beat in voice.beats:
                    duration = DURATION_MAP.get(beat.duration.value, f"d{beat.duration.value}")

                    is_chord = len(beat.notes) > 1
                    if is_chord:
                        all_tokens.append("chord_start")

                    for note in beat.notes:
                        token = f"note:s{note.string}:f{note.value}:{duration}"
                        all_tokens.append(token)

                        if note.effect.hammer:
                            all_tokens.append("hammer")
                        if note.effect.isBend:
                            all_tokens.append("bend")
                        if note.effect.slides:
                            all_tokens.append("slide")
                        if note.effect.vibrato:
                            all_tokens.append("vibrato")
                        if note.effect.letRing:
                            all_tokens.append("let_ring")
                        if note.effect.palmMute:
                            all_tokens.append("palm_mute")
                        if note.effect.staccato:
                            all_tokens.append("staccato")
                        if note.effect.isTremoloPicking:
                            all_tokens.append("tremolo_pick")
                        if note.effect.isTrill:
                            all_tokens.append("trill")
                        if note.effect.harmonic:
                            all_tokens.append("harmonic")

                    if is_chord:
                        all_tokens.append("chord_end")

                    all_tokens.append(f"wait:{duration}")

    return all_tokens

if __name__ == "__main__":
    import sys
    from generate_descriptions import extract_metadata, metadata_to_prompt

    filepath = sys.argv[1] if len(sys.argv) > 1 else "frankOcean.gp5"

    meta = extract_metadata(filepath)
    prompt = metadata_to_prompt(meta)
    tokens = encode_song(filepath)

    print("=== INPUT PROMPT ===")
    print(prompt)
    print("\n=== OUTPUT TOKENS (first 50) ===")
    print(" ".join(tokens[:50]))
    print(f"\nTotal tokens: {len(tokens)}")