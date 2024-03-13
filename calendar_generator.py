
from datetime import datetime,timedelta


start_date_str = "2024-03-11"
event_period_minutes = 5
your_name = "John Doe"
your_email = "johndoe@gmail.com"
reminder_format = "{} in 30 minutes"
total_rozay = 30 # or 29
output_file = "ramzan_calendar.ics"
list_times = '04:37,04:35,04:32,04:30,04:27,04:25,04:22,04:19,04:17,04:14,04:12,04:09,04:06,04:03,04:01,03:58,03:55,03:52,03:49,03:46,04:44,04:41,04:38,04:35,04:32,04:29,04:26,04:23,04:20,04:16'
event_name = "Sehri"
time_zone = "Europe/Berlin"

start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
list_times = [i for i in list_times.split(",") if len(i)>0]

def get_iso_format(obj):
    return obj.isoformat().replace("-","").replace(":","")+"Z"

list_times_formatted = []

for i in range(0,len(list_times)):
    time_str = list_times[i]
    time = datetime.strptime(time_str, "%H:%M").time() 
    dt_st = datetime.combine(start_date+timedelta(days=i), time)
    dt_end = dt_st + timedelta(minutes = event_period_minutes)

    list_times_formatted.append((get_iso_format(dt_st),get_iso_format(dt_end)))


def make_event(dt_start,dt_end,event_name, num):
    return """BEGIN:VEVENT
DTSTART:{}
DTEND:{}
DTSTAMP:20240313T205630Z
ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;CN={};X-NUM-GUESTS=0:mailto:{}
CREATED:20240312T035854Z
LAST-MODIFIED:20240313T205612Z
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:{} - {}
TRANSP:OPAQUE
BEGIN:VALARM
ACTION:DISPLAY
TRIGGER:-P0DT0H30M0S
DESCRIPTION:{}
END:VALARM
END:VEVENT
""".format(dt_start,
           dt_end,
           your_name,
           your_email,
           event_name,
           num,
           reminder_format.format(event_name))
events = ""


count = 1
for i,j in list_times_formatted[0:total_rozay]:
    
    events+=make_event(i,j,event_name, count)
    count +=1


calendar_text = """BEGIN:VCALENDAR
PRODID:-//Google Inc//Google Calendar 70.9054//EN
VERSION:2.0
CALSCALE:GREGORIAN
METHOD:PUBLISH
X-WR-CALNAME:{}
X-WR-TIMEZONE:{}
{}END:VCALENDAR""".format(your_email, time_zone, events)

with open(output_file,"w+") as f:
    f.write(calendar_text)