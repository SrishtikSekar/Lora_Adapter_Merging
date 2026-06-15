from trl import SFTTrainer, SFTConfig
import torch
import matplotlib.pyplot as plt

def train_adapter(dataset,test_dataset,output_dir,key):
    wandb.init(
        project="gemma-dair-ai-finetuned_on_25K",
        name=output_dir,
        config={
            "model": "gemma-3-270m-it",
            "r": 16,
            "lora_alpha": 32,
            "max_steps": 3125,
            "learning_rate": 2e-4,
            "batch_size": 2,
            "gradient_accumulation_steps": 4,
            "warmup_steps": 5,
            "weight_decay": 0.001,
            "lr_scheduler": "linear",
            "max_seq_length": 1024,
        }
    )
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name="unsloth/gemma-3-270m-it",
        max_seq_length=1024,
        load_in_4bit=True,
    )
    model = FastLanguageModel.get_peft_model(
        model,
        r=16,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                        "gate_proj", "up_proj", "down_proj"],
        lora_alpha=32,
        lora_dropout=0,
        bias="none",
        use_gradient_checkpointing="unsloth",
        random_state=3407,
        use_rslora=False,
        loftq_config=None,
    )
    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=dataset,
        eval_dataset=test_dataset,
        args=SFTConfig(
            dataset_text_field="texts",
            per_device_train_batch_size=2,
            gradient_accumulation_steps=4,
            warmup_steps=5,
            max_steps=250,
            learning_rate=2e-4,
            logging_steps=5,
            optim="adamw_8bit",
            weight_decay=0.001,
            lr_scheduler_type="linear",
            seed=3407,
            report_to="wandb",       # changed from "none"
            padding_free=False,
            output_dir=output_dir,
            save_strategy="steps",
            save_steps=125,
            save_total_limit=5,
            eval_strategy="steps",
            eval_steps=20,
            max_grad_norm=1.0,
            logging_nan_inf_filter=False,
        )
    )
    from unsloth.chat_templates import train_on_responses_only

    trainer = train_on_responses_only(
        trainer,
        instruction_part="<start_of_turn>user\n",
        response_part="<start_of_turn>model\n",
    )
    trainer.train()
    log_history=trainer.state.log_history
    steps      = [e["step"] for e in log_history if "loss" in e and "eval_loss" not in e]
    losses     = [e["loss"] for e in log_history if "loss" in e and "eval_loss" not in e]
    grad_steps = [e["step"] for e in log_history if "grad_norm" in e]
    grad_norms = [e["grad_norm"] for e in log_history if "grad_norm" in e]
    eval_steps  = [e["step"] for e in log_history if "eval_loss" in e]
    eval_losses = [e["eval_loss"] for e in log_history if "eval_loss" in e]

    # Plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ax1.plot(steps, losses, color="steelblue", label="Train Loss")
    if eval_losses:
        ax1.plot(eval_steps, eval_losses, color="red",
                 linestyle="--", marker="o", label="Eval Loss")
    ax1.set_ylabel("Loss")
    ax1.set_title(f"Training Curves — {output_dir}")
    ax1.legend()
    ax1.grid(True)

    ax2.plot(grad_steps, grad_norms, color="darkorange")
    ax2.set_ylabel("Gradient Norm")
    ax2.set_xlabel("Steps")
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(f"{output_dir}_curves.png")
    wandb.log({"training_curves": wandb.Image(f"{output_dir}_curves.png")})
    plt.show()
    wandb.finish()

    model.save_pretrained(output_dir)
    model.push_to_hub(f"Srishtik/{output_dir}",token=key)
    tokenizer.push_to_hub(f"Srishtik/{output_dir}",token=key)