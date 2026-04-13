

- `parse_metadata.py` — parses GuitarPro (.gp5) files using PyGuitarPro and 
  extracts metadata including tempo, track names, and guitar techniques
- `generate_descriptions.py` — converts extracted metadata into natural language 
  descriptions used as training prompts
- `tokenizer.py` — encodes GuitarPro songs into a flat sequence of custom tokens 
  representing notes, durations, and techniques
- `build_dataset.py` — combines metadata descriptions and token sequences into a 
  HuggingFace dataset and pushes to the Hub
- `finetune.ipynb` — Colab notebook for fine-tuning TinyLlama 1.1B and Mistral 7B 
  using LoRA, and evaluating against GPT-4o baseline


The training dataset is available on HuggingFace: 
https://huggingface.co/datasets/asreekum/guitar-tab-dataset
