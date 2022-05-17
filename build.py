from src.backend.showGenerator.basicPlugins import BasicRSSPlugin, Interlude
from src.backend.showGenerator.showGenerator import Show
import toml, os.path

# TODO: go to backlog if there are no current shows that count
# TODO: keep track of played episodes
# TODO: export history to opml

settingsFile = 'src/feeds.toml'
outputFolder = "src/public/shows"

settings = toml.load(settingsFile)

for showSettings in settings['show']:
    show = Show(showSettings, [
        BasicRSSPlugin(settings["feed"]),
        Interlude(settings["music"])
    ])

    filePath = os.path.join(outputFolder, showSettings['title'] + ".rss")
    if not os.path.exists(filePath): os.mknod(filePath)

    with open(filePath, 'w') as rss:
        rss.write(str(show))