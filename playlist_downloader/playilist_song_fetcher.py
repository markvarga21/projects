from pytube import Playlist, YouTube
from unidecode import unidecode

url = "https://youtube.com/playlist?list=PLgNTtfR_wPZe06lsaYGbvGGWi8Vg48plu"

playlist = Playlist(url)

video_urls = playlist.video_urls

path = "./music/"

for url in video_urls:
  try:
    yt = YouTube(url)
    title = yt.title
    converted_title = unidecode(title)
    if title != "Video Not Available":
      audio_stream = yt.streams.filter(only_audio=True).first()
      out_file = audio_stream.download(filename=f'{converted_title}.mp3', output_path=path)
      print(converted_title + " has been successfully downloaded.")
    else:
      print(f"Video not found for URL: {url}")
  except Exception:
    print("Something went wrong!")

