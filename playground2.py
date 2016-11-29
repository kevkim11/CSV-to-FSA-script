from datetime import datetime

todays_date_and_time = str(datetime.today())
date_and_time_list = todays_date_and_time.split()
date_list_str = date_and_time_list[0].split('-')
date_list_int = [int(x) for x in date_list_str]
time_list_str = date_and_time_list[1].split(':')
time_list_int = [float(x) for x in time_list_str]
print date_list_str
print time_list_str
print date_list_int
print time_list_int