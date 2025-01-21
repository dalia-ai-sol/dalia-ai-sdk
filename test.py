from dotenv import load_dotenv

load_dotenv()

from modules.toolbox.news.news import get_latest_news


x = get_latest_news("Donal Trump")
print(x)