from src.backend.showGenerator.basicPlugins import BasicRSSPlugin, Interlude
from src.backend.showGenerator.showGenerator import Show
import toml, os.path

# TODO: go to backlog if there are no current shows that count
# TODO: keep track of played episodes
# TODO: export history to opml

settingsDir = 'settings/'
settingsFile = settingsDir + "main.toml"
outputFolder = "src/public/shows"

settings = toml.load(settingsFile)

imports = 'imports' in settings # so we can do recursive imports
while imports:
    for index, path in enumerate(settings['imports']):
        settings.update(toml.load(settingsDir + path))
        settings['imports'].pop(index)
    imports = settings['imports']

for showSettings in settings['show']:
    show = Show(showSettings, [
        BasicRSSPlugin(settings["feed"]),
        Interlude(settings["music"])
    ])

    filePath = os.path.join(outputFolder, showSettings['title'] + ".rss")
    if not os.path.exists(filePath): os.mknod(filePath)

    with open(filePath, 'w') as rss:
        rss.write(str(show))