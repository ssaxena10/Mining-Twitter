# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Imports you'll need.
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
from TwitterAPI import TwitterAPI


consumer_key = 'cwsnAuKObHOe1AaqJjctdyorm'
consumer_secret = 'Bvp1jHLLmuhAJrAsgT76L67FnfKl7m5PJ0I5dtBGZGf2LDgZxZ'
access_token = '318398468-0AT3xXfBo2zeJjTXIeeyP2SxXyLB4zpeQycBMq1R'
access_token_secret = 'n7wQ7Ig7EqDdSZRbtpwxbOaW6XMa9QWcDHgbpcF6BVT6V'


def get_twitter():
    
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)


def read_screen_names(filename):
    
    with open(filename) as f:
        data = f.readlines()
    
    data = [x.strip() for x in data]
    return data
    
    pass


def robust_request(twitter, resource, params, max_tries=5):
    
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def get_users(twitter, screen_names):
    
    twitter = get_twitter()
 
    request = robust_request(twitter,'users/lookup',{'screen_name': screen_names})
    
    u = [r for r in request]
    
    return u
   
    pass

def get_friends(twitter, screen_name):
    
    twitter = get_twitter()
    request = robust_request(twitter, 'friends/ids', {'screen_name' : screen_name, 'count': 5000})
    u = [r for r in request]
    
    friends = []
    add = []
    for f in range(len(u)):
        friends = u[f]
        add.append(friends)
    return add
    pass

def add_all_friends(twitter, users):
   
    twitter = get_twitter()
    l = len(users)
    friends = []
    for i in range(l):
        friends = get_friends(twitter,users[i].get('screen_name'))
        users[i].update({'friends':friends})
        
    pass

def print_num_friends(users):
    
    length = len(users)

    for r in range (length):
        name = users[r].get('screen_name')
        friend = users[r].get('friends_count')
        print('%s %s' % (name, friend))
 
    pass

def followed_by_hillary_and_donald(users, twitter):
    addH = []
    addT = []
    for i in range(len(users)):
        if users[i].get('screen_name') == 'HillaryClinton':
            addH = get_friends(twitter,users[i].get('screen_name'))
        elif users[i].get('screen_name')=='realDonaldTrump':
            addT = get_friends(twitter,users[i].get('screen_name'))
    
    common = set(addH) & set(addT)
    
    request = robust_request(twitter, 'users/show', {'user_id' : common})
    u = [r for r in request]
    
    u_name = list(map (lambda x: x['screen_name'],u))
    return u_name
    
    pass

def count_friends(users):
    
    c = Counter()
    for i in range(len(users)):
        for j in users[i].get('friends'):
            c[j] = c[j]+1
    return c
    
    pass

def friend_overlap(users):
    N = 0
    li = []
    
    for i in range(0,len(users)-1):
        for j in range(i+1,len(users)):
            common = set(users[i].get('friends')) & set(users[j].get('friends'))
            N = len(common)
            li.append((users[i].get('screen_name'),users[j].get('screen_name'),N))
            
    li_sort = sorted(sorted([d for d in li if d[2]==d[2]],key=lambda x:x[0]),key=lambda x:x[2],reverse = True)
    return li_sort
    pass

def create_graph(users, friend_counts):
    #warnings.filterwarnings("ignore")
    graph = nx.Graph()
    #print(friend_counts)
    name = []
    
    for i in range(len(users)):
        name = users[i].get('screen_name')
        graph.add_node(name)
        
    for i in friend_counts:
        if friend_counts[i] > 1 :
            graph.add_node(i)
    for i in range(len(users)):
        for j in graph.nodes():
            if j in users[i]['friends']:
                graph.add_edge(users[i].get('screen_name'),j)
    
    plt.show()
    return graph
    pass

def draw_network(graph, users, filename):
    
    
    pos_nodes = dict()
    for u in users:
        pos_nodes[u['screen_name']] = u['screen_name']
        
    fig = plt.figure(figsize=(15,15))
    nx.draw_networkx(graph,labels=pos_nodes,alpha=.5, width=.1,
                     node_size=100)
    plt.show()
    plt.axis("off")
    fig.savefig('network.png')
    
    
    pass


def main():
    """ Main method. You should not modify this. """
    twitter = get_twitter()
    screen_names = read_screen_names('candidates.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    print('found %d users with screen_names %s' %
          (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    print('Friends per candidate:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    print('User followed by Hillary and Donald: %s' % followed_by_hillary_and_donald(users, twitter))
    graph = create_graph(users, friend_counts)
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph, users, 'network.png')
    print('network drawn to network.png')
    
    
if __name__ == '__main__':
    main()