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


def justify_tokens(tokens):
	candidates = []
	completed = False
	num_cand_attempts = 0
	num_tokens = len(tokens)
	offsets = {}
	print('tokens:', tokens)

	while not completed and num_cand_attempts < config.MAX_NUM_CAND_SEARCH_ATTEMPTS:
		num_cand_attempts += 1
		i = 0
		ini = 0
		phrases = []

		while i < num_tokens:
			t_window = tokens[ini:i+1]
			text_len = sum(len(t) for t in t_window) + len(t_window)
			num_p = len(phrases)

			if i + 1 == len(tokens) and text_len <= config.MAX_CAPTION_LETTERS:
				phrases.append(t_window)

				if text_len > config.MIN_CAPTION_LETTERS \
					and (len(phrases) == 1 or len(phrases) == len(offsets.keys())):
					completed = True
				break

			elif text_len > config.MAX_CAPTION_LETTERS:
				offset = offsets.get(num_p, 0)
				offsets[num_p] = offset + 1

				i -= offset
				phrases.append(tokens[ini:i])

				prev_window = tokens[ini:(i - 1)]
				prev_text_len = sum(len(t) for t in prev_window) + len(prev_window)

				if prev_text_len < config.MIN_CAPTION_LETTERS:
					offsets[num_p] = 0
					num_p += 1
					offsets[num_p] = offsets.get(num_p, 0) + 1

				ini = i
			else:
				i += 1

		candidates.append(phrases)

	# Select top first candidate
	scored = score_candidates(candidates)
	score = sorted(scored)[0] # get first (lowest) desc key
	return scored[score][0]


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
