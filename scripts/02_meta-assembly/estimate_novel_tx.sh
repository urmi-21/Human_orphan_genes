#!/bin/bash

#this script shows the commands used to run gffcompare to estimate number of novel transcripts in each tissue/tumor sample
#this was used to select top 200 samples in each tissue tumor for meta-assembly

for f in $(cat *_gtflist.txt); do gffcompare -r gencode.v33.annotation.gtf -o $(basename $f)  $f; done

for f in $(ls *tracking); do count=$(awk '$4!="="' $f | wc -l); echo "${f}: ${count}" >> novelcounts.yaml ; done