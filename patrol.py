from base.multiplePageBot import MultiplePageBot
import asyncio


class PatrolBot(MultiplePageBot):
    def __init__(self, sitename, username, password, api_loc):
        super().__init__(sitename, username, password, api_loc)

    async def Patrol(self):
        client = self.client
        meta_token_param = {
            "action": "query",
            "meta": "tokens",
            "type": "patrol|rollback",
            "format": "json",
        }
        response = await client.get(url=self.url, params=meta_token_param)
        data = response.json()
        patrol_token = data['query']['tokens']['patroltoken']
        rollback_token = data['query']['tokens']['rollbacktoken']

        print("Retrieving edits...")
        indicate = 1
        rc_query_param = {
            "action": "query",
            "list": "recentchanges",
            "rcdir": "newer",
            "rcshow": "!patrolled",
            "rcprop": "title|user|timestamp|ids|comment",
            "rclimit": 20,
            "format": "json"
        }
        while indicate:
            response = await client.get(url=self.url, params=rc_query_param)
            data = response.json()
            if 'continue' in data:
                cont_param = data['continue']
                rc_query_param.update(cont_param)
            else:
                indicate = 0
            entries = data['query']['recentchanges']
            if len(entries) == 0:
                print("No unpatrolled edits.")
                indicate = 0
            else:
                for item in entries:
                    print()
                    print(f" {item['title']} ".center(36, '='))
                    print(
                        f"User: {item['user']}\nSummary: {item['comment']}\nTime: {item['timestamp']}\n")
                    action = '1'
                    while action not in 'prn' or action == '':
                        action = input(
                            "What to do with this? [(p)atrol|(r)ollback|(n)othing]")
                        if action not in 'prn' or action == '':
                            print("Sorry, try again.")
                    if action == 'p':
                        patrol_param = {
                            "action": "patrol",
                            "rcid": item['rcid'],
                            "token": patrol_token,
                            "format": "json"
                        }
                        self.create_task(patrol_param)
                    elif action == 'r':
                        reason = input("Rollback reason (Default: <none>):")
                        rollback_param = {
                            "action": "rollback",
                            "title": item['title'],
                            "user": item['user'],
                            "token": rollback_token,
                            "format": "json"
                        }
                        if reason != "":
                            rollback_param["summary"] = reason
                        self.create_task(rollback_param)
        await self.run_tasks()
        self.__handle_result()

    def __handle_result(self):
        print()
        for item in self.result:
            if 'patrol' in item:
                print(f"Patrolled {item['patrol']['title']}.")
            else:
                print(item)


if __name__ == "__main__":
    async def main():
        bot = PatrolBot('https://minecraft-zh.gamepedia.com',
                        'MysticNebula70@Chino', 'sn32bd83spfd8ed9si6est1vpigp26sv', '/api.php')
        await bot.login()
        await bot.Patrol()
        await bot.close()
        await asyncio.sleep(1)
    asyncio.run(main())
