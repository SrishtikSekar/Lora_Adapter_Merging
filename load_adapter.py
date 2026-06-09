from peft import set_peft_model_state_dict
from huggingface_hub import hf_hub_download
def load_adapter(huggingface_repo):
    model,tokenizer=FastLanguageModel.from_pretrained(
        model_name="unsloth/gemma-3-270m-it",
        max_seq_length=2048,
        load_in_4bit=True,
    )
    model=FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj","k_proj","v_proj","o_proj",
                       "up_proj","down_proj","gate_proj"],
        lora_alpha=32,
        lora_dropout=0,
        use_rslora=False,
    )
    try:
        model_weights=hf_hub_download(
         repo_id=f"Srishtik/{huggingface_repo}",
         filename="adapter_model.safetensors"
        )
    except:
        model_weights=hf_hub_download(
         repo_id=f"Srishtik/{huggingface_repo}",
         filename="adapter_model.bin"
        )
    from safetensors.torch import load_file
    model_weights=load_file(model_weights)
    set_peft_model_state_dict(model,model_weights)
    return model