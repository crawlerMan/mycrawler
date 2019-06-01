from instabot import Bot
from pymongo import MongoClient
client = MongoClient('localhost')
db = client.InstagramCrawl
import time
from textblob import TextBlob
import re
import emoji
from stop_words import get_stop_words


bot = Bot()


def getInstagramUrlFromMediaId(media_id):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_'
    shortened_id = ''

    while media_id > 0:
        remainder = media_id % 64
        # dual conversion sign gets the right ID for new posts
        media_id = (media_id - remainder) // 64;
        # remainder should be casted as an integer to avoid a type error.
        shortened_id = alphabet[int(remainder)] + shortened_id

    return 'https://instagram.com/p/' + shortened_id + '/'


#remove hashtag
def hashtaghEx(s):
    t = remove_emoji(s)
    return re.findall(r"#(\w+)", t)

#remove emoji from text
def remove_emoji(text):
    return emoji.get_emoji_regexp().sub(u'', text)


#joda kardan kalamat
def spliteKeyWord(s):
    #s = re.sub(r'\s', '', s)
    s = s.replace(r"\n", " ")
    return re.findall(r'[\dA-Za-z]+|[^\dA-Za-z\W]+', s, re.UNICODE)


#tashkhis zaban
def lanqdet(text):

    if text == None:
        return "null"


    lanList = []
    listStop = ['aber', 'alle', 'allem', 'allen', 'aller', 'alles', 'als', 'also', 'am', 'an', 'ander', 'andere', 'anderem',
          'anderen', 'anderer', 'anderes', 'anderm', 'andern', 'anders', 'auch', 'auf', 'aus', 'bei', 'bin', 'bis',
          'bist', 'da', 'damit', 'dann', 'das', 'dass', 'dasselbe', 'dazu', 'daß', 'dein', 'deine', 'deinem', 'deinen',
          'deiner', 'deines', 'dem', 'demselben', 'den', 'denn', 'denselben', 'der', 'derer', 'derselbe', 'derselben',
          'des', 'desselben', 'dessen', 'dich', 'die', 'dies', 'diese', 'dieselbe', 'dieselben', 'diesem', 'diesen',
          'dieser', 'dieses', 'dir', 'doch', 'dort', 'du', 'durch', 'ein', 'eine', 'einem', 'einen', 'einer', 'eines',
          'einig', 'einige', 'einigem', 'einigen', 'einiger', 'einiges', 'einmal', 'er', 'es', 'etwas', 'euch', 'euer',
          'eure', 'eurem', 'euren', 'eurer', 'eures', 'für', 'gegen', 'gewesen', 'hab', 'habe', 'haben', 'hat', 'hatte',
          'hatten', 'hier', 'hin', 'hinter', 'ich', 'ihm', 'ihn', 'ihnen', 'ihr', 'ihre', 'ihrem', 'ihren', 'ihrer',
          'ihres', 'im', 'in', 'indem', 'ins', 'ist', 'jede', 'jedem', 'jeden', 'jeder', 'jedes', 'jene', 'jenem',
          'jenen', 'jener', 'jenes', 'jetzt', 'kann', 'kein', 'keine', 'keinem', 'keinen', 'keiner', 'keines', 'können',
          'könnte', 'machen', 'man', 'manche', 'manchem', 'manchen', 'mancher', 'manches', 'mein', 'meine', 'meinem',
          'meinen', 'meiner', 'meines', 'mich', 'mir', 'mit', 'muss', 'musste', 'nach', 'nicht', 'nichts', 'noch',
          'nun', 'nur', 'ob', 'oder', 'ohne', 'sehr', 'sein', 'seine', 'seinem', 'seinen', 'seiner', 'seines', 'selbst',
          'sich', 'sie', 'sind', 'so', 'solche', 'solchem', 'solchen', 'solcher', 'solches', 'soll', 'sollte',
          'sondern', 'sonst', 'um', 'und', 'uns', 'unser', 'unsere', 'unserem', 'unseren', 'unserer', 'unseres',
          'unter', 'viel', 'vom', 'von', 'vor', 'war', 'waren', 'warst', 'was', 'weg', 'weil', 'weiter', 'welche',
          'welchem', 'welchen', 'welcher', 'welches', 'wenn', 'werde', 'werden', 'wie', 'wieder', 'will', 'wir', 'wird',
          'wirst', 'wo', 'wollen', 'wollte', 'während', 'würde', 'würden', 'zu', 'zum', 'zur', 'zwar', 'zwischen',
          'über', 'فى', 'في', 'كل', 'لم', 'لن', 'له', 'من', 'هو', 'هي', 'قوة', 'كما', 'لها', 'منذ', 'وقد', 'ولا',
          'نفسه',
          'لقاء', 'مقابل', 'هناك', 'وقال', 'وكان', 'نهاية', 'وقالت', 'وكانت', 'للامم', 'فيه', 'كلم', 'لكن', 'وفي',
          'وقف', 'ولم', 'ومن', 'وهو', 'وهي', 'يوم', 'فيها', 'منها', 'مليار', 'لوكالة', 'يكون', 'يمكن', 'مليون', 'حيث',
          'اكد', 'الا', 'اما', 'امس', 'السابق', 'التى', 'التي', 'اكثر', 'ايار', 'ايضا', 'ثلاثة', 'الذاتي', 'الاخيرة',
          'الثاني', 'الثانية', 'الذى', 'الذي', 'الان', 'امام', 'ايام', 'خلال', 'حوالى', 'الذين', 'الاول', 'الاولى',
          'بين', 'ذلك', 'دون', 'حول', 'حين', 'الف', 'الى', 'انه', 'اول', 'ضمن', 'انها', 'جميع', 'الماضي', 'الوقت',
          'المقبل', 'اليوم', 'ـ', 'ف', 'و', 'و6', 'قد', 'لا', 'ما', 'مع', 'مساء', 'هذا', 'واحد', 'واضاف', 'واضافت',
          'فان', 'قبل', 'قال', 'كان', 'لدى', 'نحو', 'هذه', 'وان', 'واكد', 'كانت', 'واوضح', 'مايو', 'ب', 'ا', 'أ', '،',
          'عشر', 'عدد', 'عدة', 'عشرة', 'عدم', 'عام', 'عاما', 'عن', 'عند', 'عندما', 'على', 'عليه', 'عليها', 'زيارة',
          'سنة', 'سنوات', 'تم', 'ضد', 'بعد', 'بعض', 'اعادة', 'اعلنت', 'بسبب', 'حتى', 'اذا', 'احد', 'اثر', 'برس', 'باسم',
          'غدا', 'شخصا', 'صباح', 'اطار', 'اربعة', 'اخرى', 'بان', 'اجل', 'غير', 'بشكل', 'حاليا', 'بن', 'به', 'ثم', 'اف',
          'ان', 'او', 'اي', 'بها', 'صفر', 'أن', 'ه', 'شد', 'a', 'about', 'above', 'after', 'again', 'against', 'all',
          'am', 'an', 'and', 'any', 'are', "aren't", 'as',
          'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot',
          'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each',
          'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd",
          "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i',
          "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me',
          'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or',
          'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd",
          "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their',
          'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're",
          "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we',
          "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's",
          'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you',
          "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves', 'a', 'ai', 'aie', 'aient',
          'aies', 'ait', 'alors', 'as', 'au', 'aucun', 'aura', 'aurai', 'auraient',
          'aurais', 'aurait', 'auras', 'aurez', 'auriez', 'aurions', 'aurons', 'auront', 'aussi', 'autre', 'aux',
          'avaient', 'avais', 'avait', 'avant', 'avec', 'avez', 'aviez', 'avions', 'avoir', 'avons', 'ayant', 'ayez',
          'ayons', 'bon', 'car', 'ce', 'ceci', 'cela', 'ces', 'cet', 'cette', 'ceux', 'chaque', 'ci', 'comme',
          'comment', 'd', 'dans', 'de', 'dedans', 'dehors', 'depuis', 'des', 'deux', 'devoir', 'devrait', 'devrez',
          'devriez', 'devrions', 'devrons', 'devront', 'dois', 'doit', 'donc', 'dos', 'droite', 'du', 'dès', 'début',
          'dù', 'elle', 'elles', 'en', 'encore', 'es', 'est', 'et', 'eu', 'eue', 'eues', 'eurent', 'eus', 'eusse',
          'eussent', 'eusses', 'eussiez', 'eussions', 'eut', 'eux', 'eûmes', 'eût', 'eûtes', 'faire', 'fais', 'faisez',
          'fait', 'faites', 'fois', 'font', 'force', 'furent', 'fus', 'fusse', 'fussent', 'fusses', 'fussiez',
          'fussions', 'fut', 'fûmes', 'fût', 'fûtes', 'haut', 'hors', 'ici', 'il', 'ils', 'j', 'je', 'juste', 'l',
          'la', 'le', 'les', 'leur', 'leurs', 'lui', 'là', 'm', 'ma', 'maintenant', 'mais', 'me', 'mes', 'moi',
          'moins', 'mon', 'mot', 'même', 'n', 'ne', 'ni', 'nom', 'nommé', 'nommée', 'nommés', 'nos', 'notre', 'nous',
          'nouveau', 'nouveaux', 'on', 'ont', 'ou', 'où', 'par', 'parce', 'parole', 'pas', 'personne', 'personnes',
          'peu', 'peut', 'plupart', 'pour', 'pourquoi', 'qu', 'quand', 'que', 'quel', 'quelle', 'quelles', 'quels',
          'qui', 'sa', 'sans', 'se', 'sera', 'serai', 'seraient', 'serais', 'serait', 'seras', 'serez', 'seriez',
          'serions', 'serons', 'seront', 'ses', 'seulement', 'si', 'sien', 'soi', 'soient', 'sois', 'soit', 'sommes',
          'son', 'sont', 'sous', 'soyez', 'soyons', 'suis', 'sujet', 'sur', 't', 'ta', 'tandis', 'te', 'tellement',
          'tels', 'tes', 'toi', 'ton', 'tous', 'tout', 'trop', 'très', 'tu', 'un', 'une', 'valeur', 'voient', 'vois',
          'voit', 'vont', 'vos', 'votre', 'vous', 'vu', 'y', 'à', 'ça', 'étaient', 'étais', 'était', 'étant', 'état',
          'étiez', 'étions', 'été', 'étés', 'êtes', 'être', "ها", "برای", "که", "را", "می", "تا", "و", "آن", "هم", "نه",
          "نیز", "لیکن", "اما", "یا", "اگر", "بلکه",
          "ازبس", "دو", "یک", "بر", "به", "شما", "او", "من", "ش", "اش", "ات", "ام", "پی", "سه", "چهار", "پنج", "شش",
          "ششم", "هفت", "هشت", "نه", "ده", "هم", "هی", "از", "در", "با", ]

    t = remove_emoji(text)
    i = spliteKeyWord(t)

    filtered_fr = [w for w in i if not w in listStop]

    print(filtered_fr)

    for j in filtered_fr:
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
        return lanList



def crawler(username):
    getfollowingListInfo(username)
    getfollowerListInfo(username)


def profileScrap(username):
    userId = bot.get_user_id_from_username(username)
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
                mediaLink = getInstagramUrlFromMediaId(m)
                data = {"owner": username, "mediaID": m,"media link":mediaLink ,"likers": likers, "commntes": coment, "full_crawl": False}
                i = db.instagram_users_posts.insert_one(data)
                print("owner: %s" % username)
                ml = str(mediaLink)
                print("media link: %s" % ml)

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
                    print(data)

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
                update = db.instagram_users.update({i["username"]}, {"$set": {"crawlStatus": True}})





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
    #bot.login()
    #main()
    print("Bye")
    print(lanqdet("إذا زارتک شدّه فاعلم أنّها سحابه صیف عن قلیل تقشع، ولا یخیفک رعدها، ولا یرهبک برقها، فربّما کانت محمّلهً بالغیث"))






