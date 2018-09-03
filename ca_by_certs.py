from __future__ import print_function

__author__ = 'Bharath'
__version__ = "0.1.0"

try:
    import psycopg2
except ImportError:
    raise ImportError('\n\033[33mpsycopg2 library missing. pip install psycopg2\033[1;m\n')
    sys.exit(1)
import re
import sys

DB_HOST = 'crt.sh'
DB_NAME = 'certwatch'
DB_USER = 'guest'

def connect_to_db(limit):
    try:
        conn = psycopg2.connect("dbname={0} user={1} host={2}".format(DB_NAME, DB_USER, DB_HOST))
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("select name, CAST(no_of_certs_issued as int) as d from ca ORDER BY d desc LIMIT {};".format(limit))
    except:
        print("\n\033[1;31m[!] Unable to connect to the database\n\033[1;m")
    return cursor

def print_ca_stats(cursor, limit):
    print("\n\033[1;93m{:56} | {}".format("Certificate Authority(CA)", "No: of certs issued\033[1;m"))
    print("\033[1;93m{}|{}\033[1;m".format("_"*57, "_"*20))
    for result in cursor.fetchall():
        print(" {0:55} \033[1;93m|\033[1;m {1}".format(result[0].split('=')[-1], result[1]))

def get_limit():
    if len(sys.argv) <= 1:
        return 100
    else:
        return sys.argv[1]

if __name__ == '__main__':
    limit = get_limit()
    cursor = connect_to_db(limit)
    print_ca_stats(cursor, limit)