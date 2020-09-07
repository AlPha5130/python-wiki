import requests
import time


def main():
    print("Logging in...")
    session = requests.Session()
    url = "https://minecraft-zh.gamepedia.com/api.php"
    meta_token_param = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }
    data = session.get(url=url, params=meta_token_param).json()
    login_token = data['query']['tokens']['logintoken']
    login_param = {
        "action": "login",
        "lgname": "MysticNebula70@Homura",
        "lgpassword": "j8ih3qkg1smjao81tstgd1l0ah03lveb",
        "format": "json",
        "lgtoken": login_token
    }
    data = session.post(url, login_param).json()
    login_param = {}
    token_param = {
        "action": "query",
        "meta": "tokens",
        "type": "csrf",
        "format": "json"
    }
    data = session.get(url=url, params=token_param).json()
    csrf_token = data['query']['tokens']['csrftoken']
    with open("broken.text~", 'r', encoding='utf8') as f:
        pages = (i.rstrip() for i in f.readlines())
    for page in pages:
        delete_param = {
            "action": "delete",
            "title": page,
            "reason": "机器人：删除未使用的重定向",
            "token": csrf_token,
            "format": "json"
        }
        data = session.post(url, delete_param).json()
        print(f"Deleted {page}.")
        time.sleep(3.0)


if __name__ == "__main__":
    main()
