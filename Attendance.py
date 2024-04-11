import json
import datetime
from generate_report import *
from captureBarcodes import *

def write_to_json(data, filename):
    f = open(filename, "w")
    json.dump(data, f)
    f.close()

# Write data to JSON file
# input -> List of IDs present
# output -> data to be written to JSON file
def take_data(idmap):
    print("video is opening, make the students lined up!")
    barcodes = captureBarcodes()
    
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
def take_attendance():
    dept = input("Department(short-form): ").upper()
    sem = "sem"+input("Semester(1-8): ")
    subject = input("Subject code: ")
    currdate = datetime.datetime.now().date()
    date = currdate.strftime("%d%B%Y")
    
    idfile = open(dept+'_'+sem+'.json', 'r')
    idmap = json.loads(idfile.read())
    idfile.close()
    
    outfile = dept+'_'+sem+'_'+subject+'_'+date+'.json'

    data = take_data(idmap)
    write_to_json(data, outfile)
    print("attendance taken successfully")

#input-> void, starting point for report generation
#output->csv report file
def report():
    dept = input("Department(short-form): ").upper()
    sem = "sem"+input("Semester(1-8): ")
    subject = input("Subject code: ")
    date = input("date: (format: dd Mon yyyy)").replace(' ', '')
    outfile = dept+'_'+sem+'_'+subject+'_'+date+'.json'
    
    try:
        jsonfile = open(outfile, 'r')
        data = json.loads(jsonfile.read())
        jsonfile.close()
    except:
        print(outfile, "no file exist")
        return
    generateReport(data, outfile[:-4]+'csv')

def start():
    print("welcome to barcode attendance!")
    y = input("take attendance(1) / generate report(2): ")
    take_attendance() if y == '1' else report()
    
start()
