import yaml

from captions_to_vtt import convert as captions_to_vtt
from config import *
from google.cloud import error_reporting
from text_to_ts_phrases import TextToTimestampPhrases
from ts_phrases_to_captions import convert as phrases_to_captions


def load_story():
	with open(STORY_FILE_PATH) as f:
		data = f.read()
	return yaml.load(data, Loader=yaml.FullLoader)


if __name__ == '__main__':
	error_client = error_reporting.Client()
	try:
		# Load story
		story = load_story()
		text = ' '.join(story['text']['normalized'])
		fa_words = story['forcedAligner']['words']
		# Convert text to timestamp-phrases
		ts_phrases = TextToTimestampPhrases().convert(text, fa_words)
		# Convert timestamp-phrases to captions
		captions = phrases_to_captions(ts_phrases)
		# Convert captions to vtt-captions
		duration = story['duration']
		data = captions_to_vtt(captions, duration)

		with open(CAPTIONS_FILE_PATH, 'w') as f:
			f.write(data)

	except Exception:
		error_client.report_exception()
		raise
