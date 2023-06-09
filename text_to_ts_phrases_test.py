import unittest

from text_to_ts_phrases import TextToTimestampPhrases


class TestTextToTimestampPhrases(unittest.TestCase):

	text_to_phrases = TextToTimestampPhrases()

	def test_hypens(self):
		""" Should timestamp words with hyphens """
		text = {
			'expanded':   ['11-inch-tall', 'car.'],
			'normalized': ['11-inch-tall', 'car.']
		}
		fa_words = [
			{
				'start': 0.0,
				'end': 0.5,
				'word': '11'
			},
			{
				'start': 0.5,
				'end': 1.0,
				'word': 'inch'
			},
			{
				'start': 1.0,
				'end': 1.5,
				'word': 'tall'
			},
			{
				'start': 1.5,
				'end': 2.0,
				'word': 'car'
			}
		]
		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': '11-inch-tall car.',
				'timestamps': [(0.0, 1.5), (1.5, 2.0)]
			}
		]

	def test_quotes(self):
		""" Should timestamp phrases with quotes """
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

	def test_remove_new_lines(self):
		""" Should remove new lines """
		text = {
			'expanded': ['\nI', 'want', 'to', 'thank', 'President', 'John!".'],
			'normalized': ['\nI', 'want', 'to', 'thank', 'President', 'John!".']
		}
		fa_words = [
			{
				'start': 0.0,
				'end': 0.5,
				'word': 'I'
			},
			{
				'start': 0.5,
				'end': 1.0,
				'word': 'want'
			},
			{
				'start': 1.0,
				'end': 1.5,
				'word': 'to'
			},
			{
				'start': 1.5,
				'end': 2.0,
				'word': 'thank'
			},
			{
				'start': 2.0,
				'end': 2.5,
				'word': 'President'
			},
			{
				'start': 2.5,
				'end': 3.0,
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

	def test_replace_chars(self):
		""" Should replace characters """
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

	def test_sequence_of_punctuations(self):
		""" Should maintain sequence of punctuations """
		text = {
			'expanded': ['I', 'want', 'to', 'thank', 'President', 'John!".'],
			'normalized': ['I', 'want', 'to', 'thank', 'President', 'John!".']
		}
		fa_words = [
			{
				'start': 0.0,
				'end': 0.5,
				'word': 'I'
			},
			{
				'start': 0.5,
				'end': 1.0,
				'word': 'want'
			},
			{
				'start': 1.0,
				'end': 1.5,
				'word': 'to'
			},
			{
				'start': 1.5,
				'end': 2.0,
				'word': 'thank'
			},
			{
				'start': 2.0,
				'end': 2.5,
				'word': 'President'
			},
			{
				'start': 2.5,
				'end': 3.0,
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

	def test_split_phrases(self):
		""" Should split phrases """
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

	def test_split_years(self):
		""" Should split years """
		text = {
			'expanded': [['twenty', 'twenty-four']],
			'normalized': ['2024']
		}
		fa_words = [
			{
				'start': 0.0,
				'end': 0.5,
				'word': 'twenty'
			},
			{
				'start': 0.5,
				'end': 1.0,
				'word': 'twenty'
			},
			{
				'start': 1.0,
				'end': 1.5,
				'word': 'four'
			}
		]
		assert self.text_to_phrases.convert(text, fa_words) == [
			{
				'text': '2024',
				'timestamps': [(0.0, 1.5)]
			}
		]
