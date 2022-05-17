getPodcastFromURL("shows/Bedtime.rss", feed => {
    episodeList = feed.episodes
    console.table(episodeList)
    const player = new Shikwasa({
        container: () => document.querySelector('main'),
        download: true,
        autoplay: true,
        theme: "dark",
        themeColor: "red",
        audio: episodeList.shift()
    })


    player.on('ended', () => {
        player.update(episodeList.shift())
    })
})