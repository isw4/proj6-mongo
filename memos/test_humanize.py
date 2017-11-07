from memo_func import humanize_date
import arrow

date = '2017-11-08'
#then = arrow.get('2017-11-07')
parts = date.split('T')[0].split('-')
then = arrow.utcnow().to('local')
then = then.replace(year=int(parts[0]), month=int(parts[1]), day=int(parts[2]))
print(then.isoformat())

now = arrow.utcnow().to('local')
print(now.isoformat())

print(then.date())
print(now.date())

print(humanize_date(date))