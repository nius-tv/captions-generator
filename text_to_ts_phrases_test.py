import unittest

from text_to_ts_phrases import TextToTimestampPhrases
from unittest.mock import patch


class TestTextToTimestampPhrases(unittest.TestCase):

	text_to_phrases = TextToTimestampPhrases()

	def test_hypens(self):
		""" Should timestamp words with hyphens """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': '11'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'inch'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'tall'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'car'
			}
		]
		text = '11-inch-tall car.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': '11-inch-tall car.',
				'timestamps': [(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0)]
			}
		]

	@patch('config.MAX_SKIP_TOKENS', 1)
	def test_max_skips(self):
		""" Should fail on max skips """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'th_re'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'th_s'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': '_s'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': '_'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		with self.assertRaises(AssertionError):
			self.text_to_phrases.convert(text, fa_words)

	def test_no_time_words_end(self):
		""" Should timestamp words-with-no-time ending the captions """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_no_time_words_start(self):
		""" Should timestamp words-with-no-time starting the captions """
		fa_words = [
			{
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_phrase_distanced_no_time_words_end(self):
		""" Should timestamp words-with-no-time with distance between phrases (ending) """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'word': 'there'
			},
			{
				'end': 5.5,
				'start': 5.0,
				'word': 'this'
			},
			{
				'end': 6.0,
				'start': 5.5,
				'word': 'is'
			},
			{
				'end': 6.5,
				'start': 6.0,
				'word': 'a'
			},
			{
				'end': 7.0,
				'start': 6.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(5.0, 5.5), (5.5, 6.0), (6.0, 6.5), (6.5, 7.0)]
			}
		]

	def test_phrase_distanced_no_time_words_start(self):
		""" Should timestamp words-with-no-time with distance between phrases (starting) """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'word': 'this'
			},
			{
				'end': 5.0,
				'start': 4.5,
				'word': 'is'
			},
			{
				'end': 5.5,
				'start': 5.0,
				'word': 'a'
			},
			{
				'end': 6.0,
				'start': 5.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(4.0, 4.5), (4.5, 5.0), (5.0, 5.5), (5.5, 6.0)]
			}
		]

	def test_phrase_no_time_words_end(self):
		""" Should timestamp words-with-no-time ending a phrase """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_phrase_no_time_words_middle(self):
		""" Should timestamp words-with-no-time in middle of phrase """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_phrase_no_time_words_start(self):
		""" Should timestamp words-with-no-time starting a phrase """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_phrase_several_no_time_words_end_start(self):
		""" Should timestamp several words-with-no-time ending and starting a phrase """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'word': 'there'
			},
			{
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_phrase_several_no_time_words_middle(self):
		""" Should timestamp several words-with-no-time at middle of a phrase """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'word': 'is'
			},
			{
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_phrase_several_no_time_words_middle_end(self):
		""" Should timestamp several words-with-no-time at middle and end of a phrase """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'word': 'a'
			},
			{
				'word': 'test'
			},
			{
				'end': 3.5,
				'start': 3.0,
				'word': 'Yes'
			}
		]
		text = 'Hi there, this is a test. Yes.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			},
			{
				'text': 'Yes.',
				'timestamps': [(3.0, 3.5)]
			}
		]

	def test_phrase_several_no_time_words_start_middle(self):
		""" Should timestamp several words-with-no-time at start and middle of a phrase """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'word': 'this'
			},
			{
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_plus_sign(self):
		""" Should timestamp words with "plus signs" """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'Wieden'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'Kennedy'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'tall'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'car'
			}
		]
		text = 'Wieden+Kennedy tall car.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Wieden+Kennedy tall car.',
				'timestamps': [(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0)]
			}
		]

	@patch('config.CHAR_DICT', {'A': 'Aih', 'B': 'bEE', 'C': 'CeE'})
	def test_replace_chars(self):
		""" Should replace characters """
		fa_words = [
			{
				'end': 0.5,
				'start': 0.0,
				'word': 'Aih'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'bEE'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'CeE'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'news'
			}
		]
		text = 'Aih-bEE-CeE news.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'ABC news.',
				'timestamps': [(0.0, 1.5), (1.5, 2.0)]
			}
		]

	def test_replace_comma_quote(self):
		""" Should replace phrases ending with comma and quote """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = '"Hi there," this is a test.'

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

	def test_replace_period_quote(self):
		""" Should replace phrases ending with period and quote """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = '"Hi there." This is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': '"Hi there".',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'This is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	@patch('config.CHAR_DICT', {'A': 'Aih', 'B': 'bEE', 'C': 'CeE'})
	def test_replace_several_chars(self):
		""" Should replace several characters """
		fa_words = [
			{
				'end': 0.5,
				'start': 0.0,
				'word': 'Test'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'bEE'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'CeE'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'news'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'test'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'Aih'
			},
			{
				'end': 3.5,
				'start': 3.0,
				'word': 'bEE'
			},
			{
				'end': 4.0,
				'start': 3.5,
				'word': 'CeE'
			}
		]
		text = 'Test bEE-CeE news test Aih-bEE-CeE.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Test BC news test ABC.',
				'timestamps': [(0.0, 0.5), (0.5, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 4.0)]
			}
		]

	@patch('config.REPLACE_DICT', {'pokemon': 'pokeemonn', 'mo_re': 'more'})
	def test_replace_several_tokens(self):
		""" Should replace several tokens """
		fa_words = [
			{
				'end': 0.5,
				'start': 0.0,
				'word': 'pokeemonn'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'and'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'more'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'pokeemonn'
			}
		]
		text = 'pokeemonn and more pokeemonn.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'pokemon and mo_re pokemon.',
				'timestamps': [(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0)]
			}
		]

	@patch('config.REPLACE_DICT', {'SUVs': 'EsS-EiuU-VeEs'})
	def test_replace_tokens(self):
		""" Should replace tokens """
		fa_words = [
			{
				'end': 0.5,
				'start': 0.0,
				'word': 'I'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'like'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'Tesla\'s'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'EsS'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'EiuU'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'VeEs'
			}
		]
		text = 'I like Tesla\'s EsS-EiuU-VeEs.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'I like Tesla\'s SUVs.',
				'timestamps': [
					(0.0, 0.5), (0.5, 1.0), (1.0, 1.25), (1.25, 1.5),
					(1.5, 3.0)
				]
			}
		]

	def test_several_no_time_words_end(self):
		""" Should timestamp several words-with-no-time ending the captions """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'word': 'a'
			},
			{
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_several_no_time_words_start(self):
		""" Should timestamp several words-with-no-time starting the captions """
		fa_words = [
			{
				'word': 'hi'
			},
			{
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_sequence_of_punctuations(self):
		""" Should succeed at processing a sequence of punctuations """
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
		text = 'I want to thank President John!".'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'I want to thank President John!".',
				'timestamps': [
					(0.0, 0.5), (0.5, 1.0), (1.0, 1.5),
					(1.5, 2.0), (2.0, 2.5), (2.5, 3.0)
				]
			}
		]

	def test_split_words(self):
		""" Should split words into tokens """
		fa_words = [
			{
				'end': 0.5,
				'start': 0.0,
				'word': 'He\'s'
			},
			{
				'end': 2.0,
				'start': 0.5,
				'word': 'sleepy'
			}
		]
		text = 'He\'s sleepy.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'He\'s sleepy.',
				'timestamps': [(0.0, 0.25), (0.25, 0.5), (0.5, 2)]
			}
		]

	def test_timestap_phrases(self):
		""" Should timestamp phrases """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = 'Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_timestap_phrases_with_space_end(self):
		""" Should timestamp phrases that end with an extra spacing """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = 'Hi there,  this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]

	def test_timestap_phrases_with_space_start(self):
		""" Should timestamp phrases that start with an extra spacing """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'hi'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'there'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'this'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'is'
			},
			{
				'end': 2.5,
				'start': 2.0,
				'word': 'a'
			},
			{
				'end': 3.0,
				'start': 2.5,
				'word': 'test'
			}
		]
		text = ' Hi there, this is a test.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'Hi there,',
				'timestamps': [(0.0, 0.5), (0.5, 1.0)]
			},
			{
				'text': 'this is a test.',
				'timestamps': [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0)]
			}
		]	

	def test_tokens_with_periods(self):
		""" Should split tokens with periods """
		fa_words = [
			{
				'end': 0.5,
				'start': 0,
				'word': 'I'
			},
			{
				'end': 1.0,
				'start': 0.5,
				'word': 'O'
			},
			{
				'end': 1.5,
				'start': 1.0,
				'word': 'S'
			},
			{
				'end': 2.0,
				'start': 1.5,
				'word': 'phone'
			}
		]
		text = 'I. O. S. phone.'

		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': 'I. O. S. phone.',
				'timestamps': [(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0)]
			}
		]
