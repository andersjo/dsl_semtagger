import argparse
from collections import defaultdict



def getPredDict(udfile,sstpredictions):
    D = defaultdict(list)
    sentence_id_tag = ""
    for lineud, linesstpredictions in zip(open(udfile).readlines(),open(sstpredictions).readlines()):
        lineud = lineud.strip()
        linesstpredictions = linesstpredictions.strip()

        if lineud:
            lineud = lineud.split("\t")
            linepospredictions = linesstpredictions.split("\t")
            form = lineud[1]
            pred_sst = linepospredictions[2][2:-1] #b'noun.person' --> noun.person
            if form.startswith("<s id=") and form.endswith(">"):
                sentence_id_tag = form
            else:
                D[sentence_id_tag].append(pred_sst)
    return D

def main():
    parser = argparse.ArgumentParser(description="SST predictions to DSL-CQP format")
    parser.add_argument("--infile_sstpred",   metavar="FILE", help="SST predictions")
    parser.add_argument("--infile_ud",   metavar="FILE", help="preprocessed UD file")
    parser.add_argument("--infile_cqp",   metavar="FILE", help="original CQP file")
    args = parser.parse_args()

    pred_sst_dict = getPredDict(args.infile_ud, args.infile_sstpred)
    print(list(pred_sst_dict.keys()))
    current_sentence_id = ""
    sentenceoffset = 0
    for line in open(args.infile_cqp).readlines():
        line = line.strip()
        if line:
            if line == "</s>":
                print(line)
            elif line.startswith("<s id=") and line.endswith(">"):
                current_sentence_id = line
                sentenceoffset = 0
                print(line)
            else:
                print(line+"\t"+pred_sst_dict[current_sentence_id][sentenceoffset])
                sentenceoffset+=1

if __name__ == "__main__":
    main()
