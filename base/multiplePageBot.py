from base.baseBot import BaseBot
import asyncio


class MultiplePageBot(BaseBot):
    def __init__(self, sitename: str, username: str, password: str, api_loc: str):
        super().__init__(sitename, username, password, api_loc)
        self.__result = []
        self.__queue = asyncio.Queue()

    @property
    def result(self):
        return self.__result

    async def handle_task(self):
        while True:
            task = await self.__queue.get()
            await task
            self.__queue.task_done()
            await asyncio.sleep(1)


    async def run_tasks(self):
        tasks = []
        for _ in range(5):
            task = asyncio.create_task(self.handle_task())
            tasks.append(task)
        await self.__queue.join()
        for task in tasks:
                task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)

    def create_task(self, params, method):
        self.__queue.put_nowait(self.__gather_result(params, method))

    async def __gather_result(self, params, method):
        result = await self.send_request(params, method)
        print(result)
        self.__result.append(result)
