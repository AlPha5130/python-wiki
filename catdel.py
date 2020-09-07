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
        client = self.client
        meta_token_param = {
            "action": "query",
            "meta": "tokens",
            "type": "csrf",
            "format": "json",
        }
        response = await client.get(url=self.url, params=meta_token_param)
        data = response.json()
        csrf_token = data['query']['tokens']['csrftoken']
        print("Retrieving pages...")
        indicate = 1
        page_query_param = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": self.category,
            "cmtype": "page|file",
            "cmlimit": 20,
            "format": "json"
        }
        while indicate:
            response = await client.get(url=self.url, params=page_query_param)
            data = response.json()
            if 'continue' in data:
                cont_param = data['continue']
                page_query_param.update(cont_param)
            else:
                indicate = 0
            entries = data['query']['categorymembers']
            if len(entries) == 0:
                print("No pages or files.")
                indicate = 0
            else:
                for page in entries:
                    print(f"\nTitle: {page['title']}\n")
                    if input("Delete this? [y/n] ") == 'y':
                        reason = input("Delete reason: ")
                        if reason == "":
                            reason = f"机器人：删除所有来自{self.category}分类的页面"
                        delete_param = {
                            "action": "delete",
                            "title": page['title'],
                            "token": csrf_token,
                            "reason": reason,
                            "format": "json"
                        }
                        self.create_task(delete_param)
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
