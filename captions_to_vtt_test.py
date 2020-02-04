import unittest

from captions_to_vtt import convert
from unittest.mock import patch


class TestCaptionsToVTT(unittest.TestCase):

	@patch('config.CAPTIONS_STYLE', 'align:center line:-9 position:50% size:80%')
	@patch('config.END_DURATION_OFFSET', 5)
	def test(self):
		""" Should convert captions to WebVTT """
		captions = [
			{'end': 1.0, 'start': 0.0, 'text': 'Hi there,'},
			{'end': 3.0, 'start': 1.0, 'text': 'this is a test.'},
			{'end': 4.0, 'start': 3.0, 'text': 'Yes it is.'}
		]
		vtt = ('WEBVTT\n'
				'\n'
				'0:00:00.000 --> 0:00:03.000 align:center line:-9 position:50% size:80%\n'
				'Hi there,\n'
				'this is a test.\n'
				'\n'
				'0:00:03.000 --> 0:00:07.000 align:center line:-9 position:50% size:80%\n'
				'Yes it is.\n')

		assert convert(captions, duration=7) == vtt
