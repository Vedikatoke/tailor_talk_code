from dateparser import parse
from datetime import datetime, timedelta
from calendar_helper import check_availability, book_slot

class BookingAgent:
    def __init__(self, calendar_service):
        self.service = calendar_service

    def respond(self, user_message):
        print("User input:", user_message) 

        dt = parse(user_message, settings={'PREFER_DATES_FROM': 'future'})
        if dt:
            date = dt.date()
            start_time = dt.time()
            end_time = (datetime.combine(date, start_time) + timedelta(hours=1)).time()

            if check_availability(self.service, date, start_time, end_time):
                book_slot(self.service, "Meeting with AI", date, start_time, end_time)
                return f"Meeting booked on {date} from {start_time.strftime('%I:%M %p')} to {end_time.strftime('%I:%M %p')}."
            else:
                return f"You're already busy on {date} at that time."
        else:
            return "I couldn't understand your request. Try saying something like 'Schedule a call for tomorrow at 2 PM'."
