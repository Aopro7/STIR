import json
import csv

def read_projects_from_csv(filepath):  # 从传入路径读取csv文件，以字典list形式返回：[{"name":**,"buildID":**,"jobID":**},{}...]
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


def wirte_json(jaonFile, filepath):  # 得到json文件，写入路径
    with open(filepath, "w") as f:
        json.dump(jaonFile, f)


def read_raw_job(jobid):  # 通过jobID来获得其对应的完整testfiles文件
    with open('data/jobs/' + jobid + '/testfiles.json', 'r') as f:
        file = json.load(f)
    return file


def read_raw_prev_job(jobid):  # 通过jobID来获得其对应的完整testfiles文件
    with open('data/prevjobs/' + jobid + '/testfiles.json', 'r') as f:
        file = json.load(f)
    return file


def read_raw_build(buildid):  # 通过jobID来获得其对应的完整testfiles文件
    with open('data/builds/' + buildid + '/changedfiles.json', 'r') as f:
        file = json.load(f)
    return file


def read_buildTokens(buildid):  # 通过buildid来获得其对应的tokens
    with open('data/builds/' + buildid + '/buildtokens.json', 'r') as f:
        file = json.load(f)
    return file


def read_jobsTokens(jobid):  # 通过jobd来获得其对应的sentences
    with open('data/jobs/' + jobid + '/jobtokens.json', 'r') as f:
        file = json.load(f)
    return file


def read_BM25Score(filename):  # 通过特定文件名来得到BM25分数
    with open('data/' + filename, 'r') as f:
        file = json.load(f)
    return file


def read_cosScore(jobid):  # 通过jobid来得到嵌入余弦相似度分数
    with open('data/jobs/' + jobid + '/cosScore.json', 'r') as f:
        file = json.load(f)
    return file


def wirte_csv(context, filepath, header):  # 如果header为空的话就不加表头
    with open(filepath, 'w', newline='') as f:
        if (len(header)):
            f_csv = csv.DictWriter(f, fieldnames=header)
            f_csv.writeheader()
        else:
            f_csv = csv.DictWriter(f)
        f_csv.writerows(context)


def wirte_csv_add(context, filepath, header):  # 如果header为空的话就不加表头
    with open(filepath, 'a', newline='') as f:
        if (len(header)):
            f_csv = csv.DictWriter(f, fieldnames=header)
            f_csv.writeheader()
        else:
            f_csv = csv.DictWriter(f)
        f_csv.writerows(context)

