from Instagram import Instagram

# Get info about user
# Return list [username, biography, external_url, followers_count, followed_count, full_name, profile_pic, Facebook ID]
info = Instagram.collect_info("user")
print(info)

# Get user followers
#return list
followers = Instagram.collect_followers("user")
print(followers)

# Get user followings
# Return list
following = Instagram.collect_following("user")
print(following)
