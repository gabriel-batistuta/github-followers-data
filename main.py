from src import getter

def main():
    profile = ''
    followers = getter.get_followers(profile)
    getter.write_followers_json(followers, profile)

if __name__ == '__main__':
    main()