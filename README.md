# LoRA Adapter Merging for LLMs

This repository contains a lightweight experimentation pipeline for training, loading, evaluating, and analyzing LoRA adapters for large language models, with a focus on adapter merging and layer-wise diagnostics. The code is built around Gemma-based models and uses the Unsloth + PEFT ecosystem for efficient fine-tuning.

It includes scripts for:

- training adapters with LoRA
- loading adapters from Hugging Face Hub
- extracting low-rank update matrices from trained adapters
- measuring per-layer update strength via Frobenius norm
- evaluating generated model outputs on custom datasets
- notebooks for adapter merging experiments and analyses

## Repository structure

- `train_adapter.py` — main adapter training script for Gemma using SFTTrainer
- `train_adapter_using_responses_gemma.py` — variant focused on response-only training patterns
- `load_adapter.py` — loads a Hugging Face adapter into a base model
- `extract_lora_deltas.py` — reconstructs LoRA delta matrices from adapter weights
- `frobenius_norm.py` — computes and plots per-layer Frobenius norms
- `model_evaluation.py` — batched evaluation helpers for model quality checks
- `notebooks/` — exploratory notebooks for adapter merging, evaluation, and layer ablation
- `docs/` — report assets and analysis artifacts

## Project goal

The repository explores the idea that many specialized adapters can be trained or merged to produce a model with combined abilities. The scripts support a workflow like this:

1. fine-tune a base model with LoRA on a target task or dataset
2. push the resulting adapter to Hugging Face
3. compute adapter delta matrices
4. analyze/update strength across layers
5. merge or compare adapters in experiments and notebooks

## Dependencies

This project expects a Python environment with:

- PyTorch
- transformers
- datasets
- peft
- trl
- unsloth
- huggingface_hub
- safetensors
- matplotlib
- wandb

A typical installation looks like:

```bash
pip install torch transformers datasets peft trl unsloth safetensors matplotlib wandb huggingface_hub
```

Depending on your hardware and CUDA setup, you may also need the correct PyTorch build and CUDA-enabled runtime.

## Authentication and model access

Several scripts expect Hugging Face access and may require a Hugging Face token for publishing adapters or downloading gated models.

```bash
huggingface-cli login
```

For model uploads, scripts call `push_to_hub` using a token variable such as `key`.

## Training workflow

The training scripts use a Gemma base model, typically `unsloth/gemma-3-270m-it`, and configure a LoRA setup with modules such as:

- `q_proj`
- `k_proj`
- `v_proj`
- `o_proj`
- `gate_proj`
- `up_proj`
- `down_proj`

Example training usage:

```python
from train_adapter import train_adapter

# dataset and test_dataset should be Hugging Face datasets
# output_dir is the local checkpoint folder name
# key is your Hugging Face token or write token
model = train_adapter(dataset, test_dataset, "my_adapter", key, n_steps=500, alpha=2e-4)
```

The script logs training curves to W&B, saves checkpoints, and uploads the adapter to the Hub.

## Loading an adapter

`load_adapter.py` downloads an adapter from a Hub repository and loads it into the base model with PEFT state restoration.

```python
from load_adapter import load_adapter

model = load_adapter("my_adapter_repo_name")
```

This is useful when evaluating a trained adapter without re-running the full training pipeline.

## Extracting LoRA deltas

LoRA fine-tuning can be expressed as an update of the form:

- ΔW = (alpha / r) * B @ A

The script `extract_lora_deltas.py` reconstructs those low-rank deltas directly from `lora_A` and `lora_B` weights. This makes it easier to compare adapter strength, inspect layer scaling, and investigate merging effects across layers.

```python
from extract_lora_deltas import get_lora_deltas

layers = get_lora_deltas("my_adapter_repo_name", lora_alpha=32, r=16)
print(layers.keys())
```

## Frobenius norm analysis

The `frobenius_norm.py` utility computes the Frobenius norm of each adapter delta and plots layer-wise update magnitudes.

```python
from extract_lora_deltas import get_lora_deltas
from frobenius_norm import frobenius_norm

weights = get_lora_deltas("my_adapter_repo_name")
frobenius_norm(weights)
```

This is useful for identifying which layers receive the strongest changes after fine-tuning.

## Evaluation workflow

`model_evaluation.py` contains a batched evaluation helper that:

- formats prompts using a chat template
- generates model responses with greedy decoding
- parses the model output into a label or class
- computes final accuracy over a sample set

This is intended for classification-style tasks where the model is expected to return a single label, such as emotion labels.

## Notebooks and experiments

The `notebooks/` folder contains more exploratory work around:

- LoRA adapter merging
- multi-adapter comparison
- layer ablation studies
- representation analysis
- model evaluation and reporting

The notebooks are useful for seeing full experimental workflows, including ablation trends, merged-model comparisons, and report generation.

## Recommended workflow

A practical sequence for this project is:

```bash
# 1. prepare dataset
# 2. run training
python train_adapter.py

# 3. load and inspect model
python -c "from load_adapter import load_adapter; model = load_adapter('my_adapter_repo_name')"

# 4. compute adapter deltas and norms
python -c "from extract_lora_deltas import get_lora_deltas; from frobenius_norm import frobenius_norm; d = get_lora_deltas('my_adapter_repo_name'); frobenius_norm(d)"
```

## Notes

- This repository is research-oriented and not a polished production library.
- Many scripts are meant to be adapted to your dataset and model setup.
- Training and evaluation can be resource-intensive and may require GPU-capable hardware.
- LoRA adapter formats and model checkpoints may differ depending on the target base model and the version of the training stack.

## License

This repository does not currently include a formal license file. If you plan to reuse or distribute the code, check the repository owner and applicable licensing terms before publishing derivative work.

## Citation / project context

This project sits in the area of parameter-efficient fine-tuning and model merging. The code is intended for experimental work on low-rank adaptation, adapter comparison, and knowledge composition across specialized LoRA modules.

