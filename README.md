# stfdecrypt.py
Decryptor and encryptor for savegames of the game Star Traders: Frontiers

This is a *python* implementation of decryptor and encryptor for savegames of the game 
[Star Traders: Frontiers](https://store.steampowered.com/app/335620/Star_Traders_Frontiers/).
In fact this is basicly python port of https://github.com/johndoe31415/startradersdecryptor 
with added encryption. BTW, execelent analysis, @johndoe31415 !

Tested on Windows 10 - Star Traders: Frontiers v3.1.9

## Install
* You need Python 3.5+ (see https://www.python.org/downloads/)
* You need CryptoPlus (see https://github.com/doegox/python-cryptoplus)
* Download this package to some local directory (and unzip if needed)

## Usage
Usage is shown when the program is invoked without parameters:

```
Usage: python stfdecrypt.py <action> <keyname> <infile> <outfile>
	Action can be one of 'encrypt' or 'decrypt'.
	Keyname can be one of 'core', 'data', 'game' or 'map'.
	Example: python stfdecrypt.py decrypt game game_6.db game_6_decrypted.db
```

The reverse operation (i.e. 'encrypt' = re-encoding a tampered savegame into a
format that Star Traders: Frontiers can use), is supported as well.

See decrypt_game.bat and encrypt_game.bat as examples (for Windows).

## Note
Decrypted game file can be edited by some SQL / SQLite clients:
* https://sqlite.org/cli.html
* https://sqlitebrowser.org/
* https://sqlitestudio.pl/
* and many more (including generic SQL clients like SQuirreL)...

See https://fearlessrevolution.com/viewtopic.php?t=5650 for some hints where/how to find and modify interesting values.
