import config
import spacy


class TextToTimestampPhrases(object):

	def __init__(self):
		self.nlp = spacy.load(config.SPACY_MODEL_NAME)

	def _align_phrases_with_forced_aligned_words(self, phrases, fa_words):
		i = 0
		aligned_fa_indexes = []

		for phrase in phrases:
			a = 0
			attempts = 0
			index = []

			while a < len(phrase) and i < len(fa_words):
				token = phrase[a]
				if token['text'] in config.BREAK_TOKENS:
					if len(index) > 0:
						index[-1] = index[-1][0], True # position, if-break-token
					break

				token_text = token['text'].lower().replace('.', '') # as in "Mr.", "I. O. S."
				fa_word_text = fa_words[i]['word'].lower().replace('.', '') # as in "Mr.", "I. O. S."

				if token_text == fa_word_text:
					print('	', token_text, fa_word_text)
					index.append((i, False)) # position, if-break-token
					i += 1
					attempts = 0
				else:
					print('!' * 30, token_text, fa_word_text)
					attempts += 1

				if config.MAX_SKIP_TOKENS == attempts:
					i += 1 # Skip current
					a -= config.MAX_SKIP_TOKENS
					attempts = 0
					print('--> skip')
				else:
					a += 1

			if len(index) > 0:
				aligned_fa_indexes.append(index)

		assert len(aligned_fa_indexes) == len(phrases)

		return aligned_fa_indexes

	def _check_forced_aligned_words(self, fa_words):
		checked_list = []

		for aligned_word in fa_words:
			word = aligned_word['word'].strip()
			for k, v in config.PUNCT_TO_DICTIONARY.items():
				word = word.replace(k, '')

			if 'end' not in aligned_word or 'start' not in aligned_word:
				checked_list.append(aligned_word)
				continue

			tokens = self.nlp.tokenizer(word)
			tokens = list(tokens)
			num_tokens = len(tokens)
			duration = aligned_word['end'] - aligned_word['start']

			for i in range(0, num_tokens):
				start = aligned_word['start'] + (duration / num_tokens * i)
				right_offset = num_tokens - (i + 1)
				end = aligned_word['end'] - (duration / num_tokens * right_offset)
				new_word = {
					'start': start,
					'end': end,
					'word': tokens[i].text
				}
				checked_list.append(new_word)

		return checked_list

	def _find_closest_time(self, fa_words, side, index, prev_break, next_break):
		# Looks for closest token on the left
		left = None
		for i in range(1, config.MAX_SKIP_TOKENS + 1):
			if index - i < 0:
				break
			token = fa_words[index - i]
			if 'end' in token:
				left = i, token['end'] # distance, time
				break

		# Looks for closest token on the right
		right = None
		for i in range(1, config.MAX_SKIP_TOKENS + 1):
			if index + i + 1 > len(fa_words):
				break
			token = fa_words[index + i]
			if 'start' in token:
				right = i, token['start'] # distance, time
				break

		assert (bool(left) or bool(right))

		# Select time
		if left == None and right[0] == 1:
			if side == 'start':
				return right[1] - config.AVG_DURATION_PER_WORD
			else:
				return right[1]

		elif left == None and right[0] > 1:
			if side == 'start':
				return right[1] - (config.AVG_DURATION_PER_WORD * abs(right[0] - index))
			else:
				return right[1] - (config.AVG_DURATION_PER_WORD * abs(right[0] - (index + 1)))

		elif left[0] == 1 and right == None:
			if side == 'start':
				return left[1]
			else:
				return left[1] + config.AVG_DURATION_PER_WORD

		elif left[0] == 1 and right[0] == 1:
			if side == 'start':
				if prev_break:
					return right[1] - config.AVG_DURATION_PER_WORD
				else:
					return left[1]
			else:
				if next_break:
					return left[1] + config.AVG_DURATION_PER_WORD
				else:
					return right[1]

		elif left[0] == 1 and right[0] > 1:
			if side == 'start':
				return left[1]
			else:
				return left[1] + config.AVG_DURATION_PER_WORD

		raise Exception('No condition met')

	def _get_phrases(self, text):
		text = text.replace('-', ' ') # split words such as in-law, dry-cleaning
		text = text.replace('+', ' ') # split words such as Wieden+Kennedy

		for k, v in config.PUNCT_TO_DICTIONARY.items():
			text = text.replace(k, v)

		doc = self.nlp(text)
		phrases = []
		tokens = []

		for sent in doc.sents:
			for token in sent:
				if token.text.strip() == '':
					continue
				token = {
					'idx': token.idx,
					'text': token.text.strip()
				}
				tokens.append(token)
				t_text = token['text']
				if t_text in config.BREAK_TOKENS:
					if t_text in config.PUNCT_BACK_DICTIONARY.keys():
						replace_text = config.PUNCT_BACK_DICTIONARY[t_text]
						tokens[-1]['text'] = t_text.replace(t_text, replace_text)
					phrases.append(tokens)
					tokens = []

		return phrases

	def _timestamp_phrases(self, text, phrases, fa_words, aligned_fa_indexes):
		phrase_ts = []
		prev_break = None
		print('text:')
		print(text)
		print('aligned_fa_indexes:')
		print(aligned_fa_indexes)

		for i, index in enumerate(aligned_fa_indexes):
			words_ts = []

			for a, next_break in index:
				fa_word = fa_words[a]

				if 'start' not in fa_word:
					fa_word['start'] = self._find_closest_time(fa_words, 'start', a, prev_break, next_break)

				if 'end' not in fa_word:
					fa_word['end'] = self._find_closest_time(fa_words, 'end', a, prev_break, next_break)

				timestamp = fa_word['start'], fa_word['end']
				words_ts.append(timestamp)
				prev_break = next_break

			start = phrases[i][0]['idx']
			last_token = phrases[i][-1]
			end = last_token['idx'] + len(last_token['text'])
			caption_text = text[start:end]

			phrase_ts.append({
				'text': caption_text,
				'timestamps': words_ts
			})

		return phrase_ts

	def convert(self, text, fa_words):
		text = text.replace('."', '".')
		text = text.replace(',"', '",')
		phrases = self._get_phrases(text)
		fa_words = self._check_forced_aligned_words(fa_words)
		aligned_fa_indexes = self._align_phrases_with_forced_aligned_words(phrases, fa_words)
		ts_phrases = self._timestamp_phrases(text, phrases, fa_words, aligned_fa_indexes)

		return ts_phrases
