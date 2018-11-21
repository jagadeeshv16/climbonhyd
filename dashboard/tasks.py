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
                if EventData.objects.filter(created_id=context['id']).exists():
                    ev_obj = EventData.objects.filter(created_id=context['id']).first()
                    if not ev_obj.updated_date.replace(tzinfo=timezone.utc)< up_date_date.replace(tzinfo=timezone.utc):
                        continue
                else:
                    ev_obj = EventData()
                date_feild = context.get('local_date')
                date_feild = datetime.datetime.strptime(date_feild, "%Y-%m-%d")
                time_feild = context.get('local_time')
                time_feild = datetime.datetime.strptime(time_feild, '%H:%M').time()
                ev_obj.created = context.get('created')
                ev_obj.name = context.get('name')
                ev_obj.created_id=context.get('id')
                ev_obj.event_datetime=datetime.datetime.combine(date_feild,time_feild)
                ev_obj.status = context.get('status')
                ev_obj.updated=context.get('updated')
                ev_obj.updated_date=up_date
                ev_obj.venue_name=context.get('venue', {}).get('name', "")
                ev_obj.venue_address=context.get('venue', {}).get('address_1',"")
                ev_obj.venue_city=context.get('venue', {}).get('city',"")
                ev_obj.venue_country=context.get('venue', {}).get('country',"")
                ev_obj.link=context.get('link')
                ev_obj.Contact_Us=context.get('how_to_find_us')
                ev_obj.description = context.get('description')
                ev_obj.save()
            print("data created sucessfully")
        else:
            print("your url page is not loaded")


            