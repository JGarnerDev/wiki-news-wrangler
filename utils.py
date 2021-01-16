from datetime import datetime

now = datetime.now()
timestamp = datetime.timestamp(now)

t_str = str(datetime.fromtimestamp(timestamp))[:-10]
