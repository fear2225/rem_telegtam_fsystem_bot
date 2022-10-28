# Remote access to the file system via Telegram Messager  
## Table of Contents  
1 Description  
2 Supported commands  
3 Installation guide  
4 Config.txt parameters  

## 1 Description  
A Telegram bot script that provides access to the computer's file system within the root directory. Also, remote shutdown of the bot and whitelist are available.
---  

## 2 Supported commands  
/start - start and show your user id  
/help - show help  
/root - go to root directory  
/ver - version of bot  
/list - whitelist  
/off - shutdown bot  

## 3 Installation guide  
To get bot token follow the link: https://t.me/botfather  
### Windows, using cmd  
1. Upgrade pip  
```
python -m pip install --upgrade pip
```
2. Upload dependence
```
pip install aiogram==2.22.2
pip install pathlib
```
3. Save config in main.py skript directory and edit 'TOKEN=' line
```
TOKEN=pasteHEREyourTOKEN
```
4. Run bot using the following command
```
python c:\path_to_main\main.py
```

---
## 4 Config.txt parameters  

TOKEN=token input field  
root=the directory you can't get out of  
max symbol in line=max symbols in inline telegram button (if file name is longer than this number, it take format:'werylongfi...name.example')  
max number of buttons=max number of inline buttons (not includes 'next' and 'up' buttons)  
whitelist=leave blank, or print users` ids dvided by ','  
