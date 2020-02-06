# Warning: the position of these variables is sensitive.
# Keep them on top.
PUNCT_BACK_DICTIONARY = {
	'xxx0001': '!".'
}
# End of sensitive variables.
AVG_DURATION_PER_WORD = 0.5 # in seconds
BREAK_TOKENS = ['.', ',', ';', '?', '!'] + list(PUNCT_BACK_DICTIONARY.keys())
CAPTIONS_FILE_PATH = '/data/captions.vtt'
CAPTIONS_STYLE = 'align:center line:-9 position:50% size:85%'
END_DURATION_OFFSET = 1.5 # in seconds
MAX_CAPTION_LETTERS = 35
MAX_NUM_CAND_SEARCH_ATTEMPTS = 500
MAX_SKIP_TOKENS = 3
MIN_CAPTION_LETTERS = 25
NEW_LINE_TOKENS = ['.', '?', '!']
PUNCT_TO_DICTIONARY = {
	'!".': ' xxx0001'
}
SPACY_MODEL_NAME = 'en_core_web_sm'
STORY_FILE_PATH = '/data/story.yaml'
