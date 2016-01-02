#!/usr/bin/env bash
wget https://www.dropbox.com/s/goiw9sd5ilvcaca/da.clarindk.embd?dl=0 -O ../data/res/da.clarindk.embd
bash train_full_sst.sh
bash tag_dsl_cqp.sh ../data/samples/0008.txt