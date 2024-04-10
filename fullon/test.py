from libs import settings
from libs.settings_config import fullon_settings_loader
from libs import exchange, log, cache
from libs.bot_launcher import start, stop
from libs.database_ohlcv import start as startohlcv, stop as stopohlcv, Database as DatabaseOhlcv
from libs.database import start as startdb, stop as stopdb, Database
from run import rpcdaemon_manager as rpc
from run.process_manager import ProcessManager
from run.crawler_manager import CrawlerManager
from libs.crawler.llm_engines.openai.engine import Engine
import pytest

settings.LOG_LEVEL = "logging.INFO"


startohlcv()
startdb()

crawler = CrawlerManager()

#crawler._load_module_for_site(site='twitter')
crawler._fetch_posts(site='twitter', llm_scores=True)

stopdb()
stopohlcv()



#engine = Engine()
#print(engine._analyze_image(file='1767873893115576609.jpg'))

#post = 'I think BTC is ok, but watch out looks oversold'

#engine.score_post(post)

