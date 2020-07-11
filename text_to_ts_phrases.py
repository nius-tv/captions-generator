from config import *


class TextToTimestampPhrases(object):

	def _get_index(self, expanded, i):
		index = 0
		for a, parts in enumerate(expanded):
			if not isinstance(parts, list):
				parts = [parts]

			for part in parts:
				pieces = part.split('-')
				for _ in pieces:
					if index == i:
						is_list = len(parts) > 1 or len(pieces) > 1
						return is_list, a
					index += 1

	def convert(self, text, fa_words):
		expanded = text['expanded']
		normalized = text['normalized']
		phrases = []
		timestamps = []

		prev_i = None
		was_list = False
		for i, fa_word in enumerate(fa_words):
			is_list, norm_i = self._get_index(expanded, i)

			if not was_list:
				start = fa_word['start']

			if is_list:
				was_list = True
				end = fa_word['end']
				continue

			if was_list:
				was_list = False
				timestamps.append((start, end))

			start = fa_word['start']
			end = fa_word['end']
			timestamps.append((start, end))

			if normalized[norm_i][-1] in BREAK_TOKENS:
				text = normalized[prev_i:norm_i+1]
				text = ' '.join(text).strip()
				phrase = {
					'text': text,
					'timestamps': timestamps
				}
				phrases.append(phrase)
				prev_i = norm_i + 1
				timestamps = []

		if was_list or len(timestamps) > 0:
			timestamps.append((start, end))
			text = normalized[prev_i:norm_i+1]
			text = ' '.join(text).strip()
			phrase = {
				'text': text,
				'timestamps': timestamps
			}
			phrases.append(phrase)

		return phrases
