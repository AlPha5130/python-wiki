import httpx
import asyncio


class BaseBot(object):
    '''
    Provide login and httpx client.
    '''

    def __init__(self, sitename: str, username: str, password: str, api_loc: str):
        self.client = httpx.AsyncClient()
        self.__sitename = sitename
        self.__api_loc = api_loc
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
        login_token = await self.get_token('login')['logintoken']
        login_param = {
            "action": "login",
            "lgname": self.username,
            "lgpassword": self.__password,
            "format": "json",
            "lgtoken": login_token
        }
        response = await self.client.post(self.url, data=login_param)
        data = response.json()
        if data['login']['result'] == 'Success':
            print(f'Logged into {self.sitename} as {self.username}.')
        else:
            print("An error occurred.")
            raise RuntimeError("Failed logging in.") from None

    async def close(self):
        await self.client.aclose()

    async def get_token(self, type):
        token_param = {
            "action": "query",
            "meta": "tokens",
            "type": type,
            "format": "json",
        }
        response = await self.client.get(url=self.url, params=token_param)
        data = response.json()
        return data['query']['tokens']
