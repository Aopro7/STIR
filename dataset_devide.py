import utils
from copy import deepcopy
from random import randint

def shuffle(lst):
    temp_listB = deepcopy(lst)
    m = len(temp_listB)
    while (m):
        m -= 1
        i = randint(0, m)
        temp_listB[m], temp_listB[i] = temp_listB[i], temp_listB[m]
    return temp_listB

def projectlevel_Trainset_Testset_Devide():
    proportion = 0.9
    projectList = utils.read_projects_from_csv("data/projectinfo.csv")
    trainlist = []
    testlist = []
    currentlist = []
    visited = ['apache-incubator-dubbo']
    lenth = len(projectList)

    for project in projectList:
        if(project['name'] not in visited):
            visited.append(project['name'])
            if len(currentlist) == 1:
                currentlist = []
                continue
            currentlist = shuffle(currentlist)
            deviding = int(len(currentlist)*proportion)
            for dic in currentlist[:deviding]:
                trainlist.append(dic)
            for dic in currentlist[deviding:]:
                testlist.append(dic)
            currentlist = []
        currentlist.append(project)
        if (projectList.index(project) == lenth-1):
            visited.append(project['name'])
            if len(currentlist) == 1:
                currentlist = []
                continue
            currentlist = shuffle(currentlist)
            deviding = int(len(currentlist)*proportion)
            for dic in currentlist[:deviding]:
                trainlist.append(dic)
            for dic in currentlist[deviding:]:
                testlist.append(dic)
            currentlist = []
    header = ['name', 'buildID', 'jobID']
    utils.wirte_csv(trainlist,'data/trainset.csv',header)
    utils.wirte_csv(testlist,'data/testset.csv',header)