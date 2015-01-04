#!/bin/env python

import sys, os, warnings, configparser

from xbmcjson import XBMC

# some hack, sorry...
warnings.filterwarnings("ignore", category=UserWarning, module='urllib')


class XBMLLibStat:
    def __init__(self):
        configdata = self.readConfig()
        self.client = XBMC(configdata['host'], configdata['user'], configdata['password'])

        if self.client == None:
            raise Exception("Connection error")        

        pong = self.client.JSONRPC.Ping()
        if pong["result"] != 'pong':
            raise Exception("Connection error")        
            return 1

        
    def readConfig(self):
        if os.path.exists('config.ini'):
            config = configparser.SafeConfigParser()
            config.read('config.ini')
            if 'XBMC' in config:
                return config["XBMC"]
        else:
            raise Exception("'config.ini' file not found")        
            return 1


    def getDatas(self):
        movies_all_q = self.client.VideoLibrary.GetMovies()
        movies_all = movies_all_q["result"]["limits"]["total"]
            
        movies_watched_q = self.client.VideoLibrary.GetMovies({"filter": {"field": "playcount", "operator": "greaterthan", "value": "0"}})    
        movies_watched = movies_watched_q["result"]["limits"]["total"]
        
        tvshows_all_q = self.client.VideoLibrary.GetTVShows()
        tvshows_all = tvshows_all_q["result"]["limits"]["total"]
        
        tvshows_watched_q = self.client.VideoLibrary.GetTVShows({"filter": {"field": "playcount", "operator": "greaterthan", "value": "0"}})
        tvshows_watched = tvshows_watched_q["result"]["limits"]["total"]
        
        tvshows_episodes_q = self.client.VideoLibrary.GetEpisodes()
        tvshows_episodes = tvshows_episodes_q["result"]["limits"]["total"]
        
        tvshows_episodes_watched_q = self.client.VideoLibrary.GetEpisodes({"filter": {"field": "playcount", "operator": "greaterthan", "value": "0"}})
        tvshows_episodes_watched = tvshows_episodes_watched_q["result"]["limits"]["total"]
        
        return {
            'movies_all' : movies_all,
            'movies_watched' : movies_watched,
            'tvshows_all' : tvshows_all,
            'tvshows_watched' : tvshows_watched,
            'tvshows_episodes' : tvshows_episodes,
            'tvshows_episodes_watched' : tvshows_episodes_watched,
        }
        
    def createMessage(self):
        datas = self.getDatas()
        messageStr  = "\nXBMC Library Stat 1.0"
        messageStr += "\n---------------------\n"
        messageStr += "\nTV Shows"
        messageStr += "\n--------"
        messageStr += "\ntotal:              {}"
        messageStr += "\nwatched:            {}"
        messageStr += "\nepisodes:           {}"
        messageStr += "\nepisodes_watched:   {}"
        messageStr += "\n\nMovies"
        messageStr += "\n-------"
        messageStr += "\ntotal:              {}"
        messageStr += "\nwatched:            {}\n"
        return messageStr.format(
            datas["tvshows_all"],
            datas["tvshows_watched"],
            datas["tvshows_episodes"],
            datas["tvshows_episodes_watched"],
            datas["movies_all"],
            datas["movies_watched"],
        )
        
        
        
    def drawMessage(self):
        print(self.createMessage())
        
        

def main():
    try:
        p = XBMLLibStat()
        p.drawMessage()
        return 0
    except Exception as err:
        sys.stderr.write('\nERROR: %s\n\n' % str(err))
        return 1    
   

if __name__=="__main__":
    sys.exit(main())