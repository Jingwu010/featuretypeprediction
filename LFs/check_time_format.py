import datetime
def check_time_format(timestring):
    match = 0
    try:
        datetime.datetime.strptime(timestring, '%I:%M')     # 3:14
        match += 1
        datetime.datetime.strptime(timestring, '%H:%M')     # 13:14
        match += 1
        datetime.datetime.strptime(timestring, '%I:%M:%S')  # 3:14:00
        match += 1
        datetime.datetime.strptime(timestring, '%H:%M:%S')  # 13:14:00
        match += 1
    except:
        pass
    if match > 0:
        return True
    else:
        return False