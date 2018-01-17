betubedl (better-youtubed-downloader)
==================================================
A Python library for downloading YouTube videos

Description
--------------------------------------
YouTube is an American video-sharing website headquartered in San Bruno, California. YouTube allows users to upload, view, rate, share, add to favorites, report, comment on videos, and subscribe to other users. It primarily uses the VP9 and H.264/MPEG-4 AVC formats and Dynamic Adaptive streaming over HTTP to display a wide variety of user-generated and corporate media videos. Available content includes video clips, TV show clips, music videos, short and documentary films, audio recordings, movie trailers, live streams, and other content such as video blogging, short original videos, and educational videos. Most of the content on YouTube is uploaded by individuals, but media corporations including CBS, the BBC, Vevo, and Hulu offer some of their material via YouTube as part of the YouTube partnership program. Unregistered users can only watch videos on the site, while registered users are permitted to upload an unlimited number of videos and add comments to videos. Videos deemed potentially inappropriate are available only to registered users affirming themselves to be at least 18 years old.

Youtube has a lot of excellent resources, based on this point and reference to the source of the pytube library, I write a lightweight python library. The library does not rely on third parties, crawling through the crawler youtube page and to download resources.

Installation
--------------------------------------

Download using pip via pypi.

`pip install betubedl`

Instructions for use
--------------------------------------

```
# import the module
from betubedl import Better_Youtube_Downloader

# I study in Korea, open youtube home page, all beautiful girls dancing, I also inevitably vulgar. Instantiate the object and pass the video URL you want to download as a parameter string to the instance
betubedl = Better_Youtube_Downloader('https://www.youtube.com/watch?v=t_sE1A8jEKE&list=PLy788G47tdSQnIp3Fip5NzP_qRMnD6Gd7')

# Display all the contents of video files that can be downloaded
print betubedl.get_videos()

    # [<Video: (.3gp) - 144p>,
    #  <Video: (.3gp) - 240p>,
    #  <Video: (.flv) - 240p>,
    #  <Video: (.flv) - 360p>,
    #  <Video: (.flv) - 480p>,
    #  <Video: (.mp4) - 360p>,
    #  <Video: (.mp4) - 720p>,
    #  <Video: (.webm) - 360p>,
    #  <Video: (.webm) - 480p>]

# Display video file name, when not set the file name, it will automatically crawl the original video name
print betubedl.getVideoName()

# Set the video file name
betubedl.setVideoName("XXXXX")

# As the sort is by definition from low to high, so you can use the -1 index to the highest definition version, by screeningVideo () API instantiation video object.
video = betubedl.screeningVideo(extension='mp4')[-1]

# The get_video_url () API that calls the video object returns the filtered url address
video.get_video_url()

# The get_logo_url () API that calls the video object returns the cover map address of the crawled video
video.get_logo_url()

# Use video object download () API download to the specified path
video.download('D://')
```
