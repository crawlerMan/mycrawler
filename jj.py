def profileScrap(username):
	userId = bot.get_userid_from_username(username)
	medias = bot.get_total_user_medias(user_id=userId)

	for m in medias:
		coment = []
		coments = bot.get_media_comments(m)

		try:
			for c in coments:
				a = {"owner": username, "mediaID": m, "user_id": c["user_id"], "username": c["user"]["username"],
		             "full_name": c["user"]["full_name"], "text": c["text"], "cm_lanq": lanqdet(c["text"])}
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
				data = {"owner": username, "mediaID": m, "likers": likers,"commntes": coment, "full_crawl": False}
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
			print("Somthings wrong in get likers...")