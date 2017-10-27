# Mining-Twitter

Online Social Network Analysis - CS 579

# Introduction
This project is used to collect a political social network. For the given list of 4 twitter accounts(candidates.txt) the goal is to use Twitter API to construct a social network of these accounts.

# Candidates
The following is the list of twitter accounts of 4 U.S. presidential candidates from the previous election.
	DrJillStein
	GovGaryJohnson
	HillaryClinton
	realDonaldTrump
After the connection was established, candidates were read from candidates.txt and then were searched using get_users().

# Authentication
Twitter uses OAuth to enable secure requests to the API. Once the account has been created, tokens are generated after creating an app at apps.twitter.com. Keys & access tokens can be found in the app. These tokens will be sent with each API request made.

# Limitations (developer.twitter.com/en/docs/basics/rate-limiting)
Twitter has rate limits. The rate limits are based on request, not the amount of data (e.g. bytes) received. Rate limiting of the API is primarily on a per-user basis — or more accurately described, per user access token. The function robust_request() is used if twitter request fails and sleep for 15 minutes. This is done at most max_tries times before quitting.

# Graph
Networkx library is used to plot the network showing links between the candidates and their friends.

# Mining Twitter: 
    Learned how to use twitter’s developer platform & how to make API requests
    Learned how to use tweet metadata
    Learned how to extract entities - user mentions, hashtags and urls from tweets
