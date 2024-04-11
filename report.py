import os
import csv
import json


def generateReport(dept, sem, subject, date):
    filename = dept + "_" + sem + "_" + subject + "_" + date + ".json"
    try:
        jsonfile = open("attendance/" + filename, "r")
        data = json.loads(jsonfile.read())
        jsonfile.close()
    except:
        print(filename, "The requested file does not exist")
        return False

    field_names = ["id", "name", "time"]

    with open("output/" + filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        # Write header
        writer.writeheader()

        # Write rows
        for row in data:
            writer.writerow(row)

    print(f"CSV file 'output/{filename}' has been created successfully.")
    return True


# def grandReport(filename: str):
def grandReport(dept, sem, subject):
    filename = dept + "_" + sem + "_" + subject
    currdir = os.getcwd()
    files = os.listdir(currdir + "/attendance")
    r = filename.rfind("_")
    f = open("idmap/" + filename[:r] + ".json")
    idmap = json.loads(f.read())
    f.close()
    idmap = sorted(idmap.items(), key=lambda x: x[0])
    # print('idmap\n', idmap)
    print()
    res = []

    indexid, i = {}, 0
    for id, name in idmap:
        res.append({"Reg No": id, "Name": name})
        indexid[id] = i
        i += 1

    for file in files:
        if file.startswith(filename):
            print(file)
            f = open("attendance/" + file, "r")
            data = json.loads(f.read())
            # print('data\n', data, '\n')
            f.close()
            l, r = file.rfind("_") + 1, file.rfind(".")
            date = file[l:r]
            for student in data:
                if student["id"] in indexid:
                    # print(student["id"])
                    j = indexid[student["id"]]
                    res[j][date] = "P"

            for row in res:
                if date not in row:
                    row[date] = "A"

    # print(res)
    totaldays = len(res[0]) - 2
    for row in res:
        row["Total"] = list(row.values()).count("P")
        row["%"] = 100 * row["Total"] / totaldays

    field_names = list(res[0].keys())

    with open(f"output/{filename}.csv", "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)

        # Write header
        writer.writeheader()

        # Write rows
        for row in res:
            writer.writerow(row)

    print(f"CSV file {filename} has been created successfully.")


# grandReport('IT_sem4_IT2203')
