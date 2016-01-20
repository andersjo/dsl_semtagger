#mkdir preprocessed
trainsstcorpus="../data/sst/semdax_sst.train.tsv.poslemma"
testsstcorpus="../data/sst/semdax_sst.test.tsv.poslemma"
modelname="../data/sst/da_traintest_sst_mdl"


python extract_features.py --infile $trainsstcorpus --labels supersense > $trainsstcorpus.fss
python extract_features.py --infile $testsstcorpus --labels supersense --report > $testsstcorpus.fss 2> $testsstcorpus.rep

rungsted --train $trainsstcorpus.fss --final-model $modelname --test $testsstcorpus.fss --predictions $testsstcorpus.sstpred
python confmat_from_rugsted_pred.py --infile $testsstcorpus.sstpred > $testcorpus.eval

