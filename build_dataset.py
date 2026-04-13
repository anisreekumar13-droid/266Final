import os
from datasets import Dataset
from tokenizer import encode_song
from generate_descriptions import extract_metadata, metadata_to_prompt

def techniques_match(prompt, output):
    technique_map = {
        "hammer-on": "hammer",
        "bend": "bend",
        "slide": "slide",
        "vibrato": "vibrato",
        "let ring": "let_ring",
        "palm mute": "palm_mute",
        "staccato": "staccato",
        "harmonic": "harmonic",
    }
    for natural, token in technique_map.items():
        if natural in prompt.lower() and token not in output:
            return False
    return True

def strip_leading_waits(tokens):
    """Remove leading empty measures before first note"""
    first_note_idx = 0
    for i, token in enumerate(tokens):
        if token.startswith("note:"):
            first_note_idx = i
            break
    
    # keep only tempo token and the new_track/new_measure immediately before first note
    header = [t for t in tokens[:first_note_idx]
              if t.startswith("tempo:") or t == "new_track"]
    
    # add one new_measure before the first note
    header.append("new_measure")
    
    return header + tokens[first_note_idx:]

def build_dataset(gp_files_dir, output_dir):
    examples = []
    skipped = 0
    technique_mismatch = 0

    files = [f for f in os.listdir(gp_files_dir)
             if f.endswith(('.gp3', '.gp4', '.gp5'))]

    print(f"Found {len(files)} files...")

    for filename in files:
        filepath = os.path.join(gp_files_dir, filename)
        try:
            meta = extract_metadata(filepath)
            prompt = metadata_to_prompt(meta)
            tokens = encode_song(filepath)
            tokens = strip_leading_waits(tokens)
            token_string = " ".join(tokens)

            if not techniques_match(prompt, token_string):
                technique_mismatch += 1
                continue

            examples.append({
                "instruction": "Generate guitar tablature in token format for the following description:",
                "input": prompt,
                "output": token_string,
            })
        except Exception as e:
            print(f"Skipping {filename}: {e}")
            skipped += 1
            continue

    print(f"Built {len(examples)} examples")
    print(f"Skipped (errors): {skipped}")
    print(f"Skipped (technique mismatch): {technique_mismatch}")

    ds = Dataset.from_list(examples)
    ds = ds.train_test_split(test_size=0.1, seed=42)
    ds.save_to_disk(output_dir)
    print(f"Saved dataset to {output_dir}")
    return ds

if __name__ == "__main__":
    ds = build_dataset("data/raw", "guitar_tab_dataset")
    print("Pushing to HuggingFace Hub...")
    ds.push_to_hub("asreekum/guitar-tab-dataset")
    print("Done!")