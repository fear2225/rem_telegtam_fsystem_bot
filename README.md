# Remote access to the file system via telegram  
## Content table  
1 Description  
2 Supported commands  
3 Installation guide  
4 Config.txt parameters  

## 1 Descripton  
A telegram bot script that provides access to the computer's file system within the root directory. Remote shutdown of the bot and whitelist is available.
---

## 2 Supported command  
/start - start and show your user id  
/help - show help  
/root - go to root directory  
/ver - version of bot  
/list - whitelist  
/off - shutdow bot  

## 3 Installation guide  
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
root=the directory you can't cog ouf of  
max symbol in line=max symbols in inline telegram button (if file name longer than this number, it's take format:'werylongfi...name.example')  
max number of buttons=max number of inline buttons (not includes 'next' and 'up' buttons)  
whitelist=leave blank, or print users id devided by ','  

