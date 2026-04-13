import guitarpro

def extract_techniques(song):
    techniques = set()
    for track in song.tracks:
        for measure in track.measures:
            for voice in measure.voices:
                for beat in voice.beats:
                    if beat.effect.vibrato:
                        techniques.add("vibrato")
                    if beat.effect.isTremoloBar:
                        techniques.add("tremolo bar")
                    if beat.effect.fadeIn:
                        techniques.add("fade in")
                    for note in beat.notes:
                        if note.effect.hammer:
                            techniques.add("hammer-on")
                        if note.effect.palmMute:
                            techniques.add("palm mute")
                        if note.effect.slides:
                            techniques.add("slide")
                        if note.effect.vibrato:
                            techniques.add("vibrato")
                        if note.effect.isBend:
                            techniques.add("bend")
                        if note.effect.isTremoloPicking:
                            techniques.add("tremolo picking")
                        if note.effect.isTrill:
                            techniques.add("trill")
                        if note.effect.letRing:
                            techniques.add("let ring")
                        if note.effect.harmonic:
                            techniques.add("harmonic")
                        if note.effect.staccato:
                            techniques.add("staccato")
    return list(techniques)

if __name__ == "__main__":
    import sys
    filepath = sys.argv[1] if len(sys.argv) > 1 else "frankOcean.gp5"
    song = guitarpro.parse(filepath)
    meta = {
        "title": song.title,
        "artist": song.artist,
        "tempo": song.tempo,
        "tracks": [t.name for t in song.tracks],
        "num_measures": len(song.tracks[0].measures),
        "techniques": extract_techniques(song),
    }
    print(meta)