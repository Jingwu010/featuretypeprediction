def lf_key_word_name(row):
    # a key word in attribute name while has different representation from classes
    # PRIORITY: 2
    # e.g. student_id  studentID
    # 1. attribute name contains id
    string = str(row['Attribute_name'])
    parts = re.split('[^a-zA-Z0-9]', string)
    for part in parts:
        if part.lower() == 'id':
            return 5
    if re.findall('ID', string):
        return 5
    return 0

