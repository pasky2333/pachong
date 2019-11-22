# Redis名
REDIS_KEY = 'proxy'

# Redis数据库地址
REDIS_HOST = '127.0.0.1'

# Redis端口
REDIS_PORT = 6379

#Redis密码，如无填None
REDIS_PASSWORD = None

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 0
INITIAL_SCORE = 10

# 合法状态码
VALID_STATUS_CODES = [200, 302]

# 代理池数量上限
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 20

# 获取周期
GETTER_CYCLE = 300

# 测试api，建议抓哪个网站测哪个
TEST_API = 'https://weixin.sogou.com/weixin'

# API配置
API_HOST = '127.0.0.1'
API_PORT = 5556

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大测试批量
BATCH_TEST_SIZE = 20

# 抓取网页页数
PAGE_COUNT = 4
