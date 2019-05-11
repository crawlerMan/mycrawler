from instabot import Bot
from pymongo import MongoClient
client = MongoClient('localhost')
db = client.InstagramCrawl
import time
#from langdetect import detect as lanD
from textblob import TextBlob
import re
import emoji


bot = Bot()

#remove hashtag
def hashtaghEx(s):
    t = remove_emoji(s)
    return re.findall(r"#(\w+)", t)

#remove emoji from text
def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)


#joda kardan kalamat
def spliteKeyWord(s):
    return re.findall(r'[\dA-Za-z]+|[^\dA-Za-z\W]+', s, re.UNICODE)


#tashkhis zaban
def lanqdet(text):

    if text == None:
        return "null"

    lanList = []

    t = remove_emoji(text)
    i = spliteKeyWord(t)

    print(i)
    print(type(i))


    for j in i:
        try:
            b = TextBlob(j)
            x = b.detect_language()
            if x in lanList:
                pass
            else:
                lanList.append(x)
        except:
            print("Somethings was wrongs in lanq detect")


    if len(lanList) == 1:
        b = TextBlob(t)
        x = b.detect_language()
        return x
    else:
        return "multi"



def crawler(username):
    getfollowingListInfo(username)
    getfollowerListInfo(username)


def profileScrap(username):
    userId = bot.get_userid_from_username(username)
    medias = bot.get_total_user_medias(user_id=userId)

    for m in medias:
        coment = []
        coments = bot.get_media_comments(m)

        try:
            for c in coments:
                a = {"owner": username, "mediaID": m, "user_id": c["user_id"], "username": c["user"]["username"],
                     "full_name": c["user"]["full_name"], "text": c["text"]}
            coment.append(a)

        except:
            print("Somthings wrong in get comments...")

        try:
            likers = bot.get_media_likers(m)
        except:
            print("Somthings wrong in get likers...")

        try:
            info = bot.get_media_info(m)
            if len(info) == 0:
                data = {"owner": username, "mediaID": m, "likers": likers, "commntes": coment, "full_crawl": False}
                i = db.instagram_users_posts.insert_one(data)

            elif len(info) > 0:
                for i in info:
                    lande = lanqdet(i["caption"]["text"])
                    data = {"owner": username, "mediaID": m, "caption": i["caption"]["text"], "caption_lanq": lande,
                            "image": i["image_versions2"]["candidates"], "hashtags": hashtaghEx(i["caption"]["text"]),
                            "comment_likes_enabled": i["comment_likes_enabled"], "comment_count": i["comment_count"],
                            "caption_is_edited": i["caption_is_edited"], "like_count": i["like_count"],
                            "likers": likers,
                            "commntes": coment, "full_crawl": True}
                    i = db.instagram_users_posts.insert_one(data)
                    break
        except:
            print("Somthings wrong in get infes...")


def checkout(username):
    try:
        find = db.instagram_users.find({"username": username, "crawlStatus": True})
        findc = db.instagram_users.find({"username": username}).count()
    except:
        print("Somethings in database was wrongs...")

    try:
        if findc == 0:
            return True
        elif findc == 1:
            if find["crawlStatus"] == False:
                return True
            else:
                return False
        elif findc > 1:
            for i in find:
                if i["crawlStatus"] == False:
                    return True
                else:
                    return False
        else:
            return False
    except:
        print("Somethings was wrong!")
        pass


def startFunc():

    while True:
        username = input("plz type a username: \t")
        if checkout(username):
            try:
                x = db.instagram_users.insert({"username": username, "crawlStatus": False})
            except:
                print("Somethings in database was wrong....")
            break
        else:
            print("This username was crawled.\n")
            t = input("Do you want to try again?!(reply y or n)")
            if t == "y" or "yes" or "Y" or "Yes":
                pass
            else:
                break



def main():
    while True:
        find = db.instagram_users.find({"crawlStatus": False})
        findc = db.instagram_users.find({"crawlStatus": False}).count()
        if findc == 0:
            startFunc()
        elif findc > 0:
            for i in find:
                print("Start crawling %s" % i["username"])
                profileScrap(i["username"])
                crawler(i["username"])
                update = db.instagram_users.update({i["username"]}, {"crawlStatus": True})

    #print("End of instagram username lists...")
    # t = input("Do you have any username? (reply y or n")
    # if t == "y" or "yes" or "Y" or "Yes":
    #     startFunc()
    # else:





def getfollowingListInfo(username):

    following = bot.get_user_following(username)
    if len(following) > 0:
        data = {"username": username, "following_list": following}
        i = db.instagram_users_list.insert_one(data)

        y = 0
        g = 1
        for e in following:
            t = db.instagram_users.find({"owner": username, "type": "following", "user_id": int(e)}).count()
            if t == 0:
                following_de = bot.get_user_info(e)
                # print(following_de)
                o = following_de
                D = {"owner": username, "type": "following", "username": o["username"], "user_id": int(e),
                     "full_name": o["full_name"], "is_private": o["is_private"],
                     "follower_count": o["follower_count"], "following_count": o["following_count"],
                     "biography": o["biography"], "linke": o["external_url"], "profile_pic": o["profile_pic_url"]}
                i = db.instagram_users_info.insert_one(D)

                print("\n")
                print(str(g) + " - ")
                g = g + 1
                y = y + 1
                print("owner:%s" % username)
                print("username:%s" % o["username"])

                find = db.instagram_users.find({"username" : o["username"]}).count()
                if find == 0:
                    i2 = db.instagram_users.insert({"username": o["username"], "crawlStatus": False})

                time.sleep(10)
                if y > 70:
                    time.sleep(360)
                    y = 0
                    continue
            else:
                continue
    else:
        d = {"owner": username, "following list zero": True}
        o = db.instagram_skip_list.insert_one(d)




def getfollowerListInfo(username):
    follower = bot.get_user_followers(username)
    if len(follower) > 0:
        data = {"username": username, "follower_list": follower}
        i = db.merihach_user_follower_userid.insert_one(data)
        # for r in following:
        #    l = r
        y = 0
        g = 1
        for e in follower:
            t = db.instagram_users.find({"owner": username, "type": "follower", "user_id": int(e)}).count()
            if t == 0:
                following_de = bot.get_user_info(e)
                # print(following_de)
                o = following_de
                D = {"owner": username, "type": "follower", "username": o["username"], "user_id": int(e),
                     "full_name": o["full_name"], "is_private": o["is_private"],
                     "follower_count": o["follower_count"], "following_count": o["following_count"],
                     "biography": o["biography"], "linke": o["external_url"], "profile_pic": o["profile_pic_url"]}
                i = db.merihach_instagram_users.insert_one(D)
                print("\n")
                print(str(g) + " - ")
                g = g + 1
                y = y + 1
                print("owner:%s" % username)
                print("username:%s" % o["username"])

                find = db.instagram_users.find({"username": o["username"]}).count()
                if find == 0:
                    i2 = db.instagram_users.insert({"username": o["username"], "crawlStatus": False})


                time.sleep(10)
                if y > 70:
                    time.sleep(360)
                    y = 0
                    continue
            else:
                continue
    else:
        d = {"owner": username, "follower list zero": True}
        o = db.instagram_skip_list.insert_one(d)







if __name__ == "__main__":


    bot.login()
    main()
    print("Bye")






