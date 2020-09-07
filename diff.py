import base
from bs4 import BeautifulSoup
import requests
from itertools import zip_longest


class DiffBot(base.Automatic):
    def __init__(self, sitename, username, password, api_loc):
        super().__init__(sitename, username, password, api_loc)

    def get_diff(self, old_id: int, new_id: int):
        session = self.session
        cp_param = {
            "action": "compare",
            "fromrev": old_id,
            "torev": new_id,
            "format": "json"
        }
        data = session.get(url=self.url, params=cp_param).json()
        content = self.__get_comp(data['compare']['*'])
        for deleted, added in zip_longest(content['deleted-context'], content['added-context'], fillvalue=''):
            print(deleted, added, sep='\n', end='\n\n')

    def __get_comp(self, compare_string):
        comparands = {'deleted-context': [], 'added-context': []}
        soup = BeautifulSoup(compare_string, 'lxml')
        for change_type, css_class in (('deleted-context', 'diff-deletedline'),
                                       ('added-context', 'diff-addedline')):
            crutons = soup.find_all('td', class_=css_class)
            for cruton in crutons:
                cruton_string = ''.join(cruton.strings)
                comparands[change_type].append(cruton_string)
        return comparands


if __name__ == '__main__':
    bot = DiffBot('https://minecraft-zh.gamepedia.com',
                  'MysticNebula70@Chino', 'sn32bd83spfd8ed9si6est1vpigp26sv', '/api.php')
    bot.get_diff(460041, 466393)
