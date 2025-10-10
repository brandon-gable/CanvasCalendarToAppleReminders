from icalendar import Calendar
import os
from datetime import datetime
import subprocess

def get_path():
    """Collects the path of the ics file and returns an error if the path is invalid"""
    path = os.path.expanduser(input("Enter the .ics file path\n").strip())
    if os.path.exists(path):
        return path
    else:
        raise FileNotFoundError("File path invalid\n")
    
today = datetime.now().date()

def load_cal(path: str):
    """Parses calendar file"""
    file = open(path, "rb")
    data = file.read()
    file.close()
    return Calendar.from_ical(data)

def get_upcoming(cal, last_date):
    """Return events from today to specified date"""
    titles = []
    start_dates = []
    
    include_course_codes = input("Do you want to include the courses in the name of each reminder?\nEnter Y or N.\n")
    
    for event in cal.walk("VEVENT"):
        dtstart = event.get("dtstart").dt
        if isinstance(dtstart, datetime):
            event_date = dtstart.date()
        else:
            event_date = dtstart
        if last_date >= event_date >= today:
            if include_course_codes == 'N':
                summary = str(event.get("summary"))
                start = summary.find('[')
                new_summary = summary[:start]
                titles.append(new_summary)
            elif include_course_codes == 'Y':
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
    
reminders_list = 'Canvas' # Change this if different

def create_reminder(index, title, dt):
    """Adds the reminders to Apple Reminders"""
    safe_title = title.replace('"', '\\"')
    if isinstance(dt, datetime):
        dt_val = dt.date()
    else:
        dt_val = dt
    dt_str = dt_val.strftime("%B %d, %Y")
    reminder = "r_" + str(index)
    script = ""
    script += "set " + reminder + " to (make new reminder at end of reminders of theList)\n"
    script += "set name of " + reminder + " to \"" + safe_title + "\"\n"
    script += "set due date of " + reminder + " to date \"" + dt_str + "\"\n"
    return script

def main():
    path = get_path()
    cutoff = get_cutoff_date()
    cal = load_cal(path)
    event_titles_list, event_start_dates_list = get_upcoming(cal, cutoff)
    if not event_titles_list:
        return 0
    applescript = 'tell Application "Reminders"\n'
    applescript += 'set theList to list "' + reminders_list.replace('"', '\\"') + '"\n'
    for i in range(len(event_titles_list)):
        applescript += create_reminder(i, event_titles_list[i], event_start_dates_list[i])
    applescript += 'end tell\n'
    try:
        subprocess.run(["osascript", "-"], input=applescript, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print("osascript failed:\n", e.stderr)
        return 1
    print("Created " + str(len(event_titles_list)) + " reminders\n")
    return 0

main()