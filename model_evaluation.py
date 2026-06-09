def evaluate_model_batched(model, tokenizer, test_data, n_samples=100, batch_size=16):
    correct = 0
    samples = test_data.select(range(n_samples))

    all_prompts = []
    all_expected = []

    for sample in samples:
        expected = label_map[sample["label"]]
        prompt = tokenizer.apply_chat_template(
            [{
                "role": "user",
                "content": f"Classify the emotion in this text into one of: sadness, joy, love, anger, fear, surprise.Give me only the emotion\n\nText: {sample['text']}"
            }],
            tokenize=False,
            add_generation_prompt=True,
        )
        all_prompts.append(prompt)
        all_expected.append(expected)

    for i in range(0, n_samples, batch_size):
        print(f"Batch {i//batch_size + 1}/{n_samples//batch_size}")  # progress
        batch_prompts  = all_prompts[i:i+batch_size]
        batch_expected = all_expected[i:i+batch_size]

        inputs = tokenizer(
            batch_prompts,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256,
        ).to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=8,
                do_sample=False,
                eos_token_id=tokenizer.eos_token_id,
                pad_token_id=tokenizer.pad_token_id if tokenizer.pad_token_id else tokenizer.eos_token_id,
                forced_eos_token_id=tokenizer.eos_token_id,
            )

        input_len = inputs["input_ids"].shape[1]
        for j, (output, expected) in enumerate(zip(outputs, batch_expected)):
                # Find actual end of this prompt using attention mask
                actual_input_len = inputs["attention_mask"][j].sum().item()
                generated = tokenizer.decode(
                    output[actual_input_len:], skip_special_tokens=True
                ).strip()
                prediction = extract_emotion(generated)
                if i + j < 5:
                        print(f"Expected: {expected} | Predicted: {prediction} | Match: {prediction == expected}")

                if prediction == expected:
                        correct += 1

    accuracy = correct / n_samples
    print(f"\nAccuracy: {accuracy:.4f}")
    return accuracy