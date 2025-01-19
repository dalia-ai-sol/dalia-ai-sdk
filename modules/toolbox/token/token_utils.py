import requests
import os
from datetime import timedelta

def get_token_pricing_history(token_address, start_time=1735968000, end_time=1736054400, interval_type='1m'):
	"""
	https://docs.birdeye.so/docs/price-history#response
	Fetches token pricing history from the API, splitting requests if the time range exceeds 1000 minutes.
	"""

	address_type = "token"
	api_key = os.environ.get("BIRDEYE_API_KEY")

	# Calculate maximum allowed interval
	max_minutes = 1000
	interval_seconds = 60  # Assuming '1m' interval corresponds to 60 seconds
	max_interval = max_minutes * interval_seconds

	pricing_time, pricing_data = [], []

	# Split the time range if necessary
	current_start = start_time
	while current_start < end_time:
		current_end = min(current_start + max_interval, end_time)

		url = (
			f"https://public-api.birdeye.so/defi/history_price"
			f"?address={token_address}&address_type={address_type}"
			f"&type={interval_type}&time_from={current_start}&time_to={current_end}"
		)
		headers = {"accept": "application/json", "X-API-KEY": api_key}
		response = requests.get(url, headers=headers)

		if response.status_code == 200:
			response_data = response.json()
			if response_data.get("success"):
				historical_data = response_data.get("data", {}).get("items", [])
				if historical_data:
					for entry in historical_data:
						pricing_time.append(entry.get('unixTime'))
						pricing_data.append(entry.get('value'))

		current_start = current_end

	return pricing_time, pricing_data

def get_ticker_address(token_ticker, chain = 'solana', sort_by = 'liquidity'):
	"""
	https://docs.birdeye.so/reference/get_defi-v3-search
	"""
	api_key = os.environ.get("BIRDEYE_API_KEY")
	url = f"https://public-api.birdeye.so/defi/v3/search?keyword={token_ticker}&chain={chain}&target=token&sort_by={sort_by}"
	headers = {"accept": "application/json", "X-API-KEY": api_key}
	response = requests.get(url, headers=headers)

	token_address = None
	if response.status_code == 200:
		response_data = response.json()
		if response_data.get("success"):
			if len(response_data['data']['items'][0]['result']):
				try:
					coin = [coin for coin in response_data['data']['items'][0]['result'] if coin['symbol'].lower() == token_ticker.lower()][0]
					token_address = coin.get('address', None)
				except:
					token_address = None

	return token_address

def get_token_trade_data(token, is_ticker = False):
	"""
	https://docs.birdeye.so/reference/get_defi-v3-token-trade-data-single
	"""
	if is_ticker:
		token = get_ticker_address(token)

	api_key = os.environ.get("BIRDEYE_API_KEY")
	url = f"https://public-api.birdeye.so/defi/v3/token/trade-data/single?address={token}"
	headers = {"accept": "application/json", "X-API-KEY": api_key}

	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		response_data = response.json()
		if response_data.get("success"):
			return response_data['data']

	return {}

def get_token_metadata(token, is_ticker = False):
	"""
	https://docs.birdeye.so/reference/get_defi-v3-token-meta-data-single
	"""
	if is_ticker:
		token = get_ticker_address(token)

	api_key = os.environ.get("BIRDEYE_API_KEY")
	url = f"https://public-api.birdeye.so/defi/v3/token/meta-data/multiple?list_address={token}"
	headers = {"accept": "application/json", "X-API-KEY": api_key}

	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		response_data = response.json()
		if response_data.get("success"):
			return response_data['data']

	return {}

def get_token_creation_info(token, is_ticker = False):
	"""
	https://docs.birdeye.so/reference/get_defi-token-creation-info
	"""
	if is_ticker:
		token = get_ticker_address(token)

	api_key = os.environ.get("BIRDEYE_API_KEY")
	url = f"https://public-api.birdeye.so/defi/token_creation_info?address={token}"
	headers = {"accept": "application/json", "X-API-KEY": api_key}

	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		response_data = response.json()
		if response_data.get("success"):
			return response_data['data']

	return {}

def get_top_token_holders(token, is_ticker = False):
	"""
	https://docs.birdeye.so/reference/get_defi-v3-token-holder
	"""
	if is_ticker:
		token = get_ticker_address(token)

	api_key = os.environ.get("BIRDEYE_API_KEY")
	url = f"https://public-api.birdeye.so/defi/v3/token/holder?address={token}&offset=0&limit=100"
	headers = {"accept": "application/json", "X-API-KEY": api_key}

	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		response_data = response.json()
		if response_data.get("success"):
			return response_data['data']

	return {}

def get_top_token_traders(token, is_ticker = False):
	"""
	https://docs.birdeye.so/reference/get_defi-v2-tokens-top-traders
	"""
	if is_ticker:
		token = get_ticker_address(token)

	time_frame = '24h' # 30m, 1h, 2h, 4h, 6h, 12h, 24h
	sort_by = 'volume' # volume, trade
	api_key = os.environ.get("BIRDEYE_API_KEY")
	url = f"https://public-api.birdeye.so/defi/v2/tokens/top_traders?address={token}&time_frame={time_frame}&sort_type=desc&sort_by={sort_by}&offset=0&limit=10"
	headers = {"accept": "application/json", "X-API-KEY": api_key}

	response = requests.get(url, headers=headers)
	if response.status_code == 200:
		response_data = response.json()
		if response_data.get("success"):
			return response_data['data']

	return {}





