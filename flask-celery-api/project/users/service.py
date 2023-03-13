import random
import requests
from string import ascii_lowercase

class UserService:
    def random_username(self):
        username = ''.join([random.choice(ascii_lowercase) for i in range(5)])
        return username

    def api_call(self):
        # used for testing a failed api call
        if random.choice([0, 1]):
            raise Exception('random processing error')

        # used for simulating a call to a third-party api
        requests.post('https://httpbin.org/delay/5')
    
user_service = UserService()