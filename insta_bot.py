from instabot import Bot
from pymongo import MongoClient
client = MongoClient('localhost')
db = client.followers
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


    for j in i:
        try:
            b = TextBlob(j)
            x = b.detect_language()
            if x in lanList:
                pass
            else:
                lanList.append(x)
        except:
            print("Somethings was wrongs")


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
        info = bot.get_media_info(m)
        coments = bot.get_media_comments(m)
        for c in coments:
            a = {"user_id":c["user_id"],"text":c["text"],"username":c["user"]["username"],"full_name":c["user"]["full_name"]}
            coment.append(a)
        print(coments)
        likers = bot.get_media_likers(m)
        for i in info:
            data = {"caption": i["caption"]["text"], "caption_lanq": lanqdet(i["caption"]["text"]),
                    "image": i["image_versions2"]["candidates"], "hashtags": hashtaghEx(i["caption"]["text"]),
                    "comment_likes_enabled": i["comment_likes_enabled"], "comment_count": i["comment_count"],
                    "caption_is_edited": i["caption_is_edited"], "like_count": i["like_count"],"likers":likers,"commntes":coment}

            print(data)
            break





    for i in medias:


        # commenters = bot.get_media_commenters(i)
        # likers = bot.get_media_likers(i)
        # comment2 = bot.getMediaComments(i)
        # like2 = bot.getMediaLikers(i)

        print("coments: \n")
        for m in coments:
            print(m["text"])







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
    #medias = bot.get_total_user_medias(user_id=5428544314)
    #x = bot.get_media_info(media_id=2041231681750784644)
    y = [{'taken_at': 1498907201, 'pk': 1549268351635790796, 'id': '1549268351635790796_5428544314', 'device_timestamp': 1498906599446, 'media_type': 1, 'code': 'BWAG1uBAZvM', 'client_cache_key': 'MTU0OTI2ODM1MTYzNTc5MDc5Ng==.2', 'filter_type': 613, 'comment_likes_enabled': True, 'comment_threading_enabled': False, 'has_more_comments': True, 'max_num_visible_preview_comments': 2, 'preview_comments': [], 'can_view_more_preview_comments': False, 'comment_count': 12, 'inline_composer_display_condition': 'impression_trigger',
          'image_versions2': {'candidates': [{'width': 1080, 'height': 1080, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/84b36ed927442e92b0c99b24d80eaefd/5D6883A8/t51.2885-15/e35/19623341_1861156204145513_3166663495961804800_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&se=7&ig_cache_key=MTU0OTI2ODM1MTYzNTc5MDc5Ng%3D%3D.2'}, {'width': 480, 'height': 480, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/5ac4870c1a8065e74c7173e212fc6a1d/5D53DCA8/t51.2885-15/e35/s480x480/19623341_1861156204145513_3166663495961804800_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&ig_cache_key=MTU0OTI2ODM1MTYzNTc5MDc5Ng%3D%3D.2'}]}, 'original_width': 1080, 'original_height': 1080, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'can_viewer_reshare': True,
          'caption_is_edited': True, 'like_count': 70, 'has_liked': False, 'top_likers': [], 'direct_reply_to_author_enabled': True, 'photo_of_you': False, 'usertags': {'in': []}, 'caption': {'pk': 17887495714016309, 'user_id': 5428544314, 'text': 'Ons huisje 💚🏠 #ourplace #ourhouse #house #houses #homesweethome #huisjekijken #huis #wooninspiratie #myhouse #homeimprovment #huisje #happy #green #plant #plantsofinstagram #trees #tuin #tuininspiratie #voortuin #tuinen', 'type': 1, 'created_at': 1498908342, 'created_at_utc': 1498908342, 'content_type': 'comment', 'status': 'Active', 'bit_flags': 0, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'did_report_as_spam': False, 'share_enabled': False, 'media_id': 1549268351635790796}, 'can_viewer_save': True, 'organic_tracking_token': 'eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiZDBlZWY4MDJjNDhhNDMzN2E2YmM3NTczNTliMmFhNmIxNTQ5MjY4MzUxNjM1NzkwNzk2Iiwic2VydmVyX3Rva2VuIjoiMTU1NzU3MDYzNDQyNXwxNTQ5MjY4MzUxNjM1NzkwNzk2fDY4ODY3MDQxMDN8ZGNkZmJmNmJlYTg4ODM5OTUxZWQ5OWQyMDBiZWI3ODdlZmMzYTQ2NmFhYTliNTk5YzIwM2FmMTcxNjA2ZTNkYyJ9LCJzaWduYXR1cmUiOiIifQ=='}, {'taken_at': 1498019332, 'pk': 1541820364634527697, 'id': '1541820364634527697_5428544314', 'device_timestamp': 1498019111159, 'media_type': 1, 'code': 'BVlpXPlgRfR', 'client_cache_key': 'MTU0MTgyMDM2NDYzNDUyNzY5Nw==.2', 'filter_type': 0, 'comment_likes_enabled': True, 'comment_threading_enabled': False, 'has_more_comments': True, 'max_num_visible_preview_comments': 2, 'preview_comments': [], 'can_view_more_preview_comments': False, 'comment_count': 3, 'inline_composer_display_condition': 'impression_trigger', 'image_versions2': {'candidates': [{'width': 1080, 'height': 1350, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/4111a7487f3cc98e7b9491cffba19de5/5D75317F/t51.2885-15/e35/19367108_552604175128801_8179365980841967616_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&se=7&ig_cache_key=MTU0MTgyMDM2NDYzNDUyNzY5Nw%3D%3D.2'}, {'width': 480, 'height': 600, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/d790dd8c446384f0fb4e71d84cb5a8a6/5D58BE84/t51.2885-15/e35/p480x480/19367108_552604175128801_8179365980841967616_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&ig_cache_key=MTU0MTgyMDM2NDYzNDUyNzY5Nw%3D%3D.2'}]}, 'original_width': 1080, 'original_height': 1350, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'can_viewer_reshare': True, 'caption_is_edited': True, 'like_count': 126, 'has_liked': False, 'top_likers': [], 'direct_reply_to_author_enabled': True, 'photo_of_you': False, 'usertags': {'in': []}, 'caption': {'pk': 17859861862164987, 'user_id': 5428544314, 'text': 'Ff genieten van een koffie. Straks naar de camping met groep 7 . Mooi weer erbij 🏕 🌞\n#lovemyjob #flower #flowers #bloemen #bloem #green #interiorforyou #interieurjunkie #interior #interieur #wooninspiratie #woontrends #huisjekijken #binnenkijken #happy #cactus #plantsofinstagram #plants #mijnwestwingstijl', 'type': 1, 'created_at': 1498040011, 'created_at_utc': 1498040011, 'content_type': 'comment', 'status': 'Active', 'bit_flags': 0, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'did_report_as_spam': False, 'share_enabled': False, 'media_id': 1541820364634527697}, 'can_viewer_save': True, 'organic_tracking_token': 'eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiZDBlZWY4MDJjNDhhNDMzN2E2YmM3NTczNTliMmFhNmIxNTQxODIwMzY0NjM0NTI3Njk3Iiwic2VydmVyX3Rva2VuIjoiMTU1NzU3MDYzNDQyN3wxNTQxODIwMzY0NjM0NTI3Njk3fDY4ODY3MDQxMDN8YzZjMDNlOTAxNzJhNzMwMzFjNjNiN2Y2ZDcxYjFmOGJhYWNhODJlNWZhMDVjNjk2ZWNlMzk1NTMxY2I2ZDQ5MiJ9LCJzaWduYXR1cmUiOiIifQ=='}, {'taken_at': 1497981308, 'pk': 1541501398720699957, 'id': '1541501398720699957_5428544314', 'device_timestamp': 1497981179064, 'media_type': 1, 'code': 'BVkg1rbg941', 'client_cache_key': 'MTU0MTUwMTM5ODcyMDY5OTk1Nw==.2', 'filter_type': 613, 'comment_likes_enabled': True, 'comment_threading_enabled': False, 'has_more_comments': True, 'max_num_visible_preview_comments': 2, 'preview_comments': [], 'can_view_more_preview_comments': False, 'comment_count': 6, 'inline_composer_display_condition': 'impression_trigger', 'image_versions2': {'candidates': [{'width': 1080, 'height': 1080, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/979d53c45add2680f8e3d2a19a89358a/5D545FBA/t51.2885-15/e35/19226937_467478490266928_1196050376487337984_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&se=7&ig_cache_key=MTU0MTUwMTM5ODcyMDY5OTk1Nw%3D%3D.2'}, {'width': 480, 'height': 480, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/608ecb6a9892a38b1e7d7307da26abe3/5D50CF52/t51.2885-15/e35/s480x480/19226937_467478490266928_1196050376487337984_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&ig_cache_key=MTU0MTUwMTM5ODcyMDY5OTk1Nw%3D%3D.2'}]}, 'original_width': 1080, 'original_height': 1080, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'can_viewer_reshare': True, 'caption_is_edited': True, 'like_count': 67, 'has_liked': False, 'top_likers': [], 'direct_reply_to_author_enabled': True, 'photo_of_you': False, 'usertags': {'in': []}, 'caption': {'pk': 17859834499162208, 'user_id': 5428544314, 'text': 'Why do you take a picture of me?? 🐕\n\n#dogs #dogsofinstagram #dog #lovedogs #hond #honden #chihuahua #chihuahuas #lovechihuahuas #woodenfloor #wood', 'type': 1, 'created_at': 1497986971, 'created_at_utc': 1497986971, 'content_type': 'comment', 'status': 'Active', 'bit_flags': 0, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'did_report_as_spam': False, 'share_enabled': False, 'media_id': 1541501398720699957}, 'can_viewer_save': True, 'organic_tracking_token': 'eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiZDBlZWY4MDJjNDhhNDMzN2E2YmM3NTczNTliMmFhNmIxNTQxNTAxMzk4NzIwNjk5OTU3Iiwic2VydmVyX3Rva2VuIjoiMTU1NzU3MDYzNDQyN3wxNTQxNTAxMzk4NzIwNjk5OTU3fDY4ODY3MDQxMDN8MzIwNjQyMGQxZmFhMTY0NmMwZjhlZmU5ZmM3ODg3ZDUwYzk2Y2ZiZjI2OTZmYWFlM2FmZjYzM2I1YzE3OTg4YyJ9LCJzaWduYXR1cmUiOiIifQ=='}, {'taken_at': 1497546994, 'pk': 1537858109001785150, 'id': '1537858109001785150_5428544314', 'device_timestamp': 1497546888175, 'media_type': 1, 'code': 'BVXkc1eAV8-', 'client_cache_key': 'MTUzNzg1ODEwOTAwMTc4NTE1MA==.2', 'filter_type': 613, 'comment_likes_enabled': True, 'comment_threading_enabled': False, 'has_more_comments': True, 'max_num_visible_preview_comments': 2, 'preview_comments': [], 'can_view_more_preview_comments': False, 'comment_count': 3, 'inline_composer_display_condition': 'impression_trigger', 'image_versions2': {'candidates': [{'width': 1080, 'height': 1350, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/6040e289fb6799c4dcbafc56b9373536/5D7777D0/t51.2885-15/e35/19227058_1892830640929180_6364972126276943872_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&se=7&ig_cache_key=MTUzNzg1ODEwOTAwMTc4NTE1MA%3D%3D.2'}, {'width': 480, 'height': 600, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/f5697796f668530a1689fc6f76c02546/5D549000/t51.2885-15/e35/p480x480/19227058_1892830640929180_6364972126276943872_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&ig_cache_key=MTUzNzg1ODEwOTAwMTc4NTE1MA%3D%3D.2'}]}, 'original_width': 1080, 'original_height': 1350, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'can_viewer_reshare': True, 'caption_is_edited': False, 'like_count': 71, 'has_liked': False, 'top_likers': [], 'direct_reply_to_author_enabled': True, 'photo_of_you': False, 'caption': {'pk': 17884011391034332, 'user_id': 5428544314, 'text': 'Miss red head... #cat #cats #redcat #poes #rood #lovecats #catsofinstagram', 'type': 1, 'created_at': 1497546995, 'created_at_utc': 1497546995, 'content_type': 'comment', 'status': 'Active', 'bit_flags': 0, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'did_report_as_spam': False, 'share_enabled': False, 'media_id': 1537858109001785150}, 'can_viewer_save': True, 'organic_tracking_token': 'eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiZDBlZWY4MDJjNDhhNDMzN2E2YmM3NTczNTliMmFhNmIxNTM3ODU4MTA5MDAxNzg1MTUwIiwic2VydmVyX3Rva2VuIjoiMTU1NzU3MDYzNDQyOHwxNTM3ODU4MTA5MDAxNzg1MTUwfDY4ODY3MDQxMDN8OWRkYmMyNzM2NDE0Y2ZlODI1ZWMzNjhlMmUzY2NjZTg3ODRlNWIwMzA1MTYwMDNjOTM0ZTA5YjBhNzk1MTYyNSJ9LCJzaWduYXR1cmUiOiIifQ=='}, {'taken_at': 1495992392, 'pk': 1524817165684032337, 'id': '1524817165684032337_5428544314', 'device_timestamp': 1495992322264, 'media_type': 1, 'code': 'BUpPSIkA8NR', 'client_cache_key': 'MTUyNDgxNzE2NTY4NDAzMjMzNw==.2', 'filter_type': 0, 'comment_likes_enabled': True, 'comment_threading_enabled': False, 'has_more_comments': False, 'max_num_visible_preview_comments': 2, 'preview_comments': [], 'can_view_more_preview_comments': False, 'comment_count': 0, 'inline_composer_display_condition': 'impression_trigger', 'image_versions2': {'candidates': [{'width': 1080, 'height': 1080, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/c01b1a59d21ac35a658f5ec42e63f062/5D6F79B1/t51.2885-15/e35/18646724_235569006929363_7217737535005392896_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&se=7&ig_cache_key=MTUyNDgxNzE2NTY4NDAzMjMzNw%3D%3D.2'}, {'width': 480, 'height': 480, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/26282a349fca804ea5401e61614a1169/5D679759/t51.2885-15/e35/s480x480/18646724_235569006929363_7217737535005392896_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&ig_cache_key=MTUyNDgxNzE2NTY4NDAzMjMzNw%3D%3D.2'}]}, 'original_width': 1080, 'original_height': 1080, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'can_viewer_reshare': True, 'caption_is_edited': True, 'like_count': 53, 'has_liked': False, 'top_likers': [], 'direct_reply_to_author_enabled': True, 'photo_of_you': False, 'usertags': {'in': []}, 'caption': {'pk': 17867904325084675, 'user_id': 5428544314, 'text': '#house #homesweethome #ourplace #tree #home', 'type': 1, 'created_at': 1495992906, 'created_at_utc': 1495992906, 'content_type': 'comment', 'status': 'Active', 'bit_flags': 0, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'did_report_as_spam': False, 'share_enabled': False, 'media_id': 1524817165684032337}, 'can_viewer_save': True, 'organic_tracking_token': 'eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiZDBlZWY4MDJjNDhhNDMzN2E2YmM3NTczNTliMmFhNmIxNTI0ODE3MTY1Njg0MDMyMzM3Iiwic2VydmVyX3Rva2VuIjoiMTU1NzU3MDYzNDQyOHwxNTI0ODE3MTY1Njg0MDMyMzM3fDY4ODY3MDQxMDN8MTgxMjNkMmEwM2VjNjFhNmMzZTAwODA3N2QxNzUzMjY1ODQ1NThmOGI0MGQ5NzI0NTA1YzU1ZDY2NmY4MzU2NCJ9LCJzaWduYXR1cmUiOiIifQ=='}, {'taken_at': 1495911323, 'pk': 1524137110880211413, 'id': '1524137110880211413_5428544314', 'device_timestamp': 1495911253758, 'media_type': 1, 'code': 'BUm0qCLAVHV', 'client_cache_key': 'MTUyNDEzNzExMDg4MDIxMTQxMw==.2', 'filter_type': 0, 'comment_likes_enabled': True, 'comment_threading_enabled': False, 'has_more_comments': True, 'max_num_visible_preview_comments': 2, 'preview_comments': [], 'can_view_more_preview_comments': False, 'comment_count': 2, 'inline_composer_display_condition': 'impression_trigger', 'image_versions2': {'candidates': [{'width': 1080, 'height': 1080, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/d1377be74eebcbae853d651eb2c5e059/5D708667/t51.2885-15/e35/18722882_437640336611036_7300067123152289792_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&se=7&ig_cache_key=MTUyNDEzNzExMDg4MDIxMTQxMw%3D%3D.2'}, {'width': 480, 'height': 480, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/d1a0f5931f91a46db4d87759702046fd/5D67208F/t51.2885-15/e35/s480x480/18722882_437640336611036_7300067123152289792_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&ig_cache_key=MTUyNDEzNzExMDg4MDIxMTQxMw%3D%3D.2'}]}, 'original_width': 1080, 'original_height': 1080, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'can_viewer_reshare': True, 'caption_is_edited': False, 'like_count': 45, 'has_liked': False, 'top_likers': [], 'direct_reply_to_author_enabled': True, 'photo_of_you': False, 'caption': {'pk': 17880994099021315, 'user_id': 5428544314, 'text': 'Schatjes! 😍\n#chihuahua #dogs #travel', 'type': 1, 'created_at': 1495911324, 'created_at_utc': 1495911324, 'content_type': 'comment', 'status': 'Active', 'bit_flags': 0, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'did_report_as_spam': False, 'share_enabled': False, 'media_id': 1524137110880211413, 'has_translation': True}, 'can_viewer_save': True, 'organic_tracking_token': 'eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiZDBlZWY4MDJjNDhhNDMzN2E2YmM3NTczNTliMmFhNmIxNTI0MTM3MTEwODgwMjExNDEzIiwic2VydmVyX3Rva2VuIjoiMTU1NzU3MDYzNDQyOHwxNTI0MTM3MTEwODgwMjExNDEzfDY4ODY3MDQxMDN8M2ViZmFhYjA1MjlmNWM2ZjBlZjFmMWZlNmM0NDQzYWMxODI2NGExOTEwOGQyN2NjNzQzMzIwZGM5OWRlYjk4MSJ9LCJzaWduYXR1cmUiOiIifQ=='}, {'taken_at': 1494185558, 'pk': 1509660341876029041, 'id': '1509660341876029041_5428544314', 'device_timestamp': 1494185527668, 'media_type': 1, 'code': 'BTzZBUZA_Zx', 'client_cache_key': 'MTUwOTY2MDM0MTg3NjAyOTA0MQ==.2', 'filter_type': 114, 'comment_likes_enabled': True, 'comment_threading_enabled': False, 'has_more_comments': True, 'max_num_visible_preview_comments': 2, 'preview_comments': [], 'can_view_more_preview_comments': False, 'comment_count': 3, 'inline_composer_display_condition': 'impression_trigger', 'image_versions2': {'candidates': [{'width': 1080, 'height': 1350, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/454859de3092a4dcafd50cc2e4e966c4/5D6C9D87/t51.2885-15/e35/18299606_1677052675937570_3117678071100997632_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&se=7&ig_cache_key=MTUwOTY2MDM0MTg3NjAyOTA0MQ%3D%3D.2'}, {'width': 480, 'height': 600, 'url': 'https://scontent-lax3-1.cdninstagram.com/vp/1bab91125c22229bdf281a549dd0a806/5D766057/t51.2885-15/e35/p480x480/18299606_1677052675937570_3117678071100997632_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com&ig_cache_key=MTUwOTY2MDM0MTg3NjAyOTA0MQ%3D%3D.2'}]}, 'original_width': 1080, 'original_height': 1350, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'can_viewer_reshare': True, 'caption_is_edited': False, 'like_count': 52, 'has_liked': False, 'top_likers': [], 'direct_reply_to_author_enabled': True, 'photo_of_you': False, 'caption': {'pk': 17855246737169724, 'user_id': 5428544314, 'text': '#GardaLake #Italy', 'type': 1, 'created_at': 1494185559, 'created_at_utc': 1494185559, 'content_type': 'comment', 'status': 'Active', 'bit_flags': 0, 'user': {'pk': 5428544314, 'username': 'madeleineshouse72', 'full_name': "Madeleine's interior 🇳🇱", 'is_private': False, 'profile_pic_url': 'https://scontent-lax3-1.cdninstagram.com/vp/642527b3a1f327d0a34daef1f4cf8b82/5D6EC7D6/t51.2885-19/s150x150/57987890_278709339701014_523940337429774336_n.jpg?_nc_ht=scontent-lax3-1.cdninstagram.com', 'profile_pic_id': '2038764964625759543_5428544314', 'is_verified': False, 'has_anonymous_profile_picture': False, 'is_unpublished': False, 'is_favorite': False}, 'did_report_as_spam': False, 'share_enabled': False, 'media_id': 1509660341876029041}, 'can_viewer_save': True, 'organic_tracking_token': 'eyJ2ZXJzaW9uIjo1LCJwYXlsb2FkIjp7ImlzX2FuYWx5dGljc190cmFja2VkIjp0cnVlLCJ1dWlkIjoiZDBlZWY4MDJjNDhhNDMzN2E2YmM3NTczNTliMmFhNmIxNTA5NjYwMzQxODc2MDI5MDQxIiwic2VydmVyX3Rva2VuIjoiMTU1NzU3MDYzNDQyN3wxNTA5NjYwMzQxODc2MDI5MDQxfDY4ODY3MDQxMDN8ZGMzNDBlYjVlYzY4NGVkNTg0ZDcxODMzY2Q4ZDdjYmY2NzhkMjU0Y2FlZmE3MDBiMDUwZWIyNDliMTc0MmNhMSJ9LCJzaWduYXR1cmUiOiIifQ=='}]



    profileScrap("merihach")
    # main()
    # print("Bye")






