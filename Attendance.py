import json
import datetime
from pickle import load, dump

def write_to_json(data, date, filename):
    try:
        f = open('attendance/'+filename, "rb")
        filedata = load(f)
        f.close()
        print("prev", filedata)
    except:
        filedata = {}
        print("Making a new file...")
    if date in filedata:
        filedata[date] = list(set(filedata[date] + data))
    else:
        filedata[date] = data
    
    f = open('attendance/'+filename, "wb")
    print('to write: ', filedata)
    dump(filedata, f)
    f.close()


def take_data(idmap):
    from captureBarcodes import captureBarcodes

    print("video is opening, make the students lined up!")
    barcodes = captureBarcodes(idmap)
    return list(barcodes)


# Uses take_data() to write data to JSON
# input -> void, its entry point to taking attendance
# output -> JSON file for the class
def take_attendance(dept, sem, subject):
    current_date = datetime.date.today()
    date = current_date.isoformat()

    try:
        idfile = open("idmap/" + dept + "_" + sem + ".json", "r")
    except:
        return ("Failure", f"No Student-EnrollID file found\nfor {dept} {sem}")
    
    idmap = json.loads(idfile.read())
    idfile.close()
    
    outfile = dept+'_'+sem+'_'+subject + '.attendinfo'

    data = take_data(idmap)
    write_to_json(data, date, outfile)
    print("attendance taken successfully")
    return ("Success", "Attendance taken successfully")


def nextdate(date):
    currdate = datetime.datetime.strptime(date, "%Y-%m-%d")
    nextdate = currdate + datetime.timedelta(days=1)
    return nextdate.strftime("%Y-%m-%d")


def approveLeave(id, dept, sem, subj, start, end):
    try:
        f = open(f"attendance/{dept}_{sem}_{subj}.json", "r+")
    except:
        return ("Failure", f"No record found for\n{dept}_{sem}_{subj}")
    try:
        idmap = open(f"idmap/{dept}_{sem}.json", "r")
        ids = json.loads(idmap.read())
        idmap.close()
    except:
        return ("Failure", "The Requested department's\nIDmap does not exist")
    
    if id not in ids:
        return ("Failure", "No Student with this ID exists")
    studentName = ids[id]
    attendance = json.loads(f.read())
    # f.close()
    try:
        start = datetime.datetime.strptime(start, '%Y-%m-%d')
        end = datetime.datetime.strptime(end, '%Y-%m-%d')
    except:
        return ("Error", "Please enter correct date format")
    for date in attendance:
        d = datetime.datetime.strptime(date, '%Y-%m-%d')
        if start <= d <= end:
            attendance[date].append(id)
            print("added ", id, "to date", date)
    
    f.seek(0)
    json.dump(attendance, f)
    f.truncate()
    f.close()
    return ("Success", f"Leave for\n{studentName}\ngranted successfully.")
        
        
        
    
    