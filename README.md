# Password_vault

This is telegram bot designed for saving login and password for defined service.
Storage may be persistent or not. For this purpose two modules are described: 
  .storage_sqlite provides persistent storage using sqlite3 extension for python
  .storage_python provides non-persistent storage using simple python lists 
In default settings bot.py uses storage_sqlite and provides persistent storage.
If needed you can change this module to storage_python without changing another code: all functions are duplicated

Bot will be awailable for any user by link http://t.me/Ostanevich_password_vault_bot until my subscribe to VK Cloud will be expired
If you want to run this bot by another link get your unique token for telegram bot and put it into 'my token' variable in bot.py file

!Attention this bot was developed for educational purposes that's why I'm not responsible for the security of saved passwords
but this bot provides divided storage for different users and gives access by user_id got from telegram so it can be used to save not so important data

This repository remains open so I`ll be waiting for your commentaries and offers
