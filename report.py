import os, csv, json

def generateReport(dept, sem, subject, date):
    # no longer needed now.
    filename = dept + "_" + sem + "_" + subject + "_" + date
    try:
        jsonfile = open("attendance/" + filename+".json", "r")
        data = json.loads(jsonfile.read())
        jsonfile.close()
    except:
        print(filename, "The requested file does not exist")
        return ("Failure", f"{filename}\nThe requested file\ndoes not exist")

    field_names = ["Reg No", "Name", "Time Entered"]

    with open("output/" + filename+".csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        for row in data:
            writer.writerow({'Reg No': row['id'], 'Name': row['name'], 'Time Entered': row['time']})

    print(f"CSV file 'output/{filename}' has been created successfully.")
    return ("Success", f"{filename}'\nhas been created successfully.")


def grandReport(dept, sem, subject):
    filename = dept + "_" + sem + "_" + subject
    try:
        f = open(f"idmap/{dept}_{sem}.json")
    except:
        print("The requested department's ID-NAME map has not been created.")
        return ("Failure", f"idmap/{dept}_{sem}.json\nhas not been created.")
    idmap = json.loads(f.read())
    f.close()
    idmap = sorted(idmap.items(), key=lambda x: x[0])
    # print('idmap\n', idmap)
    print()
    res = []

    for id, name in idmap:
        res.append({"Reg No": id, "Name": name})

    try:
        classfile = open(f"attendance/{filename}.json")
        classfiledata = json.loads(classfile.read())
    except:
        return ("Empty", "No data available!")
    totWorkingDays = len(classfiledata)
    if totWorkingDays == 0: 
        return ("Empty", "No data available!")
    
    for date, presentList in classfiledata.items():
        for row in res:
            row[date] = "P" if row["Reg No"] in presentList else "A"
    
    for row in res:
        row["Total"] = list(row.values()).count("P")
        row["Percentage"] = row["Total"] / totWorkingDays
    field_names = list(res[0].keys())

    with open(f"output/{filename}.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(res)
    return ("Success", f"Report generation completed!\nin output/{filename}.csv")
