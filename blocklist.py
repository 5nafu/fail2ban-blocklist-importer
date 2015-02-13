#!/usr/bin/env python

import sys
import logging
import urllib2
import socket

# Inserts our own modules path first in the list
# fix for bug #343821
sys.path.insert(1, "/usr/share/fail2ban")

# Now we can import our modules
from client.csocket import CSocket

logSys = logging.getLogger("fail2ban.client")


class Blocklistimporter:
    def __init__(self):
        self.__conf = dict()
        self.__conf["socket"] = "/var/run/fail2ban/fail2ban.sock"
        self.__conf["url"] = "https://api.blocklist.de/getlast.php?time=300"
        self.__conf["logfile"] = "/etc/fail2ban/empty.log"
        self.__conf["loglevel"] = logging.ERROR


    def fetch_list(self):
        logSys.debug("Fetching IPs")
        try:
            listcontent = urllib2.urlopen(self.__conf["url"]).readlines()
        except urllib2.URLError as e:
          sys.exit("Cannot fetch URL: %s", e)
        logSys.debug("Got IPs")
        return listcontent

    def block_ip(self, ip):
        try:
            client = CSocket(self.__conf["socket"])
            command = ["set", "blocklist", "banip"]
            logSys.debug("Blocking %s" % ip)
            ret = client.send(command + [ip])
            if ret[0] == 0:
                logSys.debug("OK : " + `ret[1]`)
            else:
                print ret
                logSys.debug("NOK: %s = %s" % (ret[1].args, ret[1]))
                return False
        except socket.error:
            logSys.error("Unable to contact server. Is it running?")
            return False
        except Exception, e:
            logSys.error(e)
            return False
        return True

    def start(self):
        logSys.setLevel(self.__conf["loglevel"])
        stdout = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(levelname)-6s %(message)s')
        stdout.setFormatter(formatter)
        logSys.addHandler(stdout)

        listcontent = self.fetch_list()
        for ip in listcontent:
            try:
                self.block_ip(ip.rstrip())
            except Exception, e:
                logSys.debug("Got exception: %s" % str(e))
                return False
        logSys.debug("Touching log to ban new IPs")
        open(self.__conf["logfile"], 'w').close
        return True

if __name__ == "__main__":
    importer = Blocklistimporter()
    if importer.start():
        sys.exit(0)
    else:
        sys.exit(-1)
