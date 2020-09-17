from base.multiplePageBot import MultiplePageBot
import asyncio


class CreateRedirectBot(MultiplePageBot):
    async def __init__(self, sitename, username, password, api_loc):
        await super().__init__(sitename, username, password, api_loc)

    async def create_redirect(self, file: str):
        client = self.client
        csrf_token_param = {
            "action": "query",
            "meta": "tokens",
            "format": "json"
        }
        response = await client.get(self.url, params=csrf_token_param)
        data = response.json()
        csrf_token = data['query']['tokens']['csrftoken']
        for p in open(file, 'r', encoding='utf8'):
            page = p.strip()
            dest_page = page[page.find(":") + 1:]
            create_param = {
                "action": "edit",
                "title": dest_page,
                "text": f"#重定向 [[{page}]]",
                "summary": f"机器人：创建重定向页面至[[{page}]]",
                "bot": True,
                "createonly": True,
                "format": "json",
                "token": csrf_token
            }
            self.create_task(create_param)
        await self.run_tasks()
        self.__handle_result()

    def __handle_result(self):
        for data in self.result:
            if 'edit' in data and data['edit']['result'] == 'Success':
                print(f"Successfully created page '{data['edit']['title']}'.")
            else:
                print(data)


if __name__ == '__main__':
    async def main():
        bot = await CreateRedirectBot('https://minecraft-zh.gamepedia.com',
                                      'MyNe70bot@Misaka', 'kgsvs6mil2hsqkorp9v5eec9f57c3tgs', '/api.php')
        await bot.create_redirect("page.txt")
        await asyncio.sleep(1)
    asyncio.run(main())
