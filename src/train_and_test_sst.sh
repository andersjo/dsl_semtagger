#mkdir preprocessed
trainsstcorpus="../data/sst/semdax_sst.train.tsv.poslemma"
testsstcorpus="../data/sst/semdax_sst.test.tsv.poslemma"
modelname="../data/sst/da_traintest_sst_mdl"


python extract_features.py --infile $trainsstcorpus --labels supersense > $trainsstcorpus.fss
python extract_features.py --infile $testsstcorpus --labels supersense > $testsstcorpus.fss

rungsted --train $trainsstcorpus.fss --final-model $modelname --test $testsstcorpus.fss --predictions $testsstcorpus.sstpred

