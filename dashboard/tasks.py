from celery.task import task 
from celery import shared_task
from celery import Celery
import datetime
from dashboard.views import *
import os



@task
def event_data():
    groupname = settings.GROUP_NAME
    key = settings.API_KEY
    url = 'https://api.meetup.com/'+groupname+'/events?&sign=true&photo-host=public&page=20&key='+key
    context = requests.get(url)
    if context.status_code == 200:
        events= context.json()
        for context in events:
                up_date = context.get('updated')
                up_date = int(str(up_date)[:10])
                up_date = time.strftime("%Y-%m-%d %H:%M", time.localtime(up_date))
                up_date_date = datetime.datetime.strptime(up_date, '%Y-%m-%d %H:%M')
                if EventData.objects.filter(created_id=context['id']).exists() or EventData.objects.filter(updated_date=up_date_date).exists():
                    print("the data is already saved")
                else:
                    date_feild = context.get('local_date')
                    date_feild = datetime.datetime.strptime(date_feild, "%Y-%m-%d")
                    time_feild = context.get('local_time')
                    time_feild = datetime.datetime.strptime(time_feild, '%H:%M').time()
                    event = EventData.objects.update_or_create(
                       created=context.get('created'),
                       name=context.get('name'),
                       created_id=context.get('id'),
                       event_datetime=datetime.datetime.combine(date_feild,time_feild),
                       status = context.get('status'),
                       updated=context.get('updated'),
                       updated_date=up_date,
                       venue_name=context.get('venue', {}).get('name', ""),
                       venue_address=context.get('venue', {}).get('address_1',""),
                       venue_city=context.get('venue', {}).get('city',""),
                       venue_country=context.get('venue', {}).get('country',""),
                       link=context.get('link'),
                       Contact_Us=context.get('how_to_find_us'))
                print("data created sucessfully")
    else:
        print("your url page is not loaded")


            