#mkdir preprocessed
trainsstcorpus="../data/sst/semdax_sst.train.tsv.poslemma"
modelname="../data/sst/da_full_sst_mdl"

python extract_features.py --infile $trainsstcorpus --labels supersense > $trainsstcorpus.fss

rungsted --train $trainsstcorpus.fss --final-model $modelname

