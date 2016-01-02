import argparse
from lillelemma.sto_lemmatizer import StoLemmatizer

def main():
    parser = argparse.ArgumentParser(description="Join rungsted input and original file in a 5-column input file for feature extraction")
    parser.add_argument("--pospredictions",   metavar="FILE", help="input UD format file",default ="../data/pos/pred.out")
    parser.add_argument("--udfile",   metavar="FILE", help="input UD format file",default ="../data/sstannotated/ddt.1206.curated.ud")
    args = parser.parse_args()
    lemmatizer = StoLemmatizer()


    for lineud, linepospredictions in zip(open(args.udfile).readlines(),open(args.pospredictions).readlines()):
        lineud = lineud.strip()
        linepospredictions = linepospredictions.strip()
        if lineud:
            lineud = lineud.split("\t")
            linepospredictions = linepospredictions.split("\t")
            form = lineud[1]
            pos = linepospredictions[2][2:-1] #b'ADP' --> ADP
            lemma = lemmatizer.lemmatize(form, pos)
            senselabel = lineud[4]
            tokidx = lineud[0]
            print("\t".join([tokidx,form,lemma,pos,senselabel]))
        else:
            print("")

if __name__ == "__main__":
    main()
