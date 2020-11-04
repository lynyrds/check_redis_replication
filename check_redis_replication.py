#!/usr/bin/python

import sys
import redis
import argparse
from datetime import datetime

parser = argparse.ArgumentParser(description='Check Redis replication')

parser.add_argument('--src', action='store', dest='write_to', required=True,
                    help='Redis node ip or name to write to')

parser.add_argument('--src_port', action='store', dest='src_port', required=True,
                    help='Redis source port')

parser.add_argument('--src_password', action='store', dest='src_password', required=True,
                    help='Redis auth')

parser.add_argument('--dest', action='store', dest='read_from', required=True,
                    help='Redis node ip or name to read from')

parser.add_argument('--dest_port', action='store', dest='dest_port', required=True,
                    help='Redis destination port')

parser.add_argument('--dest_user', action='store', dest='dest_user', required=True,
                    help='User name for the destination node')

parser.add_argument('--dest_password', action='store', dest='dest_password', required=True,
                    help='Destination user password')

args = parser.parse_args()

print "Connecting to the source redis... ",
src_redis = redis.Redis(
host=args.write_to,
port=args.src_port,
password=args.src_password)
print "OK"


dest_url = 'redis://' + args.dest_user + ':' + args.dest_password + '@' + args.read_from + ':' + args.dest_port
print "Connecting to the target redis... ",
dest_redis = redis.Redis.from_url( url=dest_url)
print "OK"

print ""

def store_get_key(lr):
    key = lr + datetime.now().strftime("%Y%m%d_%H%M%S%s")
    
    print "Storing key " + key + " with " + lr + "... ",
    if lr == "lpush":
        src_redis.lpush(key, *range(1,101))
    else:
        src_redis.rpush(key, *range(1,101))
    print "OK"

    print "Wait for the key " + key + " to be replicated... ",
    check_again = True

    while check_again:
        if dest_redis.exists(key):
            check_again = False
            print "OK"

    my_list = []
    my_list = dest_redis.lrange(key, 0, -1)
    return my_list

print "Store the values already in descending order, get it and print as-is"
print ""
print map(int, store_get_key("lpush"))

print ""

print "Store the values in ascending order, read as is, sort, print"
print ""
final_list = []
final_list = sorted(map(int, store_get_key("rpush")), reverse=True)
print final_list


