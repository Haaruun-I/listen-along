from src.backend.showGenerator.showGenerator import BasePlugin

from random import choice

import feedparser
import logging


class BasicRSSPlugin(BasePlugin):
    customFlags = {
        "n": 'getShowByName',
        "t": 'getShowByTags'
    }

    def __init__(self, feedList):
        self.feedList = feedList
        self.playedFeeds = []

    def getShowByName(self, args):
        candidateFeeds = list(filter(lambda feed: args[0] == feed['title'] and
                            not feed in self.playedFeeds,  self.feedList))
        if not candidateFeeds: raise AttributeError("No show with name " + args[0])

        return candidateFeeds

    def getShowByTags(self, args):
        candidateFeeds = list(filter(
                lambda feed: all(category in feed['tags'] for category in args) and
                            not feed in self.playedFeeds,
                self.feedList ))
        if not candidateFeeds: raise AttributeError("No show with tags " + args)

        return candidateFeeds

    def pickFeed(self, candidateFeeds):
        return choice(candidateFeeds)

    def pickEpisode(self, chosenFeed):
        episode = feedparser.parse(chosenFeed['url']).entries[0]
        for enclosure in episode.enclosures:
                if not enclosure['type'].split('/')[0] == "audio": continue
                else: episode['link'] = enclosure['href']

        return episode

class Interlude(BasePlugin):
    def __init__(self, musicList):
        self.musicList = musicList

    def alterTimetable(self, ogTimetabe):
        if not 'interlude' in self.show.showSettings: return ogTimetabe
        elif not self.show.showSettings['interlude']: return ogTimetabe

        newTimetable = []
        for timeslot in ogTimetabe:
            newTimetable.append(timeslot)

            music = choice(self.musicList)
            music['description'] = "Short musical break"
            
            newTimetable.append(music)

        return newTimetable