#!/bin/bash

#default parameter
default_genomes_dir="./genomes/"
default_out_dir="./hmmer_result/"
profile_dir="./config/hmmer_marker_gene_profile"

#Usage
print_usage() {
  echo "Usage: $0 [-h|--help] [-i|--input] [-o|--output]"
  echo ""
  echo "#please use this script to perform Data-preprocessing---HMMER"
  echo "  -h, --help		 show this help message and exit"
  echo "  -i PATH, --input PATH  indicate the absolute path/directory of genomes, default is './genomes/'"
  echo "  -o PATH, --output PATH indicate the file to store the hmmer results, default is './hmmer_result/'"
}

#parameters--in
options=$(getopt -o i:o:h --long input:,output:,help -- "$@")
[ $? -ne 0 ] && { echo “Try ‘$0 --help’ for more information.”; exit 1; }
eval set -- "$options"

while true; do
  case $1 in
    -i | --input) shift; genomes_dir=$1 ; shift ;;
    -o | --output) shift; out_dir=$1 ; shift ;;
    -h | --help) print_usage; exit 0 ;;
    --) shift ; break ;;
    *) echo "Invalid option: $1"; exit 1 ;;
  esac
done

#parameters--set default
if [ -z "$genomes_dir" ]; then
   genomes_dir=$default_genomes_dir
fi

if [ -z "$out_dir" ]; then
   out_dir=$default_out_dir
fi
#hmmer
echo "Performing HMMER"
int=1
for i in `ls $genomes_dir`; do
  echo "Genome: $int"
  echo $i

  genome_hmmer_out_dir=${i%_*}
  mkdir $out_dir/$genome_hmmer_out_dir

  for p in `ls $profile_dir`; do
    hmmer_out_name=`basename ${p##*_} .hmm`
    hmmsearch $profile_dir/$p $genomes_dir/$i > $out_dir/$genome_hmmer_out_dir/${hmmer_out_name}.out
  done

  ((int+=1))
done

#Summary
echo "Summarizing HMMER result"
Rscript "./script/hmmer_summary.R" $out_dir
echo "Finished!"


