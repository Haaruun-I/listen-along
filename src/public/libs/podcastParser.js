const xmlParse = new DOMParser().parseFromString.bind(new DOMParser());

const getPodcastFromURL = (feedURL, callback) => {
  fetch(feedURL)
  .then(res => {res.text().then(res => {
        let parsedFeed = {}
        feed = xmlParse(res, 'text/xml')

        parsedFeed.title = feed.querySelector('title').textContent
        parsedFeed.episodes = []
        feed.querySelectorAll('item').forEach(episode => {
          parsedFeed.episodes.push({
            title: episode.querySelector('title').textContent,
            artist: episode.querySelector('author').textContent,
            src: episode.querySelector('link').textContent
          })
        
        })
        
        callback(parsedFeed)    
    })
  })
}