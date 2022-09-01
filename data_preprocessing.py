import utils
from nltk.corpus import stopwords
from nltk import data
import javalang
import re
data.path.append(r"/home/TSP/Test_For_AST/ltkModels/")

# Long Identifiers Segmentation
def spliter(tokens):

        meaningfultokens = tokens
        # split by symbol
        nonsymboltokens = list()
        for token in meaningfultokens:
            tokenlist = re.split('[_. ]', token)
            nonsymboltokens = nonsymboltokens + tokenlist

        # turn pure capital words into lowercase
        nonpureuppertokens = list()
        for token in nonsymboltokens:
            flag = 0
            for i in token:
                if ('a' <= i <= 'z'):
                    flag = 1
            if flag == 0:
                nonpureuppertokens.append(token.lower())
            if flag == 1:
                nonpureuppertokens.append(token)

        # split by capital
        supercleantokens = list()
        for token in nonpureuppertokens:
            i = 0
            index = 0
            while (index < len(token)):
                if ('A' <= token[index] <= 'Z'):
                    if (index != 0):
                        supercleantokens.append(token[i:index].lower())
                        i = index
                if (index == len(token) - 1):
                    supercleantokens.append(token[i:index + 1].lower())
                index = index + 1

        pureenglishtokens = []

        for token in supercleantokens:
            flag = 0
            for i in token:
                if not 'a' <= i <= 'z':
                    flag = 1
                    break
            if flag == 0:
                pureenglishtokens.append(token)

        return pureenglishtokens

def Javawords_cleanout(rawTokensList):  # 去除java关键词token
    Keywords = javalang.tokenizer.Keyword.VALUES
    Modifiers = javalang.tokenizer.Modifier.VALUES
    BasicTypes = javalang.tokenizer.BasicType.VALUES
    Booleans = javalang.tokenizer.Boolean.VALUES
    Separators = javalang.tokenizer.Separator.VALUES
    Operators = javalang.tokenizer.Operator.VALUES
    mixture = Keywords | Modifiers | BasicTypes | Booleans | Separators | Operators
    tokenlist = []
    for rawToken in rawTokensList:
        if rawToken.value not in mixture:
            tokenlist.append(rawToken.value)
    return tokenlist


def basic_tokenizer(sourcecode):
    rawTokensList = javalang.tokenizer.tokenize(sourcecode)
    tokenlist = Javawords_cleanout(rawTokensList)
    return tokenlist


def tokenize(sourcecode):
    BasicTokenList = basic_tokenizer(sourcecode)
    Tokenlist = spliter(BasicTokenList)
    clean_tokens = list()
    sr = stopwords.words('english')
    for token in Tokenlist:
        if (token not in sr)and(len(token)>=3):
            clean_tokens.append(token)
    return clean_tokens

# Generate tokens and output .json file into each folds
def tokenFileGenerate():
    projects = utils.read_projects_from_csv("data/projectinfo.csv")
    for project in projects:
        # for builds, using .java files only
        resultlist = []
        file = utils.read_raw_build(project["buildID"])
        for pair in file:
            filename = pair["name"]
            if len(filename) >= 6 :
                if filename[len(filename) - 5:] == ".java":
                    tokenlist = tokenize(pair["content"])
                    for token in tokenlist:
                        resultlist.append(token)

        path = "data/builds/" + project["buildID"] + "/buildtokens.json"
        utils.wirte_json(resultlist, path)

        # for jobs
        jobtokens = []
        file = utils.read_raw_job(project["jobID"])
        for pair in file:
            tokenlist = tokenize(pair["content"])
            jobtokens.append(tokenlist)

        path = "data/jobs/" + project["jobID"] + "/jobtokens.json"
        utils.wirte_json(jobtokens, path)



