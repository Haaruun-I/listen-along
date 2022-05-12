from random import choice
import rfeed, opml
import feedparser
import toml, os

# TODO: go to backlog if there are no current shows that count
# TODO: keep track of played episodes
# TODO: export history to opml
# TODO: website frontend

settingsFile = 'feeds.toml'
outputFolder = "out"

settings = toml.load(settingsFile)

allFeeds = []
for category in settings['categories']:
    for feed in settings[category]: allFeeds.append(feed)

chosenShows = [] # no duplacites 
curratedShows = {}
for show in settings['show']:
    curratedShows[show['name']] = []
    for slot in show['schedule']:
        tags = slot.split()
        category = tags.pop(0)

        if category == "*":
            feedsInCategory = allFeeds
        elif category in settings['categories']:
            feedsInCategory = settings[category]
        else: raise KeyError()
    
        if tags:
            feedsWithTag = []
            for feed in feedsInCategory:
                if feed in chosenShows: continue
                for tag in tags:
                    if not 'tags' in feed: continue
                    elif not tag in feed['tags']: continue
                    else: feedsWithTag.append(feed)

            chosenFeed = choice(feedsWithTag)
        else:
            while True: # Temporary solution: yes ik it hangs if there are no qualifiyng shows left, 
                chosenFeed = choice(feedsInCategory)
                if not chosenFeed in chosenShows: break
        
        curratedShows[show['name']].append(chosenFeed)
        chosenShows.append(chosenFeed)

for showName, showFeed in curratedShows.items():
    feedItems = []
    for feed in showFeed:
        episode = feedparser.parse(feed['url']).entries[0]
        feedItems.append(rfeed.Item(
            title = episode['title'],
            link = episode['link'],
            author = episode['author']
        ))



    feed = rfeed.Feed(
        title = showName,
        description = f"Automaticly generated feed: {showName}",
        link = "localhost",
        items = feedItems
    )

    with open(os.path.join(outputFolder, f'{showName}.rss'), 'wx') as rss:
        rss.write(feed.rss())