def build_prompt(system_prompt, history, user_input):
    prompt = f"<|im_start|>system\n{system_prompt}<|im_end|>\n"

    # keep only last 8 turns
    for u, a in history[-8:]:
        prompt += f"<|im_start|>user\n{u}<|im_end|>\n"
        prompt += f"<|im_start|>assistant\n{a}<|im_end|>\n"

    prompt += f"<|im_start|>user\n{user_input}<|im_end|>\n"
    prompt += "<|im_start|>assistant\n"

    return prompt