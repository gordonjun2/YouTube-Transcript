import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import urllib.request
import json
import urllib
import re

# To input

video_urls = ['https://www.youtube.com/watch?v=wNxUQ2sJtso']

# Do not need to modify below

transcripts_dir = './extracted_transcript'

formatter = TextFormatter()

if not os.path.exists(transcripts_dir):
    os.makedirs(transcripts_dir)

for video_url in video_urls:

    transcript = None

    video_id = video_url.split('=')[-1]

    # Retrieve video title
    params = {"format": "json", "url": "https://www.youtube.com/watch?v=%s" % video_id}
    url = "https://www.youtube.com/oembed"
    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())

    filename = re.sub('[^A-z0-9 -]', '', data['title']).replace(" ", " ") + '.txt'

    file_path = transcripts_dir + '/' + filename

    # Get transcript
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    except:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        for transcript in transcript_list:
            if transcript.is_translatable:
                transcript = transcript.translate('en').fetch()
                break

        if transcript == None:
            print("Video '" + filename + "' does not have English transcript. Skipping...")
            continue

    # .format_transcript(transcript) turns the transcript into a text string.
    txt_formatted = formatter.format_transcript(transcript)

    # Now we can write it out to a file.
    with open(file_path, 'w', encoding='utf-8') as txt_file:
        txt_file.write(txt_formatted)