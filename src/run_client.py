#!/usr/bin/python

import settings

import client

if __name__ == "__main__":
    print "running client"
    settings.ENV = settings.CLIENT
    client.run()
    print "SUCCESS"
