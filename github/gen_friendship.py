# -*- coding: utf-8 -*-

import requests
import argparse
import json
import time
import os

nodes = []
links = []

sleep_count = 0

CLIENT_ID = "1c6409e7a4219e6dea66"
CLIENT_SECRET = "44636a9d327c1e47aba28a9b50a22b39ac4caeb4"

ROOT_ENDPOINT = "https://api.github.com"
USER_ENDPOINT = ROOT_ENDPOINT + "/users/%s"
FOLLOWERS_ENDPOINT = USER_ENDPOINT + "/followers"
FOLLOWING_ENDPOINT = USER_ENDPOINT + "/following"

headers = {"Accept" : "application/vnd.github.v3+json", "User-Agent" : "stamaimer"}

ratelimit_remaining = "5000"
ratelimit_reset = time.time()

def set_ratelimit_info(headers):

    global ratelimit_remaining

    ratelimit_remaining = headers['X-RateLimit-Remaining']

    global ratelimit_reset

    ratelimit_reset = int(headers['X-RateLimit-Reset'])

def retrieve(url):

    while 1:

        try:

            print "ratelimit_remaining : %s" % ratelimit_remaining

            if '0' == ratelimit_remaining:

                interval = ratelimit_reset - time.time()

                if interval > 0:

                    global sleep_count

                    sleep_count += 1

                    print "the %d times sleep, sleeping %f seconds..." % (sleep_count, interval)

                    time.sleep(interval)

            print "request : %s" % url

            response = requests.get(url, params = {"client_id" : CLIENT_ID, "client_secret" : CLIENT_SECRET}, headers = headers)

            if 200 == response.status_code:

                # print "request : %s success" % response.url

                return response

            else:

                set_ratelimit_info(response.headers)

                print "request : %s %d" % (response.url, response.status_code)

                print json.dumps(response.json(), indent = 4)

                if 404 == response.status_code:

                    return None

        except :

            raise

def find_by_name(name):

    for node in nodes:

        if name == node['name']:

            return nodes.index(node)

def get_followers(name):

    # name = node["name"]

    # group = node["group"]

    response = retrieve(FOLLOWERS_ENDPOINT % name)

    set_ratelimit_info(response.headers)

    if response:

        followers = response.json()

        return ( user["login"] for user in followers )

        # for user in followers:

        #     if user["login"] not in [ele["name"] for ele in nodes]:

        #         tmpu = {"name":user["login"], "group":group + 1}

        #         nodes.append(tmpu)

        #         links.append({"source":nodes.index(tmpu), "target":nodes.index(node)})

        #     else:

        #         links.append({"source":find_by_name(user["login"]), "target":nodes.index(node)})

def get_following(name):

    # name = node["name"]

    # group = node["group"]

    response = retrieve(FOLLOWING_ENDPOINT % name)

    set_ratelimit_info(response.headers)

    if response:

        following = response.json()

        return ( user["login"] for user in following )

        # for user in following:

        #     if user["login"] not in [ele["name"] for ele in nodes]:

        #         tmpu = {"name":user["login"], "group":group + 1}

        #         nodes.append(tmpu)

        #         links.append({"source":nodes.index(node), "target":nodes.index(tmpu)})

        #     else:

        #         links.append({"source":nodes.index(node), "target":find_by_name(user["login"])})

def is_valid(name):

    response = retrieve(USER_ENDPOINT % name)

    if response:

        return not "message" in response.json()

def start(login, depth):

    if not is_valid(login):

        return None

    nodes.append({"name":login, "group":0})

    for node in nodes:

        if node["group"] > depth:

            print "generate graph ..."

            data = {"nodes":nodes, "links":links}

            with open(login + "_github.json", 'w') as outfile:

                json.dump(data, outfile)
            
            return os.path.abspath(login + "_github.json")

        else:

            name = node["name"]; group = node["group"]

            followers = get_followers(name)
            following = get_following(name)

            intersection = set(following).intersection(followers)

            for user in intersection:

                if user not in [ele["name"] for ele in nodes]:

                    if 2 == group:

                        continue

                    tmpu = {"name":user, "group":group + 1}

                    nodes.append(tmpu)

                    links.append({"source":nodes.index(tmpu), "target":nodes.index(node)})

                else:

                    links.append({"source":find_by_name(user), "target":nodes.index(node)})

if __name__ == "__main__":

    argument_parser = argparse.ArgumentParser(description="")

    argument_parser.add_argument("login", help="")

    argument_parser.add_argument("depth", help="", type=int)

    args = argument_parser.parse_args()

    sed_login = args.login

    max_depth = args.depth

    start(sed_login, max_depth)
