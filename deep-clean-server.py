from datetime import datetime
import time
import signal

import camera
from tensorflow import Session as tf_session
import label_image
import numpy

import asyncio
from aiohttp import web
from aiohttp.web import Response
from aiohttp_sse import sse_response
import json

MODEL_FILE = 'deep-clean-graph.pb'
LABEL_FILE = 'deep-clean-labels.txt'

result = {
	'clean': 0,
	'messy': 0,
	'busy': 0
}

loop = asyncio.get_event_loop()
app = web.Application(loop=loop)

def take_and_label_picture():
	# ts = time.time()
	# timeStamp = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M')
	image_file = 'static/lab.jpg'
	print('Taking picture and saving to '+image_file)
	camera.take_picture(image_file, True)

	graph = label_image.load_graph(MODEL_FILE)
	t = label_image.read_tensor_from_image_file(image_file)

	input_operation = graph.get_operation_by_name('import/Placeholder')
	output_operation = graph.get_operation_by_name('import/final_result')

	with tf_session(graph=graph) as sess:
		results = sess.run(output_operation.outputs[0], {
			input_operation.outputs[0]: t
		})
	results = numpy.squeeze(results)

	labels = label_image.load_labels(LABEL_FILE)
	for i, label in enumerate(labels):
		result[label] = float(results[i])

	print(result)
	message(result)

def message(data):
	for queue in app['channels']:
		payload = json.dumps(data)
		queue.put(payload)

async def subscribe(request):
	async with sse_response(request) as response:
		app = request.app
		queue = asyncio.Queue()
		print('Someone joined.')
		app['channels'].add(queue)
		try:
			while not response.task.done():
				payload = await queue.get()
				await response.send(payload)
				queue.task_done()
		finally:
			app['channels'].remove(queue)
			print('Someone left.')
	return response

def take_picture(request):
	take_and_label_picture()
	return Response(text='done')

def get_result(request):
	print(result)
	return Response(
		text=json.dumps(dict(result)),
		content_type='application/json'
	)


def signal_handler(signal, frame):
	take_and_label_picture()

def main():
	signal.signal(signal.SIGALRM, signal_handler)
	signal.alarm(5*60)

	app['channels'] = set()

	app.router.add_route('GET', '/subscribe', subscribe)
	app.router.add_route('GET', '/take-picture', take_picture)
	app.router.add_route('GET', '/result', get_result)
	app.router.add_static('/', './static/')

	take_and_label_picture()

	web.run_app(app, port=5000)

main()
