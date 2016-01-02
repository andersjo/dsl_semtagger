#!/usr/bin/env bash
infile=$1

tempfolder="./tmp"
tmpfile="$tempfolder/$$"
sstmodelname="../data/sst/da_full_sst_mdl"
posmodelname="../data/pos/da_pos_mdl"


if [ -d $tempfolder ];
then
   echo "temporal file in $tmpfile"
else
   mkdir $tempfolder
fi

python dsl2ud.py --infile $infile > $tmpfile.ud
python extract_features.py --infile "$tmpfile.ud" --labels pos > "$tmpfile.fpos"
rungsted --initial-model $posmodelname --test $tmpfile.fpos --predictions "$tmpfile.pospred"
python lemmatize_pos_predictions.py --pospredictions "$tmpfile.pospred" --udfile "$tmpfile.ud" > "$tmpfile.poslemma"
python extract_features.py --infile "$tmpfile.poslemma" --labels supersense > "$tmpfile.fss"
rungsted --initial-model $sstmodelname --test "$tmpfile.fss" --predictions "$tmpfile.sspred"
python join_sst_predictions_and_dslcqp.py --infile_sstpred "$tmpfile.sspred" --infile_ud "$tmpfile.ud" --infile_cqp $infile  > "$infile.sstpred.cqp"

rm "$tmpfile.*"