import json
import csv

def read_projects_from_csv(filepath):
    allprojectLists = []
    projectList = []
    with open('data/projectinfo.csv') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            allprojectLists.append({'name': row[0], 'buildID': row[1], 'jobID': row[2], 'prevjobID': row[4]})
    with open(filepath) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        for row in f_csv:
            for allprojectList in allprojectLists:
                if allprojectList['jobID'] == row[2]:
                    projectList.append(allprojectList)
    return projectList


def read_json(filepath):
    f = open(filepath, encoding="utf-8")
    file = json.load(f)
    return file

def wirte_txt(txtFile, filepath):
    with open(filepath, "w") as f:
        for line in txtFile:
            f.write(line+'\n')

def wirte_json(jaonFile, filepath):
    with open(filepath, "w") as f:
        json.dump(jaonFile, f)


def read_raw_job(jobid):
    with open('data/jobs/' + jobid + '/testfiles.json', 'r') as f:
        file = json.load(f)
    return file

def read_raw_originsort_job(jobid):
    with open('data/jobs/' + jobid + '/dotestfiles.json', 'r') as f:
        file = json.load(f)
    return file


def read_raw_prev_job(jobid):
    with open('data/prevjobs/' + jobid + '/testfiles.json', 'r') as f:
        file = json.load(f)
    return file


def read_raw_build(buildid):
    with open('data/builds/' + buildid + '/changedfiles.json', 'r') as f:
        file = json.load(f)
    return file


def read_buildTokens(buildid, m):
    if m == 0:
        with open('data/builds/' + buildid + '/MUbuildtokens.json', 'r') as f:
            file = json.load(f)
    if m == 1:
        with open('data/builds/' + buildid + '/MFbuildtokens.json', 'r') as f:
            file = json.load(f)
    return file


def read_jobsTokens(jobid, m):  # 通过jobd来获得其对应的sentences
    if m == 0:
        with open('data/jobs/' + jobid + '/MUjobtokens.json', 'r') as f:
            file = json.load(f)
    if m == 1:
        with open('data/jobs/' + jobid + '/MFjobtokens.json', 'r') as f:
            file = json.load(f)
    return file


def read_BM25Score(filename):
    with open('data/' + filename, 'r') as f:
        file = json.load(f)
    return file


def read_cosScore(jobid):
    with open('data/jobs/' + jobid + '/cosScore.json', 'r') as f:
        file = json.load(f)
    return file


def wirte_csv(context, filepath, header):
    with open(filepath, 'w', newline='') as f:
        if (len(header)):
            f_csv = csv.DictWriter(f, fieldnames=header)
            f_csv.writeheader()
        else:
            f_csv = csv.DictWriter(f)
        f_csv.writerows(context)


def getTestName(rawname):
    name = ''
    for i in rawname:
        if i == '/':
            name = rawname[rawname.index(i):]
            break
    return name



