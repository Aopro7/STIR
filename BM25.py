import json
import numpy as np
import math
import utils

def failed_Test_Counting(jobID):
    f = open("data/jobs/" + jobID + "/testfiles.json", encoding="utf-8")
    file = json.load(f)
    failedNumber = 0
    for test in file:
        if(test["fail"] == 1):
            failedNumber += 1
    return failedNumber

class BM25(object):

    def __init__(self,docs):
        self.D = len(docs)
        self.avgdl = sum([len(doc) + 0.0 for doc in docs]) / self.D
        self.docs = docs
        self.f = []
        self.df = {}
        self.idf = {}
        self.k1 = 1.5
        self.k2 = 0.0
        self.b = 0.75
        self.init()

    def init(self):
        for doc in self.docs:
            tmp = {}
            for word in doc:
                tmp[word] = tmp.get(word,0) + 1
            self.f.append(tmp)
            for k in tmp.keys():
                self.df[k] = self.df.get(k,0) + 1
        for k,v in self.df.items():
            self.idf[k] = math.log(self.D-v+0.5)-math.log(v+0.5)

    def sim(self,doc,index):
        score = 0
        for word in doc:
            if word not in self.f[index]:
                continue
            d = len(self.docs[index])
            score += (self.idf[word]*(self.f[index][word]/d)*(self.k1+1)
                      / ((self.f[index][word]/d)+self.k1*(1-self.b+self.b*d
                                                      / self.avgdl)))
        return score

    def simall(self,doc):
        scores = []
        for index in range(self.D):
            score = self.sim(doc,index)
            scores.append(score)
        return scores


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
        query = utils.read_buildTokens(project["buildID"])
        jobslist = utils.read_jobsTokens(project["jobID"])
        s = BM25(jobslist)
        test_score = s.simall(query)
        normedScore = Min_Max_Normalization(test_score)
        filedNumber = failed_Test_Counting(project['jobID'])
        n = 0
        while (n < filedNumber):
            normedScore[n] = 1
            n += 1
        outputMatrix.append(normedScore)

    with open(outputpath, 'w') as f:
        json.dump(outputMatrix, f)
