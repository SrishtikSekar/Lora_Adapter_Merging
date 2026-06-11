from safetensors.torch import load_file

def get_lora_deltas(repo_name: str, lora_alpha: int = 32, r: int = 16) -> dict:
    """Compute ΔW = lora_B @ lora_A * (alpha/r) directly from adapter weights."""
    from huggingface_hub import hf_hub_download

    path = hf_hub_download(
        repo_id  = f"Srishtik/{repo_name}",
        filename = "adapter_model.safetensors"
    )
    adapter_weights = load_file(path)
    scale = lora_alpha / r

    # Group A and B matrices by layer
    layers = {}
    for key, val in adapter_weights.items():
        if "lora_A" in key:
            base_key = key.replace("lora_A.default.weight", "").replace("lora_A.weight", "")
            layers.setdefault(base_key, {})["A"] = val.float()
        elif "lora_B" in key:
            base_key = key.replace("lora_B.default.weight", "").replace("lora_B.weight", "")
            layers.setdefault(base_key, {})["B"] = val.float()

    # Compute ΔW for each layer
    deltas = {}
    for base_key, mats in layers.items():
        if "A" in mats and "B" in mats:
            deltas[base_key] = scale * (mats["B"] @ mats["A"])  # (d_out, d_in)

    return deltas
