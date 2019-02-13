import datetime
def check_date_format(datestring):
    match = False
    try:
        # [TODO] Clever way to do this
        datetime.datetime.strptime(datestring, '%Y-%m-%d')      # yyyy-mm-dd
        match = True
        datetime.datetime.strptime(datestring, '%d/%b/%Y')      # yyyy-mmm-dd
        match = True
        datetime.datetime.strptime(datestring, '%Y-%j')         # yyyy-dddd
        match = True
        datetime.datetime.strptime(datestring, '%d/%m/%Y')      # dd/mm/yyyy
        match = True
        datetime.datetime.strptime(datestring, '%m/%d/%Y')      # mm/dd/yyyy
        match = True
        datetime.datetime.strptime(datestring, '%d/%m/%y')      # 31/07/13
        match = True
        datetime.datetime.strptime(datestring, '%m/%d/%y')      # mm/dd/yy
        match = True
    except:
        pass
    if match > 0:
        return True
    else:
        return False