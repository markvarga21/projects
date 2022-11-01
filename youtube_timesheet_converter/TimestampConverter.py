from unittest.loader import VALID_MODULE_NAME

from InvalidFormatException import InvalidFormatException

class TimestampConverter:
    """This class converts a given timestamp collection to youtube video links."""
    EMBEDDED_VIDEO_WIDTH = 960
    EMBEDDED_VIDEO_HEIGHT = 540

    VALID_FORMATS = ['mm:ss - description']

    BASE_HTML = """<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@100;400&display=swap" rel="stylesheet">
        <title>Szkriptnyelvek</title>
        <style>
            h2 {
                font-family: 'Montserrat', sans-serif;
            }
        </style>
    </head>
    <body>
        #TODO
    </body>
    </html>"""

    def __init__(self, video_link: str, input: str, format='mm:ss - description') -> None:
        if format not in TimestampConverter.VALID_FORMATS:
            raise InvalidFormatException(f'Format {format} is invalid!')
        self.input = input
        self.video_link = video_link
        self.format = format



    def get_data(self) -> list:
        data = []
        with open(self.input, encoding='utf-8') as f:
            data = f.readlines()
        if len(data) == 0:
            raise EOFError(f'File {self.input} is empty!')
        clean_data = [str(elem).replace('\n', '') for elem in data]
        time_description_tuple_list= []
        for elem in clean_data:
            time, description = elem.split('-', 1)
            time_description_tuple_list.append((time.strip(), description.strip()))
        
        full_data = []

        for elem in time_description_tuple_list:
            t, d = elem
            m, s = t.split(':')
            full_data.append((int(s) + int(m) * 60, d))

        links_with_descriptions = []

        id_start_index = self.video_link.find('v=')+2
        id_end_index = self.video_link.find('&')
        video_id = self.video_link[id_start_index:id_end_index]
        embedded_video_link = f'https://www.youtube.com/embed/{video_id}'

        for elem in full_data:
            t, d = elem
            link = f'{embedded_video_link}?start={t}'
            links_with_descriptions.append((link, d))


        return links_with_descriptions


    def generate_divs(self) -> str:
        div_list = []
        ls = self.get_data()
        for link, description in ls:
            div = """<hr class="rounded">
            <div>
                <h2>{}</h2>
                <iframe width="{}" height="{}" src="{}"></iframe>
            </div>""".format(
                description,
                TimestampConverter.EMBEDDED_VIDEO_WIDTH, 
                TimestampConverter.EMBEDDED_VIDEO_HEIGHT,  
                link
            )
            div_list.append(div)
        all_divs = ''.join(div_list)
        return all_divs

    def generate_html(self, name: str) -> None:
        data = self.generate_divs()
        with open(name, 'w', encoding='utf-8') as w:
            w.write(TimestampConverter.BASE_HTML.replace('#TODO', data))
