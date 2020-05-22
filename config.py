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
REPLACE_DICT = {
	# Names
	'coronavirus': 'corona-virus',
	'Coronavirus': 'Corona-virus',
	'disney+': 'disney-plus',
	'Disney+': 'Disney-plus',
	'China': 'Chyna',
	# Tesla
	'Autopilot': 'Auto-pilot',
	'autopilot': 'auto-pilot',
	# Apple
	'iPhone': 'eYe-Phone',
	'iPad': 'eye-Pad',
	'iOS': 'i-Ooh-Ess',
	'macOS': 'mac-Ooh-Ess',
	'watchOS': 'watch-Ooh-Ess',
	'iPadOS': 'eYePad-Ooh-Ess',
	'AirPods': 'Air-Pods',
	# Misc words
	'schizophrenia': 'scheezo-phrehnia',
	'Schizophrenia': 'Scheezo-phrehnia',
	'email': 'eee-mail',
	'Email': 'Eee-mail',
	'PCs': 'Pee-Cees',
	'Sen.': 'Senator',
	'mobile': 'mo-ble',
	'Mobile': 'Mo-ble',
	'genome': 'geenome',
	'Genome': 'Geenome',
	'earbuds': 'ear-buds',
	'Earbuds': 'Ear-buds',
	'SUVs': 'EsS-EiuU-VeEs',
	'tablets': 'tahblets',
	'Tablets': 'Tahblets',
	'live ': 'li-vv ',
	'Live ': 'Li-vv ',
	' live': ' li-vv',
	' Live': ' Li-vv',
	'console': 'connsole',
	'Console': 'Connsole',
	'espionage': 'espio-nash',
	'online': 'on-line',
	'spreading': 'sprehding',
	'decade': 'deh-cade',
	'dinosaur': 'dyhna-sor',
	'Dinosaur': 'Dyhna-sor',
	# People
	'Assange': 'Assanhge',
	'Xi ': 'SHe ',
	' Xi': ' SHe',
	# Countries
	'Iraq': 'Eh-rak',
	'Iran': 'Eh-ran',
	# Pokemon
	'pokemon': 'pokeemonn',
	'Pokemon': 'Pokeemonn',
	'pokedex': 'poke-dex',
	'Pokedex': 'Poke-dex',
	'pikachu': 'peeka-chuu',
	'Pikachu': 'Peeka-chuu',
	# Company names
	'Alipay': 'Ali-pay',
	'WeChat': 'We-Chat',
	'Amazon': 'Aama-zon',
	'Reuters': 'Roters',
	'NVIDIA': 'EN-VIDIA',
	'Nvidia': 'EN-vidia',
	'nvidia': 'en-vidia',
	'AT&T': 'AE-TEE-AND-TEE',
	'at&t': 'ae-tee-and-tee',
	'ATandT': 'aE-Tee-and-Tee',
	'Android': 'Anndroid',
	'Bezos': 'Behssos',
	'XBox': 'Exx-Box',
	'xbox': 'exx-Box',
	'Xbox': 'exx-box',
	'yahoo': 'ya-hoo',
	'Yahoo': 'Ya-hoo',
	'Huawei': 'Whahwaee',
	'Xiaomi': 'She-a-omee',
	'Hobbi': 'hObBy',
	# Space
	'SpaceX': 'Space-Exx',
	'NASA': 'Na-Sah',
	'Jupiter': 'Jupee-ter',
	'Venus': 'Veenus',
	'satellites': 'sahtelaets',
	'Satellites': 'sahtelaets',
	'satellite': 'sahtelaet',
	'Satellite': 'sahtelaet',
}
SPACY_MODEL_NAME = 'en_core_web_sm'
STORY_FILE_PATH = '/data/story.yaml'
