import httpx
import asyncio


class BaseBot(object):
    '''
    Provide login and httpx client.
    '''

    def __init__(self, sitename: str, username: str, password: str, api_loc: str):
        self.__client = httpx.AsyncClient()
        self.__sitename = sitename
        self.__username = username
        self.__password = password
        self.__url = f'{sitename}{api_loc}'

    @property
    def sitename(self):
        return self.__sitename

    @property
    def username(self):
        return self.__username

    @property
    def url(self):
        return self.__url

    async def login(self):
        print(f'Logging into {self.sitename} ...')
        tokens = await self.get_token('login')
        login_token = tokens['logintoken']
        login_param = {
            "action": "login",
            "lgname": self.username,
            "lgpassword": self.__password,
            "format": "json",
            "lgtoken": login_token
        }
        data = await self.send_request(login_param, 'post')
        if data['login']['result'] == 'Success':
            print(f'Logged into {self.sitename} as {self.username}.')
        else:
            print("An error occurred.")
            print(data)
            raise RuntimeError("Failed logging in.") from None

    async def close(self):
        await self.__client.aclose()
    
    async def send_request(self, data, method):
        if method == 'get':
            response = await self.__client.get(self.url, params=data)
            return response.json()
        elif method == 'post':
            await asyncio.sleep(0.5)
            response = await self.__client.post(self.url, data=data)
            return response.json()

    async def get_token(self, type):
        token_param = {
            "action": "query",
            "meta": "tokens",
            "type": type,
            "format": "json",
        }
        data = await self.send_request(token_param, 'get')
        return data['query']['tokens']

    def print_page(self, page, **kwargs):
        print(f"\n>>> {page} <<<")
        if kwargs:
            print(*(f"{k}: {v}" for k, v in kwargs.items()),
                  sep='\n', end='\n\n')
