import unittest

from text_to_ts_phrases import TextToTimestampPhrases


class TestTextToTimestampPhrases(unittest.TestCase):

	text_to_phrases = TextToTimestampPhrases()

	def test_replace_chars(self):
		text = {
			'expanded': [['Aih', 'bEE', 'CeE'], 'news.'],
			'normalized': ['ABC', 'news.']
		}
		fa_words = [
			{
				'start': 0.0,
				'end': 0.5,
				'word': 'Aih'
			},
			{
				'start': 0.5,
				'end': 1.0,
				'word': 'bEE'
			},
			{
				'start': 1.0,
				'end': 1.5,
				'word': 'CeE'
			},
			{
				'start': 1.5,
				'end': 2.0,
				'word': 'news'
			}
		]
		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'ABC news.',
				'timestamps': [(0.0, 1.5), (1.5, 2.0)]
			}
		]

		text = {
			'expanded': ['News', ['Aih', 'bEE', 'CeE.']],
			'normalized': ['News', 'ABC.']
		}
		fa_words = [
			{
				'start': 0.0,
				'end': 0.5,
				'word': 'news'
			},
			{
				'start': 0.5,
				'end': 1.0,
				'word': 'Aih'
			},
			{
				'start': 1.0,
				'end': 1.5,
				'word': 'bEE'
			},
			{
				'start': 1.5,
				'end': 2.0,
				'word': 'CeE'
			}
		]
		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'News ABC.',
				'timestamps': [(0.0, 0.5), (0.5, 2.0)]
			}
		]

	def test_split_phrases(self):
		text = {
			'expanded': ['Yes', 'I', 'win,', ['nineteen', 'eighty', 'six'], 'was', 'it.'],
			'normalized': ['Yes', 'I', 'win,', '1986', 'was', 'it.']
		}
		fa_words = [
			{
				'start': 0.0,
				'end': 0.5,
				'word': 'Yes'
			},
			{
				'start': 0.5,
				'end': 1.0,
				'word': 'I'
			},
			{
				'start': 1.0,
				'end': 1.5,
				'word': 'win'
			},
			{
				'start': 1.5,
				'end': 2.0,
				'word': 'nineteen'
			},
			{
				'start': 2.0,
				'end': 2.5,
				'word': 'eighty'
			},
			{
				'start': 2.5,
				'end': 3.0,
				'word': 'six'
			},
			{
				'start': 3.0,
				'end': 3.5,
				'word': 'was'
			},
			{
				'start': 3.5,
				'end': 4.0,
				'word': 'it'
			}
		]
		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Yes I win,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0), (1.0, 1.5)]
			},
			{
				'text': '1986 was it.',
				'timestamps': [(1.5, 3.0), (3.0, 3.5), (3.5, 4.0)]
			}
		]

	def test_quotes(self):
		text = {
			'expanded': ['"Hi', 'there",', 'this', 'is', 'a', 'test.'],
			'normalized': ['"Hi', 'there",', 'this', 'is', 'a', 'test.']
		}
		fa_words = [
			{
				'start': 0.0,
				'end': 0.5,
				'word': 'hi'
			},
			{
				'start': 0.5,
				'end': 1.0,
				'word': 'there'
			},
			{
				'start': 1.0,
				'end': 1.5,
				'word': 'this'
			},
			{
				'start': 1.5,
				'end': 2.0,
				'word': 'is'
			},
			{
				'start': 2.0,
				'end': 2.5,
				'word': 'a'
			},
			{
				'start': 2.5,
				'end': 3.0,
				'word': 'test'
			}
		]
		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': '"Hi there",',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_sequence_of_punctuations(self):
		text = {
			'expanded': ['I', 'want', 'to', 'thank', 'President', 'John!".'],
			'normalized': ['I', 'want', 'to', 'thank', 'President', 'John!".']
		}
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'I'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'want'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'to'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'thank'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'President'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'John!".'
			}
		]
		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'I want to thank President John!".',
				'timestamps': [
					(0.0, 0.5), (0.5, 1.0), (1.0, 1.5),
					(1.5, 2.0), (2.0, 2.5), (2.5, 3.0)
				]
			}
		]
