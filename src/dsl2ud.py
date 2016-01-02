__author__ = 'alonso'

"""
<s id="2000-11-48">
hold	Hold	_	holde	V	VM:----:--:----
øje	øje	_	øje	N	NC:siun:--:----
med	med	_	med	T	T-:----:--:----
ørsted	Ørsted	!$	Ørsted	N	NP:siu#:--:----
</s>
"""
import argparse

def main():
    parser = argparse.ArgumentParser(description="DSL-CQP format to Ud-internal")
    parser.add_argument("--infile",   metavar="FILE", help="input UD format file",default ="../data/pos/pred.out")
    args = parser.parse_args()

    for linecqp in open(args.infile).readlines():
        linecqp =  linecqp.strip()
        if linecqp:
            if linecqp == "</s>":
                print("")
            elif linecqp.startswith("<s id="):
                print("1\t"+linecqp+"\t_\t_\t_")
                print()
                counter = 0
            else:
                counter+=1
                lowercaseform, actualform, punctuation, lemma, cpos, langpos = linecqp.split("\t")
                print(str(counter)+"\t"+actualform+"\t_\t_\t_")
                #punctout = punctuation.replace("_","")
                #for c in punctout:
                #    print(c)


if __name__ == "__main__":
    main()
