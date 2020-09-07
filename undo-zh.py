import requests


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
    meta_token_param = {
        "action": "query",
        "meta": "tokens",
        "type": "csrf",
        "format": "json",
    }
    data = session.get(url=url, params=meta_token_param).json()
    csrf_token = data['query']['tokens']['csrftoken']
    page = input("Page name: ")
    page_query_param = {
        "action": "query",
        "prop": "revisions",
        "titles": page,
        "rvlimit": 1,
        "format": "json"
    }
    data = session.get(url=url, params=page_query_param).json()
    pages = data['query']['pages']
    if '-1' in pages.keys():
        print("Error: Page does not exist.")
    else:
        for k, v in pages.items():
            revision = v['revisions']
        revision = revision[0]
        print(f"User: {revision['user']}\nSummary: {revision['comment']}")
        if input("Undo this? [y/n]") == 'y':
            reason = input("Undo reason: ")
            revid = revision['revid']
            begin_rev = revision['parentid']
            undo_param = {
                "action": "edit",
                "title": page,
                "undo": revid,
                "undoafter": begin_rev,
                "token": csrf_token,
                "format": "json"
            }
            if reason != "":
                undo_param.update({"summary": reason})
            data = session.post(url, undo_param).json()
            print("Undone revision.")

if __name__ == "__main__":
    main()
