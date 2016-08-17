# PokemonGo Map for Telegram

<p align="center">
<img src="https://raw.githubusercontent.com/robbcocco/PokemonGo-Map-forTelegram/master/cover.jpg">
</p>

Live visualization of all the pokemon in your area. To use with a Telegram Bot. Request one [here](https://telegram.me/BotFather).  Try it [here](https://telegram.me/PkmnGoMapBot).

[Official Website] (https://jz6.github.io/PoGoMap/)

[Map repo](https://github.com/PokemonGoMap/PokemonGo-Map/tree/develop)

Bot using API from [nickoala's telepot](https://github.com/nickoala/telepot).

---
##Instructions##

```
apt-get update
apt-get install -y build-essential
apt-get install libssl-dev openssl libreadline-dev
wget https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
tar zxf Python-3.5.2.tgz
cd Python-3.5.2
./configure
make
make install
pip3.5 install telepot
apt-get install -y python
apt-get install -y python-setuptools
wget https://bootstrap.pypa.io/get-pip.py
python2.7 get-pip.py
wget -qO- https://deb.nodesource.com/setup_6.x | bash -
apt-get install -y nodejs
npm -g install phantomjs
pip3.5 install selenium
apt-get install -y unzip
wget https://github.com/robbcocco/PokemonGo-Map-forTelegram/archive/master.zip
unzip master.zip
cd PokemonGo-Map-forTelegram-master/
wget https://github.com/PokemonGoMap/PokemonGo-Map/archive/V3.1.0.zip
unzip V3.1.0.zip
cd PokemonGo-Map-3.1.0/
pip2.7 install --upgrade -r requirements.txt
```

To get your Google Maps API key Check [this page](https://pgm.readthedocs.io/en/develop/basic-install/google-maps.html) to get your key.

Run from PokemonGo-Map-forTelegram/ with `python3.5 bot.py <TELEGRAM TOKEN> <PTC Username> <PTC Password> <Steps> <Host> <Port> <GMaps Key>`
