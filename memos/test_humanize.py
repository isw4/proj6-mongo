from memo_func import humanize_date
import arrow

then = arrow.get('2017-11-06')
print(then.isoformat())
now = arrow.utcnow().to('local')
print(now.isoformat())
print(then.date())
print(now.date())