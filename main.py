import json
import os
import aiohttp
import time

import asyncio


class Main:
    def __init__(self):
        self.GUILD_ID = input('[>] Guild ID: ')
        self.CHANNEL_ID = input('[>] Channel ID: ')
        self.MESSAGE_ID = input('[>] Message ID: ')
        REASON = input(
            '\n[1] Illegal content\n'
            '[2] Harassment\n'
            '[3] Spam or phishing links\n'
            '[4] Self-harm\n'
            '[5] NSFW content\n\n'
            '[>] Reason: '
        )

        if REASON.upper() in ('1', 'ILLEGAL CONTENT'):
            self.REASON = 0
        elif REASON.upper() in ('2', 'HARASSMENT'):
            self.REASON = 1
        elif REASON.upper() in ('3', 'SPAM OR PHISHING LINKS'):
            self.REASON = 2
        elif REASON.upper() in ('4', 'SELF-HARM'):
            self.REASON = 3
        elif REASON.upper() in ('5', 'NSFW CONTENT'):
            self.REASON = 4
        else:
            print('\n[!] Reason invalid.')
            os.system(
                'title [Discord Reporter] - Restart required &&'
                'pause >NUL &&'
                'title [Discord Reporter] - Exiting...'
            )
            time.sleep(3)
            os._exit(0)

        self.RESPONSES = {
            '401: Unauthorized': '[!] Invalid Discord token.',
            'Missing Access': '[!] Missing access to channel or guild.',
            'You need to verify your account in order to perform this action.': '[!] Unverified.'
        }
        self.sent = 0
        self.errors = 0

    async def _reporter(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                'https://discordapp.com/api/v8/report', json={
                    'channel_id': self.CHANNEL_ID,
                    'message_id': self.MESSAGE_ID,
                    'guild_id': self.GUILD_ID,
                    'reason': self.REASON
                }, headers={
                    'user-agent': 'Mozilla/5.0 (Linux; Android 8.1.0; GO1452 Build/OPM2.171019.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.110 Mobile Safari/537.36',
                    'authorization': self.TOKEN
                }
            ) as report:
                if (status := report.status) == 201:
                    self.sent += 1
                    print('[!] Reported successfully.')
                elif status in (401, 403):
                    self.errors += 1
                    print(self.RESPONSES[await report.json()['message']])
                else:
                    self.errors += 1
                    print(f'[!] Error: {await report.text()} | Status Code: {status}')

    def _update_title(self):
        while True:
            os.system(f'title [Discord Reporter] - Sent: {self.sent} ^| Errors: {self.errors}')
            time.sleep(0.1)

    async def _multi_threading(self):
        coros = [self._reporter() for _ in range(300)]
        await asyncio.gather(*coros)

    def setup(self):
        recognized = None
        if os.path.exists('config.json'):
            with open('config.json', 'r') as f:
                try:
                    data = json.load(f)
                    self.TOKEN = data['discordToken']
                except (KeyError, json.decoder.JSONDecodeError):
                    recognized = False
                else:
                    recognized = True
        else:
            recognized = False

        if not recognized:
            self.TOKEN = input('[>] Discord token: ')
            with open('config.json', 'w') as f:
                json.dump({'discordToken': self.TOKEN}, f)

        asyncio.run(self._multi_threading())


if __name__ == '__main__':
    os.system('cls && title [Discord Reporter] - Main Menu')
    main = Main()
    main.setup()