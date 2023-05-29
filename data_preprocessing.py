import utils
from nltk.corpus import stopwords
import javalang
import re

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

def javawords_cleanout(rawTokensList):  # 去除java关键词token
    Keywords = javalang.tokenizer.Keyword.VALUES
    Modifiers = javalang.tokenizer.Modifier.VALUES
    BasicTypes = javalang.tokenizer.BasicType.VALUES
    Booleans = javalang.tokenizer.Boolean.VALUES
    Separators = javalang.tokenizer.Separator.VALUES
    Operators = javalang.tokenizer.Operator.VALUES
    mixture = Keywords | Modifiers | BasicTypes | Booleans | Separators | Operators
    tokenlist = []
    for rawToken in rawTokensList:
        if rawToken not in mixture:
            tokenlist.append(rawToken)
    return tokenlist


def basic_tokenizer(sourcecode):
    rawTokensList = javalang.tokenizer.tokenize(sourcecode)
    identifiers_tokens = []
    for rawtoken in rawTokensList:
        if type(rawtoken) == javalang.tokenizer.Identifier:
            identifiers_tokens.append(rawtoken.value)
    return identifiers_tokens


def tokenize(sourcecode):
    basicTokenList = basic_tokenizer(sourcecode)
    splitedTokenList = spliter(basicTokenList)
    nonJavawordsTokenList = javawords_cleanout(splitedTokenList)
    clean_tokens = list()
    sr = stopwords.words('english')
    for token in nonJavawordsTokenList:
        if (token not in sr) and (len(token) >= 3):
            clean_tokens.append(token)
    MFtokens = clean_tokens
    MUtokens = list(set(MFtokens))
    return MFtokens, MUtokens

# Generate tokens and output .json file into each folds
def tokenFileGenerate():
    projects = utils.read_projects_from_csv("data/projectinfo.csv")
    for project in projects:

        # for builds, using .java files only
        MFbuildtokens = []
        MUbuildtokens = []
        file = utils.read_raw_build(project["buildID"])
        for pair in file:
            filename = pair["name"]
            if len(filename) >= 6:
                if filename[len(filename) - 5:] == ".java":
                    MFtokenlist, MUtokenlist = tokenize(pair["content"])
                    for MFtoken, MUtoken in zip(MFtokenlist, MUtokenlist):
                        MFbuildtokens.append(MFtoken)
                        MUbuildtokens.append(MUtoken)
        MUbuildtokens = list(set(MUbuildtokens))

        utils.wirte_json(MFbuildtokens, "data/builds/" + project["buildID"] + "/MFbuildtokens.json")
        utils.wirte_json(MUbuildtokens, "data/builds/" + project["buildID"] + "/MUbuildtokens.json")

        # for jobs
        MFjobtokens = []
        MUjobtokens = []

        file = utils.read_raw_job(project["jobID"])
        for pair in file:
            MFtokenlist, MUtokenlist = tokenize(pair["content"])
            MFjobtokens.append(MFtokenlist)
            MUjobtokens.append(MUtokenlist)

        utils.wirte_json(MFjobtokens, "data/jobs/" + project["jobID"] + "/MFjobtokens.json")
        utils.wirte_json(MUjobtokens, "data/jobs/" + project["jobID"] + "/MUjobtokens.json")

