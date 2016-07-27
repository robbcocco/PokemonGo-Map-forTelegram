import sys
import asyncio
import telepot
import telepot.aio
import os
import datetime
import time

from selenium import webdriver

"""
Run with
python3.5 bot.py <token> <PTC username> <PTC password> <steps> <host> <port> <gmaps key>

"""

async def handle(msg):
    global server_used
    chat_id = msg['chat']['id']
    command = msg['text']
    sender = msg['from']
    sender_id = msg['from']['id']
    if command.lower().startswith('/pokemap'):
        if command.count(' ') >= 1:
            # initialize the set
            if sender_id not in users:
                users[sender_id] = 0
            # print info
            print('Sender: ', sender)
            print('Command: ', command)
            print('Actual time: ', time.time())
            print('Latest use: ', users[sender_id])
            # check if the user has used the server in the last 10 minutes
            if time.time()-users[sender_id] > wait_time:
                # check if the server is being used
                if server_used is False:
                    # set the server as occupied
                    server_used = True
                    # update the time when the user used the server
                    users[sender_id] = time.time()
                    # save the location into a variable
                    locTemp = command.split(' ', 1)
                    location = locTemp[1]
                    # run the shell command
                    os.system('python2.7 PokemonGo-Map-1.0/example.py -a ptc -u %s -p %s -l "%s" -st %s -H %s -P %s >mapstd.txt 2>maperr.txt &' % (USER, PASS, location, STEP, HOST, PORT))
                    # let the map load a minute
                    await bot.sendMessage(chat_id, 'Wait two minutes...')
                    await asyncio.sleep(120)
                    # initialize the page
                    driver = webdriver.PhantomJS()
                    driver.set_window_size(512, 512)
                    driver.get('http://%s:%s' % (HOST, PORT))
                    # let the page load
                    await asyncio.sleep(6)
                    # save a screenshot
                    driver.save_screenshot('loc.png')
                    # kill the map
                    os.system('pkill -f example.py')
                    os.system('pkill -f python2.7')
                    os.system('pkill -f node')
                    os.system('pkill -f phantomjs')
                    # send the screenshot
                    await bot.sendChatAction(chat_id, 'upload_photo')
                    await bot.sendPhoto(chat_id, open('loc.png', 'rb'), caption=location)
                    # set the server as free
                    server_used = False
                else:
                    await bot.sendMessage(chat_id, 'Wait until i\'m avaiable')
                    # wait until the server is free
                    while(server_used is True):
                        await asyncio.sleep(1)
                    await bot.sendMessage(chat_id, 'I\'m now avaiable!')
            else:
                countdown = str(round(users[sender_id] + wait_time - time.time()))
                await bot.sendMessage(chat_id, 'Wait %s seconds until you can use me again' % countdown)
        else:
            await bot.sendMessage(chat_id, 'Correct syntax is "/pokemap location"')

    elif command.lower().startswith('/start'):
        await bot.sendMessage(chat_id, 'Hi! Try me with /pokemap')

    elif command.lower().startswith('/help'):
        await bot.sendMessage(chat_id,  'To get the map of a location with nearby Pokémon, just type\n' \
                                        '/pokemap followed by the desired location')


# get arguments from command-line
TOKEN = sys.argv[1]
USER = sys.argv[2]
PASS = sys.argv[3]
STEP = sys.argv[4]
HOST = sys.argv[5]
PORT = sys.argv[6]
GKEY = sys.argv[7]

# global variables
server_used = False
users = {}
wait_time = 600

bot = telepot.aio.Bot(TOKEN)
loop = asyncio.get_event_loop()

loop.create_task(bot.message_loop(handle))
print('Listening ...')

loop.run_forever()
