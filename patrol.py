from base.multiplePageBot import MultiplePageBot
import asyncio


class PatrolBot(MultiplePageBot):
    def __init__(self, sitename, username, password, api_loc):
        super().__init__(sitename, username, password, api_loc)

    async def patrol(self):
        tokens = await self.get_token('patrol|rollback')
        patrol_token = tokens['patroltoken']
        rollback_token = tokens['rollbacktoken']
        rc_query_param = {
            "action": "query",
            "list": "recentchanges",
            "rcdir": "newer",
            "rcshow": "!patrolled",
            "rcprop": "title|user|timestamp|ids|comment",
            "rclimit": 20,
            "format": "json"
        }
        print("Retrieving edits...")
        entries = await self.query_page_loop(rc_query_param, 'recentchanges')
        if len(entries) == 0:
            print("No unpatrolled edits.")
        else:
            for item in entries:
                props = {
                    "User": item['user'],
                    "Summary": item['comment'],
                    "Time": item['timestamp']
                }
                self.print_page(item['title'], props)
                action = '1'
                while action not in 'prn' or action == '':
                    action = input(
                        "What to do with this? [(p)atrol|(r)ollback|(n)othing] ")
                    if action not in 'prn' or action == '':
                        print("Sorry, try again.")
                if action == 'p':
                    patrol_param = {
                        "action": "patrol",
                        "rcid": item['rcid'],
                        "token": patrol_token,
                        "format": "json"
                    }
                    self.create_task(patrol_param, 'post')
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
                    self.create_task(rollback_param, 'post')
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
        await bot.patrol()
        await bot.close()
        await asyncio.sleep(1)
    asyncio.run(main())
