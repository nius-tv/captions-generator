import unittest

from ts_phrases_to_captions import convert
from unittest.mock import patch


@patch('config.MAX_CAPTION_LETTERS', 50)
@patch('config.MIN_CAPTION_LETTERS', 15)
class TestTimestampPhrasesToCaptions(unittest.TestCase):

	def test_captions(self):
		""" Should succeed at converting timestamp-phrases into captions """
		ts_phrases = [
			{
				'text': 'Windows 7 will no longer get security patches.',
				'timestamps': [
					(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0),
					(2.0, 2.5), (2.5, 3.0), (3.0, 3.5), (3.5, 4.0)
				]
			},
			{
				'text': 'Microsoft won\'t release any new security patch.',
				'timestamps': [
					(4.0, 4.5), (4.5, 5.0), (5.0, 5.5), (5.5, 6.0),
					(6.0, 6.5), (6.5, 7.0), (7.0, 7.5)
				]
			}
		]
		assert convert(ts_phrases) == [
			{
				'start': 0.0,
				'end': 4.0,
				'text': 'Windows 7 will no longer get security patches.'
			},
			{
				'start': 4.0,
				'end': 7.5,
				'text': 'Microsoft won\'t release any new security patch.'
			}
		]

	def test_concat_a_big_and_small_phrase(self):
		""" Should concat a big and small phrase """
		ts_phrases = [
			{
				'text': 'Subway services have been suspended,',
				'timestamps': [
					(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0),
					(2.0, 2.5)
				]
			},
			{
				'text': 'roads and houses closed.',
				'timestamps': [
					(2.5, 3.0), (3.0, 3.5), (3.5, 4.0), (4.0, 4.5)
				]
			},
			{
				'text': 'Collectively,',
				'timestamps': [
					(4.5, 5.0)
				]
			},
			{
				'text': 'people are not happy with the unintended regulation you have seen so far.',
				'timestamps': [
					(5.0, 5.5), (5.5, 6.0), (6.0, 6.5), (6.5, 7.0),
					(7.0, 7.5), (7.5, 8.0), (8.0, 8.5), (8.5, 9.0),
					(9.0, 9.5), (9.5, 10.0), (10.0, 10.5), (10.5, 11.0),
					(11.0, 11.5)
				]
			}
		]
		assert convert(ts_phrases) == [
			{
				'start': 0.0,
				'end': 2.0,
				'text': 'Subway services have been'
			},
			{
				'start': 2.0,
				'end': 4.5,
				'text': 'suspended, roads and houses closed.'
			},
			{
				'start': 4.5,
				'end': 8.0,
				'text': 'Collectively, people are not happy with the'
			},
			{
				'start': 8.0,
				'end': 11.5,
				'text': 'unintended regulation you have seen so far.'
			}
		]

	def test_concat_a_small_and_big_phrase(self):
		""" Should concat a small and big phrase """
		ts_phrases = [
			{
				'text': 'Well,',
				'timestamps': [
					(0.0, 0.5)
				]
			},
			{
				'text': 'this is another super long test text with one punctuation.',
				'timestamps': [
					(0.5, 1.0), (1.0, 1.5), (1.5, 2.0), (2.0, 2.5),
					(2.5, 3.0), (3.0, 3.5), (3.5, 4.0), (4.0, 4.5),
					(4.5, 5.0), (5.0, 5.5)
				]
			}
		]
		assert convert(ts_phrases) == [
			{
				'start': 0,
				'end': 3.0,
				'text': 'Well, this is another super long'
			},
			{
				'start': 3.0,
				'end': 5.5,
				'text': 'test text with one punctuation.'
			}
		]

	def test_concat_captions(self):
		""" Should concatenate a short phrase ending with comma """
		ts_phrases = [
			{
				'text': 'Windows 7,',
				'timestamps': [
					(0.0, 0.5), (0.5, 1.0)
				]
			},
			{
				'text': 'will no longer get security patches.',
				'timestamps': [
					(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0),
					(3.0, 3.5), (3.5, 4.0)
				]
			}
		]
		assert convert(ts_phrases) == [
			{
				'start': 0.0,
				'end': 4.0,
				'text': 'Windows 7, will no longer get security patches.'
			}
		]

	def test_concat_few_small_phrases(self):
		""" Should concatenate a few small phrases ending with comma """
		ts_phrases = [
			{
				'text': 'Windows 7,',
				'timestamps': [
					(0.0, 0.5), (0.5, 1.0)
				]
			},
			{
				'text': 'and Vista,',
				'timestamps': [
					(1.0, 1.5), (1.5, 2.0)
				]
			},
			{
				'text': 'will no longer get security patches in the future.',
				'timestamps': [
					(2.0, 2.5), (2.5, 3.0), (3.0, 3.5), (3.5, 4.0),
					(4.0, 4.5), (4.5, 5.0), (5.0, 5.5), (5.5, 6.0),
					(6.5, 7.0)
				]
			}
		]
		assert convert(ts_phrases) == [
			{
				'start': 0,
				'end': 3.5,
				'text': 'Windows 7, and Vista, will no longer'
			},
			{
				'start': 3.5,
				'end': 7.0,
				'text': 'get security patches in the future.'
			}
		]

	def test_concat_on_comma_not_on_period(self):
		""" Should concat on commas but not on periods """
		ts_phrases = [
			{
				'text': 'I like the following days amongst all these day,',
				'timestamps': [
					(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0),
					(2.0, 2.5), (2.5, 3.0), (3.0, 3.5), (3.5, 4.0),
					(4.0, 4.5)
				]
			},
			{
				'text': 'Mondays,',
				'timestamps': [
					(4.5, 5.0)
				]
			},
			{
				'text': 'and Tuesdays.',
				'timestamps': [
					(5.0, 5.5), (5.5, 6.0)
				]
			},
			{
				'text': 'The rest are Nah.',
				'timestamps': [
					(6.0, 6.5), (6.5, 7.0), (7.0, 7.5), (7.5, 8.0)
				]
			}
		]
		assert convert(ts_phrases) == [
			{
				'start': 0.0,
				'end': 3.5,
				'text': 'I like the following days amongst all'
			},
			{
				'start': 3.5,
				'end': 6.0,
				'text': 'these day, Mondays, and Tuesdays.'
			},
			{
				'start': 6.0,
				'end': 8.0,
				'text': 'The rest are Nah.'
			}
		]

	def test_concat_small_phrases(self):
		""" Should concatenate multiple small phrases ending with comma """
		ts_phrases = [
			{
				'text': 'Windows 7,',
				'timestamps': [
					(0.0, 0.5), (0.5, 1.0)
				]
			},
			{
				'text': 'Windows Vista,',
				'timestamps': [
					(1.0, 1.5), (1.5, 2.0)
				]
			},
			{
				'text': 'and Windows 10,',
				'timestamps': [
					(2.0, 2.5), (2.5, 3.0), (3.0, 3.5)
				]
			},
			{
				'text': 'will no longer get security patches.',
				'timestamps': [
					(3.5, 4.0), (4.0, 4.5), (4.5, 5.0), (5.0, 5.5),
					(5.5, 6.0), (6.0, 6.5)
				]
			}
		]
		assert convert(ts_phrases) == [
			{
				'start': 0.0,
				'end': 3.0,
				'text': 'Windows 7, Windows Vista, and Windows'
			},
			{
				'start': 3.0,
				'end': 6.5,
				'text': '10, will no longer get security patches.'
			}
		]

	def test_split_phrase(self):
		""" Should split phrase into multiple captions """
		ts_phrases = [
			{
				'text': 'This is a very long text with one punctuation symbol.',
				'timestamps': [
					(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0),
					(2.0, 2.5), (2.5, 3.0), (3.0, 3.5), (3.5, 4.0),
					(4.0, 4.5), (4.5, 5.0)
				]
			}
		]
		assert convert(ts_phrases) == [
			{
				'start': 0.0,
				'end': 3.0,
				'text': 'This is a very long text'
			},
			{
				'start': 3.0,
				'end': 5.0,
				'text': 'with one punctuation symbol.'
			}
		]

	def test_split_multiple_words(self):
		""" Should split phrase containing words-with-dashes into multiple captions """
		ts_phrases = [
			{
				'text': 'The feud between Apple and big-name iOS developers like Epic Games continues to rage in the courts,',
				'timestamps': [
					(0.0, 0.5), (0.5, 1.0), (1.0, 1.5), (1.5, 2.0),
					(2.0, 2.5), (2.5, 3.0), (3.0, 3.5), (3.5, 4.0),
					(4.0, 4.5), (4.5, 5.0), (5.0, 5.5), (5.5, 6.0),
					(6.0, 6.5), (6.5, 7.0), (7.0, 7.5), (7.5, 8.0)
				]
			},
			{
				'text': 'but the iPhone maker has extended an olive branch to smaller devs.',
				'timestamps': [
					(8.0,  8.5),  (8.5,  9.0),  (9.0,  9.5),  (9.5, 10.0),
					(10.0, 10.5), (10.5, 11.0), (11.0, 11.5), (11.5, 12.0),
					(12.0, 12.5), (12.5, 13.0), (13.0, 13.5), (13.5, 14.0),
				]
			}
		]

		assert convert(ts_phrases) == [
			{
				'start': 0.0,
				'end': 3.0,
				'text': 'The feud between Apple and big-name'
			},
			{
				'start': 3.0,
				'end': 6.5,
				'text': 'iOS developers like Epic Games continues to'
			},
			{
				'start': 6.5,
				'end': 10.5,
				'text': 'rage in the courts, but the iPhone maker'
			},
			{
				'start': 10.5,
				'end': 14.0,
				'text': 'has extended an olive branch to smaller devs.'
			}
		]
