from base.baseBot import BaseBot
import asyncio


class MultiplePageBot(BaseBot):
    def __init__(self, sitename: str, username: str, password: str, api_loc: str):
        super().__init__(sitename, username, password, api_loc)
        self.__task_list = []
        self.result = []

    async def run_tasks(self):
        if self.__task_list:
            await asyncio.gather(*self.__task_list)

    async def __send_request(self, body, result_container):
        await asyncio.sleep(1)
        response = await self.client.post(self.url, data=body)
        result_container.append(response.json())

    def create_task(self, params):
        self.__task_list.append(asyncio.create_task(self.__send_request(params, self.result)))
