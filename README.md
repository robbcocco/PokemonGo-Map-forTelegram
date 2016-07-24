# PokemonGo Map for Telegram

<p align="center">
<img src="http://i.imgur.com/L1YZQBq.jpg">
</p>

Live visualization of all the pokemon in your area. To use with a Telegram Bot. Request one [here](https://telegram.me/BotFather).

[Official Website] (https://jz6.github.io/PoGoMap/)

[Map repo](https://github.com/AHAAAAAAA/PokemonGo-Map/tree/develop)

Bot using API from [nickoala's telepot](https://github.com/nickoala/telepot).

---
##Instructions##

```
apt-get update
apt-get install -y build-essential
apt-get install -y python3
apt-get install -y python3-setuptools
apt-get install -y python
apt-get install -y python-setuptools
wget https://bootstrap.pypa.io/get-pip.py
python3.4 get-pip.py
python2.7 get-pip.py
pip3.4 install telepot
wget -qO- https://deb.nodesource.com/setup_6.x | bash -
apt-get install -y nodejs
npm -g install phantomjs
pip3.4 install selenium
apt-get install -y unzip
wget https://github.com/robbcocco/PokemonGo-Map-forTelegram/archive/master.zip
unzip master.zip
cd PokemonGo-Map-forTelegram-master/
wget https://github.com/AHAAAAAAA/PokemonGo-Map/archive/V1.0.zip
unzip V1.0.zip
cd PokemonGo-Map-1.0/
pip2.7 install --upgrade -r requirements.txt
```

Add your Google Maps API key to credentials.json. Check [this page](https://github.com/AHAAAAAAA/PokemonGo-Map/wiki/Google-Maps-API:-a-brief-guide-to-your-own-key) to get your key.

Run from PokemonGo-Map-forTelegram/ with `python3.4 bot.py <token> <PTC username> <PTC password> <steps> <host> <port>`
