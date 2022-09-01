import training
import data_preprocessing
import BM25
import dataset_devide
import evaluation

data_preprocessing.tokenFileGenerate()

BM25.BM25_Score_Output("data/projectinfo.csv", "data/BM25_score.json")

dataset_devide.projectlevel_Trainset_Testset_Devide()

base_Model = 'all-MiniLM-L6-v2'
trainset = "data/trainset.csv"
testset = "data/testset.csv"
frontdivision = 0.5
backdivision = 0.05
epoch = 5
modelname = 'SatTCP_Imbalance' + str(frontdivision) + '_' + str(backdivision) + "_epo" + str(epoch)
outputModel = './models/' + modelname
scoreOutput = "data/" + modelname + "_score.json"
BM25forTrain = 'data/BM25_score.json'
evaOutput = "data/" + modelname + "_eva" + ".csv"

training.SatTCPtraining(frontdivision, backdivision, base_Model, trainset, outputModel, BM25forTrain,
                      epoch)
training.COSscore_Output(outputModel, testset, scoreOutput)
evaluation.projectlevel_evolution_for_SatTCP(testset, scoreOutput, evaOutput)