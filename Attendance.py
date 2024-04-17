import json
import datetime
from pickle import load, dump

def write_to_json(data, date, filename):
    try:
        f = open('attendance/'+filename, "rb")
        filedata = load(f)
        f.close()
        print('prev',filedata)
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
        idfile = open('idmap/'+dept+'_'+sem+'.json', 'r')
    except:
        return ("Failure", f"No Student-EnrollID file found\nfor {dept} {sem}")
    
    idmap = json.loads(idfile.read())
    idfile.close()
    
    outfile = dept+'_'+sem+'_'+subject + '.attendinfo'

    data = take_data(idmap)
    write_to_json(data, date, outfile)
    print("attendance taken successfully")
    return ("Success", "Attendance taken successfully")