import os
import json
import arrow
import requests

def get_latest_news(query) -> json:
	"""
	Based on the search topics, grabs the most recent NEWS articles.
	"""
	base_url = "https://gnews.io/api/v4/search"
	api_key = os.getenv('GNEWS_API_KEY')
	end_time = arrow.utcnow()
	start_time = end_time.shift(hours=-48)
	news_articles = []
	params = {
		'q': query,
		'lang': "en",
		'max': 5,
		'in' : 'title,description,content',
		'sortby': 'publishedAt',
		'apikey': api_key,
		'expand' : 'content'
	}
	response = requests.get(base_url, params=params)
	response.raise_for_status()
	news_data = response.json()
	if 'articles' in news_data:
		articles = news_data['articles']
		for _, article in enumerate(articles, start=1):
			article_obj = {}
			article_obj["api_source"] = "gnews"
			article_obj["search_query"] = query
			article_obj["title"] = article.get("title", "")
			article_obj["description"] = article.get("description", "")
			article_obj["url"] = article.get("url", "")
			article_obj["content"] = article.get("content", "")[0:10000]
			article_obj["image"] = article.get("image", "")
			article_obj["publication_date"] = article.get("publishedAt", "")
			article_obj["source_name"] = article["source"]["name"]
			article_obj["source_url"] = article["source"]["url"]
			article_obj["collection_time"] = arrow.utcnow().format("YYYY-MM-DDTHH:mm:ss")
			news_articles.append(article_obj)
	return news_articles