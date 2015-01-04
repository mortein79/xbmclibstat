xbmclibstat
===========

Command line utility that read library stat from the famous XBMC/KODI media player over the JSON RPC.

Requirements:
-------------

* Python 3
* [xbmcjson library](https://github.com/jcsaaddupuy/python-xbmc)
* XBMC/KODI with activated [Webserver JSON RPC access](http://kodi.wiki/view/Webserver)

Usage
-----

Just run it, no additional parameters. But required a _config.ini_ file in same folder.

```
[XBMC]
host = http://<URL>:[<port>]/jsonrpc
user = <username>
password = <userpassword>
```
