from datasets import load_from_disk

ds = load_from_disk("guitar_tab_dataset")

both = sum(1 for ex in ds['train'] 
           if 'slide' in ex['input'].lower() and 'slide' in ex['output'])
input_only = sum(1 for ex in ds['train'] 
                 if 'slide' in ex['input'].lower() and 'slide' not in ex['output'])
output_only = sum(1 for ex in ds['train'] 
                  if 'slide' not in ex['input'].lower() and 'slide' in ex['output'])

print(f"slide in BOTH prompt and output: {both}/{len(ds['train'])}")
print(f"slide in prompt ONLY: {input_only}")
print(f"slide in output ONLY: {output_only}")

# also print a few examples that have slide in both
print("\n=== Sample training examples with slide ===")
count = 0
for ex in ds['train']:
    if 'slide' in ex['input'].lower() and 'slide' in ex['output']:
        print(f"\nInput: {ex['input']}")
        print(f"Output snippet: {' '.join(ex['output'].split()[:30])}")
        count += 1
        if count >= 3:
            break