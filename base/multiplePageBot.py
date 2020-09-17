from base.baseBot import BaseBot
import asyncio


class MultiplePageBot(BaseBot):
    def __init__(self, sitename: str, username: str, password: str, api_loc: str):
        super().__init__(sitename, username, password, api_loc)
        self.__task_list = []
        self.__result = []
        self.__batch_limit = 25

    @property
    def result(self):
        return self.__result

    @property
    def batch_limit(self):
        return self.__batch_limit

    @batch_limit.setter
    def batch_limit(self, value: int):
        self.__batch_limit = value

    async def run_tasks(self):
        batch = []
        for index, elem in enumerate(self.__task_list):
            if (index+1) % self.batch_limit == 0:
                await asyncio.gather(*batch)
                batch = []
            else:
                batch.append(elem)

    async def __send_request(self, data, method):
        self.__result.append(await self.send_request(data, method))

    def create_task(self, params, method):
        self.__task_list.append(asyncio.create_task(
            self.__send_request(params, method)))

    async def query_page_loop(self, query_param, result_key):
        looping = True
        result = []
        while looping:
            data = await self.send_request(query_param, 'get')
            if 'continue' in data:
                continue_param = data['continue']
                query_param.update(continue_param)
            else:
                looping = False
            pages = data['query'][result_key]
            if len(pages) == 0:
                looping = False
            else:
                result.extend(pages)
        return result
