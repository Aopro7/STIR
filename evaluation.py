import training
import utils
import numpy as np
def projectlevel_evolution_for_SatTCP(testlistpath, scorepath, outputpath):
    totaleva = []
    projectList = utils.read_projects_from_csv(testlistpath)
    lenth = len(projectList)
    scorematrix = utils.read_json(scorepath)
    header = ['name', 'APFDcmean', 'APFDcmid','APFDmean','APFDmid']
    visited = ['apache-incubator-dubbo']
    lastname = 'apache-incubator-dubbo'
    currentlist = []
    currentscore = []
    print("evoluting on testset...")
    for project,score in zip(projectList,scorematrix):

        if(project['name'] not in visited):
            visited.append(project['name'])
            APFDcmean, APFDcmid = APFDc_for_SatTCP(currentlist, currentscore)
            APFDmean, APFDmid = APFD_for_SatTCP(currentlist, currentscore)
            totaleva.append({"name":lastname,"APFDcmean":APFDcmean, "APFDcmid":APFDcmid, "APFDmean":APFDmean, "APFDmid":APFDmid})
            lastname = project['name']
            currentlist = []
            currentscore = []

        currentlist.append(project)
        currentscore.append(score)

        if (projectList.index(project) == lenth-1):
            visited.append(project['name'])
            APFDcmean, APFDcmid = APFDc_for_SatTCP(currentlist, currentscore)
            APFDmean, APFDmid = APFD_for_SatTCP(currentlist, currentscore)
            totaleva.append({"name":project['name'],"APFDcmean":APFDcmean, "APFDcmid":APFDcmid, "APFDmean":APFDmean, "APFDmid":APFDmid})
            currentlist = []
            currentscore = []

    utils.wirte_csv(totaleva, outputpath, header)

def APFDc_for_SatTCP(projectsFileOrpath,scoreFileOrpath):
    APFDcScore = []
    if type(projectsFileOrpath) == list:
        projectList = projectsFileOrpath
    else:
        projectList = utils.read_projects_from_csv(projectsFileOrpath)
    if type(scoreFileOrpath) == list:
        scores = scoreFileOrpath
    else:
        scores = utils.read_json(scoreFileOrpath)

    for project, score in zip(projectList, scores):
        file = utils.read_raw_job(project["jobID"])
        m = 0
        n = len(file)
        SortedIndex = list(np.argsort(-(np.array(score))))
        totalTime = 0
        for dic in file:
            totalTime += dic["time"]
            if dic["fail"] == 1:
                m += 1
        totalTime = totalTime * m
        savedTimeTotal = 0

        for i in range(m):
            savedTime = 0
            for ii in range(SortedIndex.index(i), n):
                savedTime += file[SortedIndex[ii]]["time"]
            hundledTime = savedTime - (0.5 * file[i]["time"])
            savedTimeTotal += hundledTime
        APFDcScore.append(savedTimeTotal/totalTime)
    APFDcmean = sum(APFDcScore) / len(APFDcScore)
    APFDcmid = sorted(APFDcScore)[int(len(APFDcScore) / 2)]
    return APFDcmean, APFDcmid

def APFD_for_SatTCP(projectsFileOrpath,scoreFileOrpath):
    APFDScore = []
    if type(projectsFileOrpath) == list:
        projectList = projectsFileOrpath
    else:
        projectList = utils.read_projects_from_csv(projectsFileOrpath)
    if type(scoreFileOrpath) == list:
        scores = scoreFileOrpath
    else:
        scores = utils.read_json(scoreFileOrpath)

    for project, score in zip(projectList, scores):
        file = utils.read_raw_job(project["jobID"])
        m = 0
        n = len(file)
        SortedIndex = list(np.argsort(-(np.array(score))))
        for dic in file:
            if dic["fail"] == 1:
                m += 1

        sumTFi = 0
        for i in range(m):
            sumTFi += SortedIndex.index(i) + 1
        result = (1 - (sumTFi / (n * m)) + 1 / (2 * n))
        APFDScore.append(result)

    APFDmean = sum(APFDScore) / len(APFDScore)
    APFDmid = sorted(APFDScore)[int(len(APFDScore) / 2)]

    return APFDmean, APFDmid



