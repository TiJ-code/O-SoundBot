# SoundBot
This is a sound bot. It can be used to play music on a server 24/7.\
However, it plays a special track every half and full hour.\
Can be used ideally on e.g. roleplay servers for news.

## Manual: Setup the bot

#### 1. Setup *config.json* file
Put your Token, and the necessary IDs in the given fields.

### **IMAGES OUTDATED**
#### 2. Install ffmpeg [WINDOWS]
Download [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip) and unzip it.


#### 3. Setup ffmpeg [WINDOWS]
Create a folder with the name "ffmpeg" on the same level as the Bot Python file.\
![The newly created 'ffmpeg' directory](https://i.imgur.com/rh4NBQ0.png)\
Now copy the 'bin' folder from the unpacked ffmpeg folder into the newly created one.\
(Test is only a test folder i created for this showing purpose, this is also where the bot sits)\
![The 'bin' folder inside of the newly created 'ffmpeg' directory](https://i.imgur.com/tziMw3r.png)
![The files inside the 'bin' folder](https://i.imgur.com/EXFRRSe.png)


#### 4. Using
Do not forget to install all the dependencies that the bot will need.
```
pip install -r requirements.txt
or
pip3 install -r requirements.txt
```
