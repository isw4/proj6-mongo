from memo_func import humanize_date
import arrow

servertime = arrow.utcnow().to('local')

def test_today():
	todaydate = servertime.isoformat().split('T')[0]
	assert humanize_date(todaydate) == "Today"

def test_tomorrow():
	tmrdate = servertime.shift(days=+1).isoformat().split('T')[0]
	assert humanize_date(tmrdate) == "Tomorrow"

def test_in2days():
	intwo = servertime.shift(days=+2).isoformat().split('T')[0]
	assert humanize_date(intwo) == "in 2 days"

def test_1dayago():
	oneago = servertime.shift(days=-1).isoformat().split('T')[0]
	assert humanize_date(oneago) == "a day ago"
