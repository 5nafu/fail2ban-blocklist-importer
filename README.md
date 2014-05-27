fail2fan-blocklist-importer
===========================

A small script to import and ban IPs from a list (like from blocklist.de). The list has to be formatted one IP per line, with no additional text.

After fetching the list, the script will add each IP to fail2bans blocklist jail and trigger the actual banning by touching the appropiate log file.

Configuration
-------------

In the script, edit the configuration dict:
*   **socket:** The socket used by fail2ban
*   **url:** The URL of the list.
*   **logfile:** Full path of the Logfile used in the Jail configuration. This file will be crated if it does not exist.
*   **loglevel:** How much should be logged. Currently used values are: logging.DEBUG, logging.INFO, logging.ERROR

TODO
----

*   Get Socket and Logfile Configuration from fail2ban
*   handle unblocking of IPs

Credit
------

This script was inspired by [Kapsonfile](https://forum.blocklist.de/viewtopic.php?f=11&t=107#p333 "Thank you!")
