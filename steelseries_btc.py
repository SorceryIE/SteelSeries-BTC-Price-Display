from time import sleep
import requests
import os
import json

game = 'BITCOIN'
event = 'BITCOIN'
name = 'BTC Price Display'
developer = 'Sorcery Ltd'
last_btc_price = 0
counter = 0


def init():
	global sse_address
	core_props_path = f"{os.getenv('PROGRAMDATA')}\\SteelSeries\\SteelSeries Engine 3\\coreProps.json"
	sse_address = json.load(open(core_props_path))["address"]
	# now register the app
	metadata = {"game": game, "game_display_name": name, "developer": developer}
	requests.post(f"http://{sse_address}/game_metadata", json=metadata)
	# now add some handlers for new event
	screen_handler = {
		"device-type": "screened",
		"zone": "one",
		"mode": "screen",
		"datas": [
			{
				"has-text": True,
				"icon-id": 4,
				'bold': True,
			}
		]
	}
	handlers = {"game": game, "event": event, "icon_id": 4, "handlers": [screen_handler]}
	requests.post(f"http://{sse_address}/bind_game_event", json=handlers)


def get_btc_price():
	r = requests.get('https://blockchain.info/ticker').json()
	return r['USD']['last']


def send_event():
	global last_btc_price, counter
	btc_price = last_btc_price
	counter = counter % 10
	if counter == 0:
		btc_price = get_btc_price()
		last_btc_price = btc_price
	event_data = {"game": game, "event": event, "data": {"value": btc_price}}
	r = requests.post(f"http://{sse_address}/game_event", json=event_data)
	counter += 1


init()
while True:
	send_event()
	sleep(1)
