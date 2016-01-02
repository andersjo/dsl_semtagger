import argparse
def main():
    parser = argparse.ArgumentParser(description="Join rungsted input and original file in a 5-column input file for feature extraction")
    parser.add_argument("--infile",   metavar="FILE", help="input UD format file",default ="../data/sstannotated/semdax.all.tsv")
    args = parser.parse_args()
    for line in open(args.infile).readlines():
        line = line.strip()
        if not line:
            pass
            print()
        elif line.startswith("#"):
            pass
        else:
            a = line.split("\t")
            tokidx, form, label = a[0],a[1],a[2]
            tokidx = tokidx.split("-")[1]
            print("\t".join([tokidx,form,"_","_",label]))


if __name__ == "__main__":
    main()