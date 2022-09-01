from sentence_transformers import SentenceTransformer, SentencesDataset, InputExample, evaluation, losses, util
from torch.utils.data import DataLoader
import numpy as np
import utils
from copy import deepcopy
from random import randint

def shuffle(lstB, lstJ, labels):
    temp_listB = deepcopy(lstB)
    temp_listJ = deepcopy(lstJ)
    temp_labels = deepcopy(labels)
    m = len(temp_listB)
    while (m):
        m -= 1
        i = randint(0, m)
        temp_listB[m], temp_listB[i] = temp_listB[i], temp_listB[m]
        temp_listJ[m], temp_listJ[i] = temp_listJ[i], temp_listJ[m]
        temp_labels[m], temp_labels[i] = temp_labels[i], temp_labels[m]
    return temp_listB, temp_listJ, temp_labels

def getscore(projectpath, socrepath):
    allprojects = utils.read_projects_from_csv("data/projectinfo.csv")
    trainprojects = utils.read_projects_from_csv(projectpath)
    allscore = utils.read_json(socrepath)
    Score = []
    for trainproject in trainprojects:
        Score.append(allscore[allprojects.index(trainproject)])
    return Score

def SatTCPtraining(frontdivision, backdivision, modelname, trainprojectpath, outputpath, socrepath,
                                   epochnum):
    model = SentenceTransformer(modelname)
    BM25scores = getscore(trainprojectpath, socrepath)
    projectList = utils.read_projects_from_csv(trainprojectpath)
    builds_list = []
    jobs_list = []
    labels = []
    print("Trainingset loading...")
    for project, BM25score in zip(projectList, BM25scores):

        currentjobs = utils.read_raw_job(project['jobID'])
        file_q = utils.read_buildTokens(project['buildID'])
        qurey = " ".join(file_q)
        sentences = utils.read_jobsTokens(project['jobID'])

        SortedIndex = list(np.argsort(-(np.array(BM25score))))

        lenth = len(SortedIndex)
        frontselection = int(lenth * frontdivision)
        backselection = int(lenth * backdivision)
        if frontselection < 1:
            frontselection = 1

        if lenth == 1:
            builds_list.append(qurey)
            jobs_list.append(" ".join(sentences[0]))
            labels.append(1)
            continue

        for sentenceindex in SortedIndex[:frontselection]:
            builds_list.append(qurey)
            jobs_list.append(" ".join(sentences[sentenceindex]))
            if currentjobs[sentenceindex]["fail"] == 1:
                labels.append(1)
            else:
                labels.append(0)
        if backdivision != 0:
            if backselection < 1:
                backselection = 1
            for sentenceindex in SortedIndex[(lenth - backselection):]:
                builds_list.append(qurey)
                jobs_list.append(" ".join(sentences[sentenceindex]))
                if currentjobs[sentenceindex]["fail"] == 1:
                    labels.append(1)
                else:
                    labels.append(0)

    shuffle_builds_list, shuffle_jobs_list, shuffle_labels = shuffle(builds_list, jobs_list, labels)
    train_size = int(len(shuffle_builds_list) * 0.9)

    train_data = []
    for idx in range(train_size):
        train_data.append(
            InputExample(texts=[shuffle_builds_list[idx], shuffle_jobs_list[idx]], label=float(shuffle_labels[idx])))

    eval_builds = shuffle_builds_list[train_size:]
    eval_jobs = shuffle_jobs_list[train_size:]
    eval_label = shuffle_labels[train_size:]
    evaluator = evaluation.EmbeddingSimilarityEvaluator(eval_builds, eval_jobs, eval_label)

    train_dataset = SentencesDataset(train_data, model)
    train_dataloader = DataLoader(train_dataset, shuffle=True, batch_size=68)
    train_loss = losses.CosineSimilarityLoss(model)

    model.fit(train_objectives=[(train_dataloader, train_loss)], epochs=epochnum, warmup_steps=100, evaluator=evaluator,
              evaluation_steps=1000, output_path=outputpath)

def COSscore_Output(modelpath, testprojectpath, outputpath):
    print("Testset's cosScore generating...")
    model = SentenceTransformer(modelpath)
    cosScoresMatrix = []
    projectList = utils.read_projects_from_csv(testprojectpath)

    for project in projectList:
        qurey = " ".join(utils.read_buildTokens(project['buildID']))
        sentences = []
        file = utils.read_jobsTokens(project['jobID'])
        for sentence in file:
            sentences.append(" ".join(sentence))
        cosScores = util.pytorch_cos_sim(model.encode(qurey), model.encode(sentences))
        cosScores = cosScores.tolist()
        cosScoreslist = cosScores[0]
        cosScoresMatrix.append(cosScoreslist)
    utils.wirte_json(cosScoresMatrix, outputpath)


