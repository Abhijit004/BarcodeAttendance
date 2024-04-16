import json
import datetime

def write_to_json(data, filename):
    try:
        f = open('attendance/'+filename, "r")
        prev = json.loads(f.read())
        f.close()
        print('prev',prev)
    except:
        prev = []
        print("Making a new file...")
    dataid = set([row["id"] for row in data])
    for row in prev:
        if row["id"] not in dataid:
            data.append(row)
    f = open('attendance/'+filename, "w")
    print('to write: ', data)
    json.dump(data, f)
    f.close()

# Write data to JSON file
# input -> List of IDs present
# output -> data to be written to JSON file
def take_data(idmap):
    from captureBarcodes import captureBarcodes
    print("video is opening, make the students lined up!")
    barcodes = captureBarcodes(idmap)
    
    res = []
    curr = datetime.datetime.now().time()
    time = curr.strftime("%H:%M")
    for b in barcodes:
        if b not in idmap: continue
        res.append({"id": b, "name": idmap[b], "time": time})
    return res

# Uses take_data() to write data to JSON
# input -> void, its entry point to taking attendance
# output -> JSON file for the class
def take_attendance(dept, sem, subject):
    current_date = datetime.date.today()
    date = current_date.isoformat()
    
    try:
        idfile = open('idmap/'+dept+'_'+sem+'.json', 'r')
    except:
        return ("Failure", f"{dept+'_'+sem+'.json'}\n has not been created.")
    
    idmap = json.loads(idfile.read())
    idfile.close()
    
    outfile = dept+'_'+sem+'_'+subject+'_'+date+'.json'

    data = take_data(idmap)
    write_to_json(data, outfile)
    print("attendance taken successfully")
    return ("Success", "Attendance taken successfully")