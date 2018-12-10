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
        event = EventData.objects.filter(status="upcoming")
        for i in event:
            if i.event_datetime.replace(tzinfo=timezone.utc)<datetime.datetime.today().replace(tzinfo=timezone.utc):
                EventData.objects.filter(name=i.name).update(status="past")
    else:
        print("your url page is not loaded")


@task
def event_photo():
        groupname = settings.GROUP_NAME
        key = settings.API_KEY
        url = 'https://api.meetup.com/'+groupname+'/photo_albums?&sign=true&photo-host=public&key='+key
        context = requests.get(url)
        if context.status_code == 200:
            events= context.json()
            for context in events:
                event_id = context.get('event', {}).get('id', "")
                photo_id = context.get('id')
                if EventPhoto.objects.filter(photo_id=photo_id).exists():
                    print("data created")
                else:
                    if EventData.objects.filter(created_id=event_id).exists():
                        ph_data = EventPhoto()
                        ph_data.event = EventData.objects.get(created_id=event_id)
                        data = context.get('photo_sample')
                        if data:
                            for i in data:
                                EventPhoto.objects.create(
                                event = EventData.objects.get(created_id=event_id),
                                highres_link = i['highres_link'],
                                photo_link = i['photo_link'],
                                thumb_link = i['thumb_link'],
                                photo_id = context.get('id'))
                        else:
                            pass
                    print("data created sucessfully")
        else:
            print("your url is not found")
  
        
@task()
def Insta_photos():
    model = Photos
    form = PhotosForm
    template_name = 'eventdata.html'
    display = Display(visible=0, size=(1366, 768))
    display.start()
    driver = webdriver.Firefox()
    driver.get("https://www.instagram.com/climbon_hyderabad/")
    time.sleep(2)
    url = []
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    shortcode = driver.find_elements_by_class_name("FyNDV")
    time.sleep(2)
    for i in shortcode:
        ele = i.find_elements_by_css_selector('a')
        for j in ele:
            lis = j.get_attribute('href')
            url.append(lis)
    match = False
    while(match==False):
        last = lenOfPage
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        time.sleep(2)
        if last != lenOfPage:
            shortcode = driver.find_elements_by_class_name("FyNDV")
            time.sleep(2)
            for i in shortcode:
                ele = i.find_elements_by_css_selector('a')
                for j in ele:
                    lis = j.get_attribute('href')
                    url.append(lis)
        else:
            match = True
                
    total = list(set(url))
    main = []
    for l in total:
        team = "https://api.instagram.com/oembed/?url="+l
        main.append(team)
    display.stop()

    for i in main:
        url = requests.get(i)
        if url.status_code == 200:
            events = url.json()
            k = i.strip('/')
            code = k.rsplit('/',1)[1]
            title = events.get('title').encode('unicode-escape')
            html = events.get('html').encode('unicode-escape')
            if Photos.objects.filter(shortcode=code).exists():
                print("data already exists")
            else:
                event_photos, created = Photos.objects.get_or_create(
                    shortcode=code,
                    title=title, html=html,
                    thumbnail_url=events.get('thumbnail_url'))
                print("data created")
        
