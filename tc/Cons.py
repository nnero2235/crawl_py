
#same to logging LEVEL  value
LOG_DEBUG = 10
LOG_INFO = 20
LOG_WARNING = 30
LOG_ERROR = 40
LOG_CRITIAL = 50


USER_AGENTS = [
"Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60",
"Opera/8.0 (Windows NT 5.1; U; en)",
"Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50",
"Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50"
]

HTTP_HEADERS = {
"ua" : "User_Agent",
"refer":"Refer",
"host":"Host"
}

REDIS_TASK_KEYS = "task_keys"
REDIS_URL_KEYS = "url_keys"

REDIS_TASK_COMLETE = "is_complete"
REDIS_TASK_QUEUE_SIZE = "task_queue_size"
REDIS_TASK_FETCHED_URLS = "fetched_urls"
REDIS_TASK_RE_FETCH = "re_fetch"

#task queue default time
TASK_QUEUE_WAIT_TIME = 10
