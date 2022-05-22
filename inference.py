from transformers import (
    MODEL_WITH_LM_HEAD_MAPPING,
    WEIGHTS_NAME,
    AdamW,
    AutoConfig,
    PreTrainedModel,
    PreTrainedTokenizer,
    get_linear_schedule_with_warmup,
)
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import BlenderbotSmallTokenizer, BlenderbotSmallForCausalLM

import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
#tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-small')
#model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small").to(device)
#model = AutoModelForCausalLM.from_pretrained('./output-small/').to(device)

#tokenizer = BlenderbotSmallTokenizer.from_pretrained('facebook/blenderbot_small-90M')
#model = BlenderbotSmallForCausalLM.from_pretrained("./output").to(device)

tokenizer = AutoTokenizer.from_pretrained('microsoft/DialoGPT-medium')
model = AutoModelForCausalLM.from_pretrained('./output/').to(device)

# Let's chat for 4 lines
for step in range(50):
    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(str(input(">> User:")) + tokenizer.eos_token, return_tensors='pt').to(device)

    # append the new user input tokens to the chat history
    bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1).to(device) if step > 0 else new_user_input_ids

    #print(bot_input_ids)

    # generated a response while limiting the total chat history to 1000 tokens, 
    chat_history_ids = model.generate(
        bot_input_ids, max_length=200,
        pad_token_id=tokenizer.eos_token_id,  
        no_repeat_ngram_size=3,       
        do_sample=True, 
        top_k=100, 
        top_p=0.7,
        temperature=0.8
    ).to(device)
    
    # pretty print last ouput tokens from bot
    print("JocyBot: {}".format(tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)))

