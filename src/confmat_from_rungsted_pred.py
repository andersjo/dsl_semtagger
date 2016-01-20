import argparse
from sklearn.metrics import classification_report


def cleanlabel(label):
    l = label[2:-1]
    if l.startswith("B-") or l.startswith("I-"):
        l = l[2:]
    return l
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--infile",   metavar="FILE", help="input UD format file",default ="../data/pos/pred.out")
    args = parser.parse_args()

    y = []
    y_pred = []


    for line in open(args.infile).readlines():
        line = line.strip()
        if line:
            line = line.split("\t")
            goldlabel = cleanlabel(line[1]) #b'b-noun.person' --> ADP
            predicted = cleanlabel(line[2]) #b'ADP' --> ADP
            y.append(goldlabel)
            y_pred.append(predicted)

    print(y_pred)

    print(classification_report(y,y_pred))


if __name__ == "__main__":
    main()
