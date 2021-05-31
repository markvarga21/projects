import urllib.request
import re

def key_convert(search):
	keywords_arr = search.split()
	search_key_mix = ""
	KEYWORD = ""
	if len(keywords_arr) > 1:
		for pk in keywords_arr:
			search_key_mix += pk
			search_key_mix += '+'
		KEYWORD = search_key_mix[:len(search_key_mix)-1]
	else:
		KEYWORD = keywords
	return KEYWORD

def title_to_url(searching):
	megtekintesszam_szerint = "&sp=CAM%253D"

	html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + key_convert(searching) + megtekintesszam_szerint)
	video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
	final_url = "https://www.youtube.com/watch?v=" + video_ids[0]
	return final_url


keywords = "mozart"

print("A legtobbet megtekintett video a {} kulcsszora:\n {}".format(keywords, title_to_url(keywords)))


