import webbrowser
import sinaweibopy3
import csv
import time


def write_to_csv(url, data_list):
    with open(url, "a", newline="") as datacsv:
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        csvwriter.writerow(data_list)


def read_from_file(url):
    ids = []
    with open(url, "r") as f:
        for line in f.readlines():
            ids.append(line.strip('\n'))
    return ids


def main():
    try:
        # step 1 : sign a app in weibo and then define const app key,app srcret,redirect_url
        APP_KEY = '127174040'
        APP_SECRET = '2b483df41e57480249a35660b69dcf19'
        REDIRECT_URL = 'https://api.weibo.com/oauth2/default.html'
        # step 2 : get authorize url and code
        client = sinaweibopy3.APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=REDIRECT_URL)
        url = client.get_authorize_url()
        print(url)
        webbrowser.open_new(url)
        # step 3 : get Access Token
        # Copy the above address to the browser to run,
        # enter the account and password to authorize, the new URL contains code
        result = client.request_access_token(
            input("please input code : "))  # Enter the CODE obtained in the authorized address
        print(result)

        client.set_access_token(result.access_token, result.expires_in)

    except ValueError:
        print('pyOauth2Error')

    ids = read_from_file("2.txt")
    sids = read_from_file("ids.txt")
    # screen_names = []
    # for uid in ids:
    #     screen_name = client.get_user_info(uid)
    #     print(screen_name)
    #     screen_names.append(screen_name)
    # write_to_csv("test.csv", screen_names)

    for sid in sids:
        relationship = []
        print("sid: " + sid)
        for tid in ids:
                flag = client.get_friendships(sid, tid)
                print("tid: " + tid + ", flag: " + str(flag))
                if flag:
                    relationship.append('1')
                else:
                    relationship.append('0')
        write_to_csv('test.csv', relationship)


if __name__ == '__main__':
    main()
