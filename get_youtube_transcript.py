import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import urllib.request
import json
import urllib

video_urls = ['https://www.youtube.com/watch?v=eyCQrMuJpEk',
            'https://www.youtube.com/watch?v=mO6twStYiCc']

transcripts_dir = './extracted_transcript'

formatter = TextFormatter()

if not os.path.exists(transcripts_dir):
    os.makedirs(transcripts_dir)

for video_url in video_urls:

    video_id = video_url.split('=')[-1]

    # Must be a single transcript.
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # .format_transcript(transcript) turns the transcript into a text string.
    txt_formatted = formatter.format_transcript(transcript)

    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())

    file_path = transcripts_dir + '/' + data['title'].replace(' ', '_') + '.txt'

    # Now we can write it out to a file.
    with open(file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(txt_formatted)