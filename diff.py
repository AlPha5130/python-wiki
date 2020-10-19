from base.baseBot import BaseBot
from bs4 import BeautifulSoup
from itertools import zip_longest
import asyncio


class DiffBot(BaseBot):
    def __init__(self, sitename, username, password, api_loc):
        super().__init__(sitename, username, password, api_loc)

    async def get_diff(self, old_id: int, new_id: int):
        cp_param = {
            "action": "compare",
            "fromrev": old_id,
            "torev": new_id,
            "format": "json"
        }
        data = await self.send_request(cp_param, 'get')
        content = self.__get_comp(data['compare']['*'])
        print(data)
        for line, deleted, added in zip_longest(content['diff-line'], content['deleted-context'], content['added-context'], fillvalue=''):
            print(line, deleted, added, sep='\n', end='\n\n')

    def __get_comp(self, compare_string):
        comparands = {'diff-line': [],
                      'deleted-context': [], 'added-context': []}
        soup = BeautifulSoup(compare_string, 'lxml')
        for change_type, css_class in (('diff-line', 'diff-lineno'), ('deleted-context', 'diff-deletedline'), ('added-context', 'diff-addedline')):
            crutons = soup.find_all('td', class_=css_class)
            for cruton in crutons:
                cruton_string = ''.join(cruton.strings)
                comparands[change_type].append(cruton_string)
        return comparands


if __name__ == '__main__':
    async def main():
        bot = DiffBot('https://minecraft-zh.gamepedia.com',
                      'MysticNebula70@Chino', 'sn32bd83spfd8ed9si6est1vpigp26sv', '/api.php')
        await bot.login()
        await bot.get_diff(460041, 466393)
        await bot.close()
        await asyncio.sleep(1)
    asyncio.run(main())
