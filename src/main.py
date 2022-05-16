from showGenerator.basicPlugins import BasicRSSPlugin, Interlude
from showGenerator.showGenerator import Show
import toml, os

# TODO: go to backlog if there are no current shows that count
# TODO: keep track of played episodes
# TODO: export history to opml
# TODO: website frontend

settingsFile = 'feeds.toml'
outputFolder = "public/shows"

print('bla')

settings = toml.load(settingsFile)

for showSettings in settings['show']:
    show = Show(showSettings, [
        BasicRSSPlugin(settings["feed"]),
        Interlude(settings["music"])
    ])

    with open(os.path.join(outputFolder, f"{showSettings['title']}.rss"), 'w') as rss:
        rss.write(str(show))