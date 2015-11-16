__author__ = 'alonso'

import argparse
import re

from collections import Counter
import os, shutil
import nltk


INPUTFILECOLUMNS = "id form lemma pos supersense".split(" ")

class Sentence:
    def __init__(self):
        self.comments = []
        self.indices = []
        self.forms = []
        self.lemmas = []
        self.postags = []
        self.labels = []

    def __str__(self):
        return " ".join(self.forms)

    def featurizesentence(self):
        sentencefeats = []
        for idx, sense in enumerate(self.forms):
            fi = FeatureInstance()
            fi.label = sense
            fi.f_sliding_window(self,idx)
            fi.f_morphology(self.forms[idx],self.postags[idx])
            sentencefeats.append(fi)
        return sentencefeats



class FeatureInstance:
    def __init__(self):
        self.label = []
        self.feats = {}
    def __str__(self):
        return str(self.feats)


    def _featnames(self,idx,windowsize): #"generates the name for w-2,,w+2 style features"
        names = []
        for x in range(windowsize*2+1):
            suffix = x-windowsize
            names.append(idx+"_"+(str(int(suffix))))
        return names

    def _feat_vw_name(self,string):
        return string.replace(':', '<COLON>').replace('|', '<PIPE>').replace(' ', '_')

    def f_sliding_window(self, sentence, idx):
        self.feats["formwindow"] = self.stringwindow(sentence.forms,idx,2,"f")
        self.feats["lemmawindow"] = self.stringwindow(sentence.lemmas,idx,2,"l")
        self.feats["poswindow"] = self.stringwindow(sentence.postags,idx,2,"p")

    def f_embeddings(self):
        pass

    def f_brownclusters(self):
        pass

    def f_morphology(self,word,pos): #this is OLD code and needs review, the POS-trigger conditions are old and not UD-POS based
        mfeats = []
        # check capitalization
        if word[0].isupper() and not word in ["URL", "NUMBER"]:
            mfeats.append("caps")  #first char is uppercase

        # check if contains digits
        #TODO change this condition to a regex
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

        self.feats["morpholofy"] = " ".join(mfeats)

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
                current_sentence.labels.append(parts[4])
    if current_sentence.forms:
        yield current_sentence



def main():
    parser = argparse.ArgumentParser(description="Feature extractor")
    parser.add_argument("--infile",   metavar="FILE", help="input UD format file",default ="../data/samples/train.sample.ud")
    args = parser.parse_args()

    #TODO: The text is already lemmatized at this stage, no need to load Danish lemmatizer
    #

    allfeats = []
    for sent in readSentences(args.infile):
        allfeats.extend(sent.featurizesentence())

    for f in allfeats:
        print(f)





if __name__ == "__main__":
    main()