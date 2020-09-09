from base.multiplePageBot import MultiplePageBot
import asyncio


class CatdelBot(MultiplePageBot):
    def __init__(self, sitename, username, password, api_loc):
        super().__init__(sitename, username, password, api_loc)
        self.__cat = ''

    @property
    def category(self):
        return self.__cat

    @category.setter
    def category(self, value: str):
        self.__cat = value

    async def delete(self):
        tokens = await self.get_token('csrf')
        csrf_token = tokens['csrftoken']
        print("Retrieving pages...")
        page_query_param = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": self.category,
            "cmtype": "page|file",
            "cmlimit": 20,
            "format": "json"
        }
        entries = await self.query_page_loop(page_query_param, 'categorymembers')
        if len(entries) == 0:
            print("No pages or files.")
        else:
            for page in entries:
                self.print_page(page)
                if input("Delete this? [y/n] ") == 'y':
                    reason = input(
                        "Delete reason: ") or f"机器人：删除所有来自{self.category}分类的页面"
                    delete_param = {
                        "action": "delete",
                        "title": page['title'],
                        "token": csrf_token,
                        "reason": reason,
                        "format": "json"
                    }
                    self.create_task(delete_param, 'post')
            await self.run_tasks()
            self.__handle_result()

    def __handle_result(self):
        for item in self.result:
            print(item)


if __name__ == '__main__':
    async def main():
        bot = CatdelBot('https://minecraft-zh.gamepedia.com',
                        'MysticNebula70@Homura', 'j8ih3qkg1smjao81tstgd1l0ah03lveb', '/api.php')
        bot.category = 'Category:等待删除'
        await bot.login()
        await bot.delete()
        await bot.close()
        await asyncio.sleep(1)
    asyncio.run(main())
