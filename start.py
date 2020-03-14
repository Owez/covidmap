from apscheduler.schedulers.blocking import BlockingScheduler
from covidmap import launch_flask

scheduler = BlockingScheduler()
scheduler.add_job(launch_flask, 'interval', hours=3)
scheduler.start()