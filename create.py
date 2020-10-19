from base.multiplePageBot import MultiplePageBot
import asyncio


class CreateRedirectBot(MultiplePageBot):
    def __init__(self, sitename, username, password, api_loc):
        super().__init__(sitename, username, password, api_loc)

    async def create_redirect(self, file: str):
        tokens = await self.get_token('csrf')
        csrf_token = tokens['csrftoken']
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
            self.create_task(create_param, 'post')
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
        bot = CreateRedirectBot('https://minecraft-zh.gamepedia.com',
                                'MyNe70bot@Misaka', 'kgsvs6mil2hsqkorp9v5eec9f57c3tgs', '/api.php')
        await bot.login()
        await bot.create_redirect("list.txt")
        await asyncio.sleep(1)
    asyncio.run(main())
