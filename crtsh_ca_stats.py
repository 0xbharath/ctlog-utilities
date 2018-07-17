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

def connect_to_db(domain_name):
    try:
        conn = psycopg2.connect("dbname={0} user={1} host={2}".format(DB_NAME, DB_USER, DB_HOST))
        cursor = conn.cursor()
        cursor.execute("SELECT distinct  ca.name, COUNT(*) count FROM certificate_identity ci, ca ca WHERE ci.NAME_TYPE = 'dNSName' AND reverse(lower(ci.NAME_VALUE)) LIKE reverse(lower('%{0}')) AND ca.id=ci.issuer_ca_id GROUP BY ca.name ORDER BY count desc;".format(domain_name))
    except:
        print("\n\033[1;31m[!] Unable to connect to the database\n\033[1;m")
    return cursor

def print_ca_stats(cursor, domain_name):
    print("\n\033[1;94mCertificate Authority(CA) stats for the domain - {}\033[1;m".format(domain_name))
    print("\n\033[1;93m{:56} | {}".format("Certificate Authority(CA)", "No: of certs issued\033[1;m"))
    print("\033[1;93m_________________________________________________________|______\033[1;m")
    for result in cursor.fetchall():
        print(" {0:55} \033[1;93m|\033[1;m {1}".format(result[0].split('=')[-1], result[1]))

def get_domain_name():
    if len(sys.argv) <= 1:
        print("\n\033[33mUsage: python crtsh_enum_psql.py <target_domain>\033[1;m\n")
        sys.exit(1)
    else:
        return sys.argv[1]

if __name__ == '__main__':
    domain_name = get_domain_name()
    cursor = connect_to_db(domain_name)
    print_ca_stats(cursor, domain_name)