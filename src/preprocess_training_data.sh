#mkdir preprocessed
corpuspath="/Users/alonso/proj/semdax/supersenses/official_distribution"
tempsuffixes="ud fpos pospred"
for fn in `ls $corpuspath`
do
    outdir="../preprocessed/$fn"
    #mkdir $outdir
    currentfn="$corpuspath/$fn"
    for file in `ls $currentfn/*tsv`
    do
        tmpfile="$outdir/$(basename $file)"
        python webanno2ud.py --infile $file > "$tmpfile.ud"
        python extract_features.py --infile "$tmpfile.ud" --labels pos > "$tmpfile.fpos"
        rungsted --initial-model ../data/pos/da_pos_mdl --test $tmpfile.fpos --predictions "$tmpfile.pospred"
        python lemmatize_pos_predictions.py --pospredictions "$tmpfile.pospred" --udfile "$tmpfile.ud" > "$tmpfile.poslemma"
        for suffix in $tempsuffixes
        do
            rm "$tmpfile.$suffix"
        done

    done
done