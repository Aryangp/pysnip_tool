import replicate


def prompt_llama2(message:str):
    pre_prompt = """You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond 
    once as 'Assistant'.Give a one line answer. 
    """
    prompt_input = message

    # Generate LLM response
    output = replicate.run('a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', # LLM model
                            input={"prompt": f"{pre_prompt} {prompt_input} Assistant: ", # Prompts
                            "temperature":0.1, "top_p":0.9, "max_length":168, "repetition_penalty":1})  # Model parameters


    full_response = ""

    for item in output:
      full_response += item

    return full_response

