__author__ = 'alonso'

import argparse
import re
import numpy as np
from collections import Counter, defaultdict
import os, shutil
import sys, os

import nltk

INPUTFILECOLUMNS = "id form lemma pos supersense".split(" ")

class Sentence:
    def __init__(self):
        self.comments = []
        self.indices = []
        self.forms = []
        self.lemmas = []
        self.postags = []
        self.supersenses = []

    def __str__(self):
        return " ".join(self.forms)

    def _instanceid(self,sentid,wordid):
        return "'"+str(sentid)+"-"+str(wordid)

    def featurizesentence_supersense(self,sentid,embeddings,dimensions,brownclusters,senselexicon,wordnet):
        sentencefeats = []
        for idx, sense in enumerate(self.supersenses):
            fi = FeatureInstance()
            fi.label =  "B-noun.person" if sense == "_" else sense
            fi.instanceid = self._instanceid(sentid,idx)
            fi.f_sliding_window_supersense(self,idx)
            fi.f_morphology(self.forms[idx],self.postags[idx])
            fi.f_embeddings(self.forms[idx],embeddings,dimensions)
            fi.f_brownclusters(self.forms[idx],brownclusters)
            fi.f_lexiconfeats(self.forms[idx],senselexicon)
            fi.f_ontotype_feature(self.postags[idx],self.lemmas[idx],wordnet)
            sentencefeats.append(fi)
        return sentencefeats

    def featurizesentence_pos(self,sentid,brownclusters):
        sentencefeats = []
        for idx, postag in enumerate(self.postags):
            fi = FeatureInstance()
            fi.instanceid = self._instanceid(sentid,idx)
            fi.label = "NOUN" if postag == "_" else postag
            fi.f_sliding_window_pos(self,idx)
            fi.f_morphology(self.forms[idx],self.postags[idx])
            fi.f_brownclusters(self.forms[idx],brownclusters)
            sentencefeats.append(fi)
        return sentencefeats

class FeatureInstance:
    def __init__(self):
        self.label = ""
        self.feats = {}
        self.instanceid = ""
        self.checkpos = {"NOUN": 'n', "VERB": 'v', "ADJ": "a", "AUX":"v"}

    def __str__(self):
        return self.label+" "+self.instanceid+"|"+ " |".join([k+" "+self.feats[k] for k in self.feats.keys()])

    def _get_embedding(self,word,embeddings,dimensions):
        if word in embeddings:
            embed=embeddings[word]
        else:
            embed = [0.0] * dimensions
        return embed

    def _featnamelist(self,pref,n):
        namelist = []
        for i in range(n):
            namelist.append(pref+"_"+str(i))
        return namelist



    def _featnames(self,idx,windowsize): #"generates the name for w-2,,w+2 style features"
        names = []
        for x in range(windowsize*2+1):
            suffix = x-windowsize
            names.append(idx+"_"+(str(int(suffix))))
        return names

    def _feat_vw_name(self,string):
        return string.replace(':', '<COLON>').replace('|', '<PIPE>').replace(' ', '_')

    def f_sliding_window_supersense(self, sentence, idx):
        self.feats["formwindow"] = self.stringwindow(sentence.forms,idx,2,"f").lower()
        self.feats["lemmawindow"] = self.stringwindow(sentence.lemmas,idx,2,"l").lower()
        self.feats["poswindow"] = self.stringwindow(sentence.postags,idx,2,"p")

    def f_sliding_window_pos(self, sentence, idx):
        self.feats["formwindow"] = self.stringwindow(sentence.forms,idx,2,"f")

    def f_embeddings(self,word,embeddings,dimensions):
        current_v = self._get_embedding(word,embeddings,dimensions)
        self.feats["embeddings"] = " ".join(["e"+str(i)+":"+str(v) for i,v in enumerate(current_v)])

    def f_brownclusters(self,word,brownclusters):
        self.feats["brownclusters"] =  brownclusters.get(word.lower(),"OOV")

    def f_lexiconfeats(self,word,senselexicon):
        self.feats["senselexicon"] =  " ".join(sorted(senselexicon.get(word.lower(),[])))

    def f_ontotype_feature(self,pos,lemma,dannet):
        ot = "_"
        if pos in self.checkpos.keys():
            s = dannet.synsets(lemma.lower()+"."+self.checkpos[pos])
            if s:
                ot = s[0].attrs()["ontological_type"].replace("(","").replace(")","")
                if not ot:
                    ot="OOV"
        ot = ot.replace("(","").replace(")","")
        if "+" in ot:
            ot = ot +" "+" ".join(ot.split("+"))
        self.feats["ontotype"] =  ot




    def f_morphology(self,word,pos): #this is OLD code and needs review, the POS-trigger conditions are old and not UD-POS based
        mfeats = []
        # check capitalization
        if word[0].isupper() and not word in ["URL", "NUMBER"]:
            mfeats.append("caps")  #first char is uppercase

        # check if contains digits
        if "0" in word or pos == "NUM":
            mfeats.append("num")



        # check if contains hyphen
        if "-" in word:
            mfeats.append("hyphen")

        if pos in ["NOUN", "PROPN"] and word.endswith("s") or word.endswith("s'"): #possible genitive marker
            mfeats.append("genmark")


        # single character
        if len(word) == 1:
            mfeats.append("single")

        # 3char suffix
        if len(word) > 4:
            mfeats.append("suffix=" + self._feat_vw_name(word[-3:]))
        else:
            mfeats.append("suffix=_")

        # 3char prefix
        if len(word) > 4:
            mfeats.append("prefix=" + self._feat_vw_name(word[:3]))
        else:
            mfeats.append("prefix=" + self._feat_vw_name(word))

        # if entire word is uppercase
        if word.isupper():
            mfeats.append("allUpper")
        # only letters
        if word.isalpha():
            mfeats.append("alphanum")
        result = []
        for c in word:
            if c.isupper():
                result.append('X')
            elif c.islower():
                result.append('x')
            elif c in '0123456789':
                result.append('d')
            else:
                result.append("-")
        mfeats.append("shape="+re.sub(r"x+", "x*", ''.join(result)))

        self.feats["morphology"] = " ".join(mfeats)

    def stringwindow(self, stringlist, index, windowsize, name): #for [a,b,c,d,e], i=2 and windowsize=2, returns [a,b,c,d] with headers for each value
        paddedlist = ["^","_"] + stringlist + ["_","$"]
        index = index + windowsize
        values = paddedlist[(index-windowsize):index+windowsize+1]
        names = self._featnames(name, windowsize)
        result = []
        for n, v in zip(names, values):
            result.append(self._feat_vw_name(n+"="+v))
        return " ".join(result)



def readSentences(infile):
    current_sentence = Sentence()

    for line_no, line in enumerate(open(infile), 1):
        line = line.strip("\n")
        if not line:
            # Add extra properties to ROOT node if exists
            # Handle multi-tokens
            yield current_sentence
            current_sentence = Sentence()
        elif line.startswith("#"):
            current_sentence.comments.append(line)
        else:
            parts = line.split("\t")
            if len(parts) != len(INPUTFILECOLUMNS):
                error_msg = 'Invalid number of columns in line {} (found {}, expected {})'.format(line_no, len(parts), len(INPUTFILECOLUMNS))
                raise Exception(error_msg)
            else:
                current_sentence.indices.append(parts[0])
                current_sentence.forms.append(parts[1])
                current_sentence.lemmas.append(parts[2])
                current_sentence.postags.append(parts[3])
                current_sentence.supersenses.append(parts[4])
    if current_sentence.forms:
        yield current_sentence



def readclusters(infile):
    words2ids = {}
    for l in open(infile).readlines():
        fields = l.strip().split("\t")
        clusterId = fields[0]
        word = fields[1]
        words2ids[word] = clusterId
    return words2ids


def readembeddings(infile):
    embeddings = {}
    dimensions = 0
    for line in open(infile).readlines():
        line = line.strip()
        if line:
            a= line.split(" ")
            embeddings[a[0]] = np.array([float(v) for v in a[1:]]) #cast to float, otherwise we cannot operate
            dimensions = len(a[1:])
    return (embeddings,dimensions)

def readsenselexicon(folder):
    D = defaultdict(set)
    for file in os.listdir(folder):
        for line in open(folder+"/"+file).readlines():
            line = line.strip()
            if " " in line:
                continue
            else:
                D[line].add(file)
    return D

def main():
    parser = argparse.ArgumentParser(description="Feature extractor")
    parser.add_argument("--infile",   metavar="FILE", help="input UD format file",default ="../data/pos/da-ud-dev.pos.ud")
    parser.add_argument("--brownclusters",   metavar="FILE", help="input UD format file",default ="../data/res/brownpaths_clarin_500")
    parser.add_argument("--embeddings",   metavar="FILE", help="input UD format file",default ="../data/res/da.clarindk.embd")
    parser.add_argument("--senselexiconfolder",   metavar="FILE", help="input UD format file",default ="../data/res/senselists/")
    parser.add_argument("--labels",  help="supersense/pos", default ="supersense")

    args = parser.parse_args()
    browndict = readclusters(args.brownclusters)


    if args.labels == "supersense":
        sys.path.append('./uniwordnet/')
        import uniwordnet.universal as universal
        from uniwordnet.dannet import DannetLoader, Dannet
        (embeddings,dimensions) = readembeddings(args.embeddings)
        senselexicon = readsenselexicon(args.senselexiconfolder)
        dannet = Dannet.load('/Users/alonso/data/DanNet-2.2_csv')
        allfeats = []
        for sentid,sent in enumerate(readSentences(args.infile)):
            allfeats.extend(sent.featurizesentence_supersense(sentid,embeddings,dimensions,browndict,senselexicon,dannet))
            allfeats.append("")

    elif args.labels == "pos":
        allfeats = []
        for sentid,sent in enumerate(readSentences(args.infile)):
            allfeats.extend(sent.featurizesentence_pos(sentid,browndict))
            allfeats.append("")
    else:
        exit("bad label type")

    for f in allfeats:
        print(f)





if __name__ == "__main__":
    main()