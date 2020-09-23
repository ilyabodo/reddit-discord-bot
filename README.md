# reddit-discord-bot

This is a Discord Bot that allows users to be notified on discord when certain terms appear in new posts on a subreddit. It also allows basic queries of subreddits to get hot/top/newest posts.

Current commands include:
"Basic commands":
!hot (subreddit) (#)   (Returns the first (#) of hot posts from the subreddit)
!new (subreddit) (#)   (Returns the first (#) of new posts from the subreddit)
!topall (subreddit)    (Returns the top posts of all time)
!topyear (subreddit)    (Returns the top posts of the year
!topmonth (subreddit)    (Returns the top posts of the month)
!topweek (subreddit)    (Returns the top posts of the week)
!topday (subreddit)    (Returns the top posts of the day)
!tophour (subreddit)    (Returns the top posts of the hour)

User/searching commands:
!hello    (initalizes the user - users must run this command before using other user commands)
!new_search (subreddit) (terms seperated by ',' with no space inbetween)
!remove_search (subreddit) (terms)
!my_search    (Returns a list of all searches the user is running)
!mention (true/false)    (Sets weither the bot will @ mention you when a search term is found, defaults to false)


API keys/tokens are imported from a .env file


Reddit Discord Bot is a work in progress and does have some bugs currently!

List of known bugs to be fixed:
-Not all user commands check if registered, causes bot errors
-All !top functions are usually failing, (probably too many posts being returned)

List of features that will be added in the future:
-Remove the need for spacing in search terms
-Add file saving for search dicts
-Make my_search response a nicer to look at
-Add confirmation upon starting new search