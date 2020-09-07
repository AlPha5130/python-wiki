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
        client = self.client
        print(f'Logging into {self.sitename} ...')
        meta_token_param = {
            "action": "query",
            "meta": "tokens",
            "type": "login",
            "format": "json"
        }
        response = await client.get(url=self.url, params=meta_token_param)
        data = response.json()
        login_token = data['query']['tokens']['logintoken']
        login_param = {
            "action": "login",
            "lgname": self.username,
            "lgpassword": self.__password,
            "format": "json",
            "lgtoken": login_token
        }
        response = await client.post(self.url, data=login_param)
        data = response.json()
        if data['login']['result'] == 'Success':
            print(f'Logged into {self.sitename} as {self.username}.')
        else:
            print("An error occurred.")
            raise RuntimeError("Failed logging in.") from None

    async def close(self):
        await self.client.aclose()
