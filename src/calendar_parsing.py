from icalendar import Calendar
import os
from datetime import datetime

def get_path() -> str:
    """Collects the path of the ics file and returns an error if the path is invalid"""
    path = input("Enter the .ics file path\n").strip()
    if os.path.exists(path):
        return path
    else:
        raise FileNotFoundError("File path invalid\n")
    
today = datetime.now().date()
reminder_list = "Canvas" # Change this if different

def load_cal(path: str):
    """Parses calendar file"""
    file = open(path)
    data = file.read()
    file.close()
    return Calendar.from_ical(data)

def get_upcoming(cal, last_date):
    """Return events from today to specified date"""
    titles = []
    start_dates = []
    
    for event in cal.walk("VEVENT"):
        dtstart = event.get("dtstart").dt
        if isinstance(dtstart, datetime):
            event_date = dtstart.date()
        else:
            event_date = dtstart
        if last_date >= event_date >= today:
            summary = str(event.get("summary"))
            titles.append(summary)
            start_dates.append(dtstart)
    return titles, start_dates
    
        
def get_cutoff_date():
    """Asks for last date to include"""
    date_str = input("Enter the last date that should be included as MM/DD/YYYY\n")
    try:
        last_date = datetime.strptime(date_str, "%m/%d/%Y").date()
        return last_date
    except:
        raise ValueError("Improper date format")
    
def main():
    path = get_path()
    cutoff = get_cutoff_date()
    cal = load_cal(path)
    event_titles_list = get_upcoming(cal, cutoff)
    event_start_dates_list = get_upcoming(cal, cutoff)
    for i in range(0, len(event_titles_list)):
        print(str(event_titles_list[i]) + " " + str(event_start_dates_list[i]))
        i += 1
    return 0
        
main()