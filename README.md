# Reddit Discord Bot

**Current version: v1.1**  
This is a Discord Bot that allows users to be notified on discord when certain terms appear in new posts on a subreddit. It also allows basic queries of subreddits to get hot/top/newest posts.
### v1.1 update changes (12/15/2020):

> Feature changes:
>* Mentions are now on a search by search basis, and are declared when adding a new search
>* My searches list is now much easier to read
>* Searches are now removed using a list number found in !my_searches
>* Search terms are now whitespace and capitalization indifferent
>* Reddit title and body text are now whitespace and capitalization indifferent

>*Under the hood:*
>* Reduced number of internal lists/dicts
>* Switched from json to pickle files to allow searches to be saved and persist through bot restarts
>* A few small loop optimizations

>*Bug fixes:*
>* Top functions now work correctly, returning the top 10 results
>* User commands now send a message if a user isn't registered

### Bot Commands 
*Basic commands:*
* !hot (subreddit) (#)  ----- Returns the first (#) hot posts from the subreddit
* !new (subreddit) (#)  ----- Returns the first (#) new posts from the subreddit
* Top commands:
	* !topall (subreddit) ----- Returns the top posts of all time
	* !topyear (subreddit) ----- Returns the top posts of the year
	* !topmonth (subreddit) ----- Returns the top posts of the month
	* !topweek (subreddit) ----- Returns the top posts of the week
	* !topday (subreddit) ----- Returns the top posts of the day
	* !tophour (subreddit) ----- Returns the top posts of the hour

*User/searching commands:*
* !hello ----- Initalizes the user. Users must run this command before using other commands in this section
* !goodbye ----- Removes the user. Users need to be registered for searching to work
* !new_search (mention?: true/false) (subreddit) (list of terms separated with commas) ----- Starts a new search within 	inputted subreddit for all of the terms. Bot will send a notifications to the channel the command was run in and will mention the user if mention=true when a term is found
* !my_search ----- Bot will send a list of searches the user is running
* !remove_search (#) ----- Bot will remove the search according to the numbers given by !my_search

Command aliases:
* !hot: 
* !new:
* !topall: !all, !top_all
* !topyear: !year, !top_year
* !topmonth: !month, !top_month
* !topweek: !week, !top_week
* !topday: !day, !top_day, !top, !today
* !tophour: !hour, !top_hour, !now  
--  
* !hello:
* !goodbye
* !new_search: !newsearch, !ns
* !my_search: !mysearch, !ms, !list
* !remove_search: !removesearch, !rs, !remove