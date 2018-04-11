#-*-encoding:'utf-8'-*-

import re
import sys
import argparse
import logging
import json
import sqlite3


def readFromFile(hostsFileLocation,dbLocation):
    with open(hostsFileLocation) as fp:
        obj = json.load(fp)
        updateSQLite3(obj,dbLocation)


def updateSQLite3(hosts,dbLocation):
    conn = sqlite3.connect(dbLocation)
    c = conn.cursor()
    for host in hosts:
        name = host['name']
        ip = host['ip']
        port = host['port']
        description = host['description']
        auth = host['auth']
        username = ''
        password = ''
        if auth == 1:
            username = host['username']
            password = host['password']
        insertStmt = 'INSERT INTO core_client(name,ip,port,description,created_at,updated_at,password,username,auth) VALUES (?,?,?,?,?,?,?,?,?)'
        insertTuple = (name,ip,port,description,'','',password,username,auth)
        c.execute(insertStmt,insertTuple)
    conn.commit()
    conn.close()


def main():
    parser = argparse.ArgumentParser(description='import hosts into gerapy from file')
    parser.add_argument('hostsFile',type=str)
    parser.add_argument('db.sqlite3', type=str)
    args = parser.parse_args()
    hostsFileLocation = vars(args)['hostsFile']
    dbLocation = vars(args)['db.sqlite3']
    readFromFile(hostsFileLocation,dbLocation)

if __name__ == '__main__':
    main()
