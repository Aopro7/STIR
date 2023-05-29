import json
import numpy as np
import utils
from gensim.summarization import bm25

def failed_Test_Counting(jobID):
    f = open("data/jobs/" + jobID + "/testfiles.json", encoding="utf-8")
    file = json.load(f)
    failedNumber = 0
    for test in file:
        if(test["fail"] == 1):
            failedNumber += 1
    return failedNumber

def Min_Max_Normalization(rawVec):
    if len(rawVec)== 1:
        return [1.0]
    rawVec2d = []
    rawVec2d.append(rawVec)
    X = np.array(rawVec2d)
    min = X.min()
    max = X.max()
    normedScore = []
    for score in rawVec:
        normedScore.append((score - min)/(max - min))
    return normedScore


def BM25_Score_Output(projectPath, outputpath):
    outputMatrix = []
    projectList = utils.read_projects_from_csv(projectPath)

    for project in projectList:

        query = utils.read_buildTokens(project["buildID"], 0)
        jobslist = utils.read_jobsTokens(project["jobID"], 0)

        bm25Model = bm25.BM25(jobslist)
        bm25_scores = bm25Model.get_scores(query)

        normedScore = Min_Max_Normalization(bm25_scores)
        filedNumber = failed_Test_Counting(project['jobID'])
        n = 0
        while (n < filedNumber):
            normedScore[n] = 1
            n += 1
        outputMatrix.append(normedScore)
    utils.wirte_json(outputMatrix, outputpath)

