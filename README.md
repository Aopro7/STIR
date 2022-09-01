# SatTCP:Semantic-aware Two-phase Test Case Prioritization for Continuous Integration
Code for the JSEP 2022 paper *Semantic-aware Two-phase Test Case Prioritization for Continuous Integration*
# Dataset Information
We use the dataset in [Empirically Revisiting and Enhancing IR-Based Test-Case Prioritization](https://dl.acm.org/doi/abs/10.1145/3395363.3397383).
You can download this dataset at <https://sites.google.com/view/ir-based-tcp/resources>, download 'builds.zip' and 'jobs.zip', unzip them into folder 'data' in our epository.
# Getting Started
You can train and use SatTCP by following the steps below, you can also refer to the process in `run_example.py`.
* Data preprocess:
```
data_preprocessing.tokenFileGenerate()
```
* BM25 score calculating:
```
BM25.BM25_Score_Output()
```
* Divide the dataset into trainset and testset
```
dataset_devide.projectlevel_Trainset_Testset_Devide()
```
* Parameter setting
```
base_Model: basic pretrained model that provided by sentence_transformers.
frontdivision: the top ratio of test cases that selected in the phase of coarse-grained filtering(default by 0.5).
backdivision: the bottom ratio of test cases that selected in the phase of coarse-grained filtering(default by 0.05).
```
* Trainging SatTCP:
```
training.SatTCPtraining(frontdivision, backdivision, base_Model, trainset, outputModel, BM25forTrain, epoch)
```
* evaluation:
```
training.COSscore_Output(outputModel, testset, scoreOutput)
evaluation.projectlevel_evolution_for_SatTCP(testset, scoreOutput, evaOutput)
```
