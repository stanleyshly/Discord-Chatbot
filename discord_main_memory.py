# the os module helps us access environment variables
# i.e., our API keys
import os

# these modules are for querying the Hugging Face model
import json
import requests

# the Discord Python API
import discord

import yaml
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
import torch


class MyClient(discord.Client):
    def __init__(self, config, conn):
        super().__init__()
        self.config = config
        self.conn = conn        


    async def on_ready(self):
        # print out information when the bot wakes up
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        """
        this function is called whenever the bot sees a message in a channel
        """
        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
            return

        if message.channel.id not in self.config["WHITELIST_CHANNEL"]:
            return
        # while the bot is waiting on a response from the model
        # set the its status as typing for user-friendliness
        
        async with message.channel.typing():
            self.conn.send([message.content])
            response = self.conn.recv()
        
        # send the model's response to the Discord channel
        if response:
            await message.channel.send(response)
        else:
            await message.channel.send("Hmm, something isn't quite working right")

def main(conn, config):
    client = MyClient(config, conn)
    client.run(config["DISCORD_TOKEN"])
def chatbot(conn, config):        
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(config["TOKENIZER"])
    #model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small").to(device)
    model = AutoModelForCausalLM.from_pretrained(config["MODEL"]).to(device)

    while True==True:
        # encode the new user input, add the eos_token and return a tensor in Pytorch
        message_recieved  = conn.recv() 
        new_user_input_ids = tokenizer.encode(str(message_recieved) + tokenizer.eos_token, return_tensors='pt').to(device)

        
        # append the new user input tokens to the chat history
        try:
            if bot_input_ids.shape[1]  > config["MAX_TOKEN_LEN_BEFORE_DELETE"]:
                bot_input_ids = new_user_input_ids
                print('resetting memory')
            else:
                bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1).to(device) 
        except:
            bot_input_ids = new_user_input_ids
            print('resetting memory')

        #print(bot_input_ids)

        # generated a response while limiting the total chat history to 1000 tokens, 
        # Max token length is 1024(but set 1000) for this model, other times it is 512 tokens for other model
        chat_history_ids = model.generate(
            bot_input_ids, max_length=config['MAX_MODEL_TOKEN_LEN'],
            pad_token_id=tokenizer.eos_token_id,  
            no_repeat_ngram_size=3,       
            do_sample=True, 
            top_k=100, 
            top_p=0.7,
            temperature=config['TEMPERATURE']
        ).to(device)
        
        print(bot_input_ids.shape)
        # pretty print last ouput tokens from bot
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        conn.send(response)

from multiprocessing import Process, Pipe

if __name__ == '__main__':
    config = yaml.safe_load(open("./config.yml"))
    parent_conn, child_conn = Pipe()
    p = Process(target=main, args=(child_conn,config,))
    p.start()
    q = Process(target=chatbot, args=(parent_conn,config,))
    q.start()
    
