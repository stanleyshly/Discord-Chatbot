# the os module helps us access environment variables
# i.e., our API keys
import os

# these modules are for querying the Hugging Face model
import json
import requests

# the Discord Python API
import discord

import torch
import yaml



class MyClient(discord.Client):
    def __init__(self, config):
        super().__init__()
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
        self.config = config        
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(self.config["TOKENIZER"])
        #model = AutoModelWithLMHead.from_pretrained("microsoft/DialoGPT-small").to(device)
        self.model = AutoModelForCausalLM.from_pretrained(self.config["MODEL"]).to(self.device)


    def query(self, message):
        """
        make request to the Local model 
        """
        new_user_input_ids = self.tokenizer.encode(message + self.tokenizer.eos_token, return_tensors='pt').to(self.device)
        bot_input_ids = new_user_input_ids
        chat_history_ids = self.model.generate(
            bot_input_ids, max_length=200,
            pad_token_id=self.tokenizer.eos_token_id,  
            no_repeat_ngram_size=3,       
            do_sample=True, 
            top_k=100, 
            top_p=0.7,
            temperature=self.config["TEMPERATURE"]
        ).to(self.device)
        return self.tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)


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
          response = self.query(message.content)
        
        # send the model's response to the Discord channel
        if response:
            await message.channel.send(response)
        else:
            await message.channel.send("Hmm, Something Isn't quite working right")

def main():
    config = yaml.safe_load(open("./config.yml"))
    print(config)
    client = MyClient(config)
    client.run(config["DISCORD_TOKEN"])

if __name__ == '__main__':
  main()
