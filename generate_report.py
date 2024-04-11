import os
import csv
import json
def generateReport(data, filename):
    field_names = ['id', 'name', 'time']

    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        # Write header
        writer.writeheader()

        # Write rows
        for row in data:
            writer.writerow(row)

    print(f"CSV file '{filename}' has been created successfully.")

def grandReport(filename):
    filename = filename+'.json'
    currdir = os.getcwd()
    files = os.listdir(currdir)
    f = open(filename)
    idmap = json.loads(f.read())
    f.close()
    idmap = sorted(idmap.items(), key = lambda x: x[0])
    print('idmap\n', idmap)
    res = []
    
    indexid, i = {}, 0
    for id, name in idmap:
        res.append({"Reg No": id, "Name": name})
        indexid[id] = i
        i += 1
        
    print('res initial look\n', res)
    print('index ID\n', indexid)
    
    # for file in files:
    #     if file.startswith(filename) and :
    #         f = open(file, 'r')
    #         data = json.loads(f.read())
            
    print(files)
# grandReport('IT_sem4')
