import config

from statistics import *


def convert(ts_phrases):
	all_captions = []
	tmp_ts_phrases = []

	for ts_phrase in ts_phrases:
		tmp_ts_phrases.append(ts_phrase)

		if ts_phrase['text'][-1] in config.NEW_LINE_TOKENS:
			captions = sentence_to_captions(tmp_ts_phrases)
			all_captions.extend(captions)
			tmp_ts_phrases = []

	return all_captions


def get_all_tokens_and_timestamps(ts_phrases):
	all_tokens = []
	all_ts = []

	for ts_phrase in ts_phrases:
		tokens = ts_phrase['text'].split(' ')
		all_tokens.extend(tokens)

		ts = ts_phrase['timestamps']
		all_ts.extend(ts)

	return all_tokens, all_ts




def sentence_to_captions(ts_phrases):
	captions = []
	count = 0
	tokens, timestamps = get_all_tokens_and_timestamps(ts_phrases)
	justified_phrases = justify_tokens(tokens)
	
	for phrase_tokens in justified_phrases:
		ini = timestamps[count]
		count += len(phrase_tokens)
		end = timestamps[count - 1]

		caption = {
			'start': ini[0],
			'end': end[1],
			'text': ' '.join(phrase_tokens)
		}
		print('-', caption['text'])
		captions.append(caption)

	return captions


def score_candidates(candidates):
	scored = {}

	for cand in candidates:
		# Create list with phrase lenghts
		phrase_lens = [len(' '.join(phrase)) for phrase in cand]
		# Calculate standard deviation of phrase lenghts
		score = pstdev(phrase_lens)

		if score not in scored:
			scored[score] = []
		scored[score].append(cand)

	return scored
