from random import choice
import rfeed, feedparser

class BasePlugin():
    customFlags = {}

    def initializingShow(self, show):
        self.show = show

    def pickEpisode(self, chosenFeed):
        return chosenFeed

    def pickFeed(self, candidateFeeds):
        return candidateFeeds

    def alterTimetable(self, timetable):
        return timetable

class Show:
    def __init__(self, showSettings, plugins=[]):
        self.showSettings = showSettings
        self.plugins = plugins

        if not type(self.plugins) == list: raise AttributeError("You need atleast one plugin.")

        self.customFlags = {}
        for plugin in self.plugins:
            for flag, method in plugin.customFlags.items():
                self.customFlags[flag] = getattr(plugin, method)

        itunesDetails = rfeed.iTunes(
            image = showSettings['image']
                if 'image' in showSettings else "localhost/static/mic-art.jpg",
        )

        timetable = map(self.parseParameters, showSettings['timetable'])
        self.feed = rfeed.Feed(
            title = showSettings['title'],
            description = showSettings['description'] 
                if 'description' in showSettings else "Automatic show: " + showSettings['title'],
            link = showSettings['url']
                if 'url' in showSettings else "localhost",
            extensions = [itunesDetails],
            items = self.fillTimetable(timetable)
        )

    def parseParameters(self, parameters):
        # args = self.parser.parse_args(shlex.split(parameters)) // maybe later
        args = parameters.split()
        flag = args.pop(0)[1:]

        if flag in self.customFlags.keys(): candidateFeeds = self.customFlags[flag](args)
        else: AttributeError("Please pick a supported mode with a - followed by the flag letter")
        
        return candidateFeeds

    def fillTimetable(self, timetable):
        filledTimetable = []
        for candidateFeeds in timetable:
            chosenFeed = self.runPlugins('pickFeed', candidateFeeds)
            filledTimetable.append(self.runPlugins('pickEpisode', chosenFeed))

        filledTimetable = self.runPlugins('alterTimetable', filledTimetable)
        outputFeed = []
        for episode in filledTimetable:
            details = []
            if 'image' in chosenFeed:
                details = [ rfeed.iTunesItem(image = chosenFeed.image['href']) ]
            
            outputFeed.append(rfeed.Item(
                title = episode['title'],
                link = episode['link'],
                author = episode['author'],
                description = episode['description'],
                extensions = details
            ))

        return outputFeed

    def runPlugins(self, stage, parameters): # Cannot think of a better name
        for plugin in self.plugins:
            plugin.initializingShow(self)
            try: 
                stageMethod = getattr(plugin, stage)
                parameters = stageMethod(parameters)
            except AttributeError: NotImplementedError("Please extend the BasePlugin class, " + plugin + " dosnt, dont be like them.")
            

        return parameters

    def __str__(self):
        return self.feed.rss()