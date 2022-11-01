#!/usr/bin/env python3

from TimestampConverter import TimestampConverter

import sys
import webbrowser

MANDATORY_PARAMETERS = ['--name', '--input', '--format', '--link']

def main():
    arguments = sys.argv[1:]
    for elem in MANDATORY_PARAMETERS:
        if elem not in arguments:
            print(f'{elem} not present!')
            exit(-1)
    output_name = arguments[arguments.index('--name') + 1]
    timestamp_input = arguments[arguments.index('--input') + 1]
    timestamp_format = arguments[arguments.index('--format') + 1]
    link = arguments[arguments.index('--link') + 1]

    converter = TimestampConverter(video_link=link, input=timestamp_input, format=timestamp_format)
    converter.generate_html(output_name)
    if '--open' in arguments:
        webbrowser.open(output_name)

    
if __name__ == '__main__':
    main()