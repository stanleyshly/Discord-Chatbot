# Jocy Bot

Guide for creating your own Jocy Bot

1) Create config.yml like

```
DISCORD_TOKEN: TOKEN
WHITELIST_CHANNEL: [CHANNELS]
TEMPERATURE: 0.9
MAX_MODEL_TOKEN_LEN: 1000
MAX_TOKEN_LEN_BEFORE_DELETE: 384
MODEL: "./output-medium/"
TOKENIZER: "microsoft/DialoGPT-medium"

```

Some scripts work like Lexi Bot but here are the steps for clarity

2) Create Discord Bot and find token, and find channels that the bot is allowed to respond in

3) Export all channels with Discord Chat Explorer in csv file format and place all ```.csv``` files into the ```csv``` folder.

4) Run ```csv_dictionary.py```, this creates ```alias.py```. This can be editted to give each user a "nickname", not really needed under current system. 

5) Then run ```csv_conversation.py``` but edit the ```username``` with the user to emulate speaking style, this creates ```processed-data.csv``` which needs to be uploaded to your root Google Drive for use on Colab. 

6) Upload ```DiabloGPT Bread.ipynb``` to drive and run on Colab with a GPU instance. 

7) Download the entire output folder that is created by the script after each cell is run.

8) Run ```discord_main_main.py```

9) Party(if it works)

10) Create if an issue if something is broken.