import sys
import asyncio
import telepot
import telepot.aio
import os
import datetime
import time
import subprocess
import signal

from telepot.aio.delegate import per_chat_id, create_open
from selenium import webdriver

"""
Run with
python3.5 bot.py <TELEGRAM TOKEN> <PTC Username> <PTC Password> <Steps> <Host> <Port> <GMaps Key>

"""


class PokeMap(telepot.aio.helper.ChatHandler):
    def __init__(self, seed_tuple, timeout):
        super(PokeMap, self).__init__(seed_tuple, timeout)

    def print_info(self, msg):
        # print info
        print('Sender: ', msg['from'])
        print('Command: ', msg['text'])
        print('Actual time: ', time.time())
        print('Msg time: ', msg['date'])
        print('Latest use: ', users[msg['from']['id']])

    async def run_server(self, msg, run_args):
        print('Result: run_server')
        # declare global variables
        global server_used
        # set the server as occupied
        server_used = True
        # update the time when the user used the server
        users[msg['from']['id']] = time.time()
        # save the location into a variable
        locTemp = msg['text'].split(' ', 1)
        location = locTemp[1]
        # run the shell command
        run_map = [
                'python2.7', 'PokemonGo-Map-2.2.0/runserver.py',
                '-a', 'ptc',
                '-u', run_args['user'],
                '-p', run_args['pass'],
                '-l', "%s" % location,
                '-st', run_args['step'],
                '-H', run_args['host'],
                '-P', run_args['port']
        ]
        with open('mapstd.txt', 'w') as mapstd:
            with open('maperr.txt', 'w') as maperr:
                process = subprocess.Popen(run_map, stdout=mapstd, stderr=maperr, preexec_fn=os.setsid)
        # let the map load
        await self.sender.sendMessage('Wait...')
        await asyncio.sleep(load_time)
        # initialize the page
        try:
            driver = webdriver.PhantomJS()
            driver.set_window_size(512, 512)
            driver.get('http://%s:%s' % (run_args['host'], run_args['port']))
            # let the page load
            await asyncio.sleep(6)
            # save a screenshot
            driver.save_screenshot('loc.png')
            # terminate the map
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
        except:
            print('WebDriverException')
            await self.sender.sendMessage('Something went wrong, try again! :c')
        else:
            # send the screenshot
            await self.sender.sendChatAction('upload_photo')
            await self.sender.sendPhoto(open('loc.png', 'rb'), caption=location+'\nispokemongodownornot.com')
        # set the server as free
        server_used = False

    async def wait_server(self, msg):
        print('Result: wait_server')
        await self.sender.sendMessage('Wait until i\'m avaiable')
        # wait until the server is free
        while(server_used is True):
            await asyncio.sleep(1)
        await self.sender.sendMessage('I\'m now avaiable!')

    async def wait_countdown(self, msg):
        print('Result: wait_server')
        countdown = round(users[msg['from']['id']] + wait_time - time.time())
        await self.sender.sendMessage('Wait %s seconds until you can use me again' % str(countdown))
        while (countdown > 0):
            countdown = round(users[msg['from']['id']] + wait_time - time.time())
            await asyncio.sleep(1)
        await self.sender.sendMessage('You can now use me again!')


    async def on_chat_message(self, msg):
        if 'text' in msg:
            if msg['text'].lower().startswith('/pokemap'):
                if msg['text'].count(' ') >= 1:
                    # initialize the set
                    if msg['from']['id'] not in users:
                        users[msg['from']['id']] = 0
                    self.print_info(msg)
                    # avoid old messages
                    if time.time()-msg['date'] < 15 or msg['from']['id'] in whitelist:
                        # check if the user has used the server recently of if he is in the whitelist
                        if time.time()-users[msg['from']['id']] > wait_time or msg['from']['id'] in whitelist:
                            # check if the server is being used
                            if server_used is False:
                                # send the screenshot if there is a free server
                                await self.run_server(msg, run_args)
                            else:
                                # else send a message when a server is unused
                                await self.wait_server(msg)
                        else:
                            # else send a message when he can use it again
                            await self.wait_countdown(msg)
                else:
                    await self.sender.sendMessage('Correct syntax is "/pokemap location"')


            elif msg['text'].lower().startswith('/start'):
                await self.sender.sendMessage('Hi! Try me with /pokemap')

            elif msg['text'].lower().startswith('/help'):
                await self.sender.sendMessage(  'To get the map of a location with nearby Pokémon, just type\n' \
                                                '/pokemap followed by the desired location')

    async def on_edited_chat_message(self, msg):
        pass


TOKEN = sys.argv[1]  # get token from command-line

# global variables
server_used = False
run_args = {
        'user' : sys.argv[2],
        'pass' : sys.argv[3],
        'step' : sys.argv[4],
        'host' : sys.argv[5],
        'port' : sys.argv[6],
        'gkey' : sys.argv[7]
}
users = {}
whitelist = []  # add here your telegram id
wait_time = 600
load_time = 120

bot = telepot.aio.DelegatorBot(TOKEN, [
    (per_chat_id(), create_open(PokeMap, timeout=3600)),
])

loop = asyncio.get_event_loop()
loop.create_task(bot.message_loop())
print('Listening ...')

loop.run_forever()
