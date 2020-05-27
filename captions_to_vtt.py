import config
import datetime


def build_vtt_caption(caption_a, caption_b=None):
	lines = [
		caption_a['text']
	]

	if caption_b is None:
		end = caption_a['end']
	else:
		end = caption_b['end']
		lines.append(caption_b['text'])

	header = '{} --> {} {}'.format(caption_a['start'],
								   end,
								   config.CAPTIONS_STYLE)
	lines.insert(0, header)
	lines.append('')

	return lines


def convert(captions, duration):
	captions = format_captions(captions, duration)
	count = 0
	lines = ['WEBVTT', '']
	prev_caption = None

	for caption in captions:
		if caption['text'][-1] in config.NEW_LINE_TOKENS:
			count = 1

		if count == 0:
			prev_caption = caption
			count = 1
			continue

		count = 0
		if prev_caption is None:
			vtt_caption = build_vtt_caption(caption)
		else:
			vtt_caption = build_vtt_caption(prev_caption, caption)
			prev_caption = None
		lines.extend(vtt_caption)

	return '\n'.join(lines)


def format_captions(captions, duration):
	formatted = captions.copy()

	for i, caption in enumerate(formatted):
		# Start time
		caption['start'] = format_time(caption['start'])
		# End time
		end = caption['end']
		if i + 1 == len(formatted):
			end += config.END_DURATION_OFFSET
		if end > duration:
			end = duration
		caption['end'] = format_time(end)
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
