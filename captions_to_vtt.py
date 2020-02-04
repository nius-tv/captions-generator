import config
import datetime


def convert(captions):
	lines = ['WEBVTT', '']
	captions = format_captions(captions)

	for caption in captions:
		header = '{} --> {} {}'.format(caption['start'],
									   caption['end'],
									   config.CAPTIONS_STYLE)
		lines.append(header)
		lines.append(caption['text'])
		lines.append('')

	return '\n'.join(lines)


def format_captions(captions):
	formatted = captions.copy()

	for i, caption in enumerate(formatted):
		# Start time
		caption['start'] = format_time(caption['start'])
		# End time
		if i + 1 == len(formatted):
			caption['end'] += config.END_DURATION_OFFSET
		caption['end'] = format_time(caption['end'])
		# The following condition allow us to use the "start" of current
		# caption as "end" of prev one, preventing his prevents "time gaps".
		if i > 0:
			formatted[i - 1]['end'] = caption['start']

	return formatted


def format_time(time):
	if time > 0:
		time = str(datetime.timedelta(seconds=time))
		if '.' in time:
			time = time[:-3] # 0:00:03.840000 to 0:00:03.840, required by WebVTT.
		else:
			time = '{}.000'.format(time)
	else:
		time = '0:00:00.000'

	return time
