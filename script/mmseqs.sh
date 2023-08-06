#!/bin/bash

#default parameter
default_genomes_dir="./genomes/"
default_out_dir="./mmseqs_result/"
default_hmmer_result_summary_dir="./hmmer_result_summary/"
default_tmp_dir="./tmp"
mmseqs_marker_db_dir="./config/mmseqs_marker_gene_db/"

#Usage
print_usage() {
  echo "Usage: $0 [-h|--help] [-i|--input] [-s|--hsummary] [-t|--tmp] [-o|--output]"
  echo ""
  echo "#please use this script to perform Data-preprocessing---MMseqs2"
  echo "  -h, --help               show this help message and exit"
  echo "  -i PATH, --input PATH    indicate the absolute path/directory of genomes, default is './genomes/'"
  echo "  -s PATH, --hsummary PATH indicate the absolute path/directory of hmmer result summary, default is './hmmer_result_summary/'"
  echo "  -t PATH, --tmp PATH      indicate the file to store the temporary results, default is './tmp'"
  echo "  -o PATH, --output PATH   indicate the file to store the mmseqs results, default is './mmseqs_result/'"
}

#parameters--in
options=$(getopt -o i:o:s:t:h --long input:,output:,hsummary:,tmp:,help -- "$@")
[ $? -ne 0 ] && { echo “Try ‘$0 --help’ for more information.”; exit 1; }
eval set -- "$options"

while true; do
  case $1 in
    -i | --input) shift; genomes_dir=$1 ; shift ;;
    -o | --output) shift; out_dir=$1 ; shift ;;
    -s | --hsummary) shift; hmmer_result_summary_dir=$1; shift ;;
    -t | --tmp) shift; tmp_dir=$1; shift ;;
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

if [ -z "$hmmer_result_summary_dir" ]; then
   hmmer_result_summary_dir=$default_hmmer_result_summary_dir
fi

if [ -z "$tmp_dir" ]; then
   tmp_dir=$default_tmp_dir
fi

#split_genomes
split_genomes_dir="${tmp_dir}/split_genomes"
mkdir -p $split_genomes_dir
for f in `ls $genomes_dir`
do
  file_name=${f%_*}
  mkdir $split_genomes_dir/$file_name
  cat $genomes_dir/$f | awk -F "[ ]" '{print $1}' |  awk '/^>/&&NR>1{print "";}{ printf "%s",/^>/ ? $0" ":$0 }' | sed s/" "/\\n/ > $split_genomes_dir/$file_name/$f
  echo "" >> $split_genomes_dir/$file_name/$f
done

for f in `ls $hmmer_result_summary_dir`
do
  mkdir -p $out_dir/$f
  mkdir $split_genomes_dir/$f/mmseqs_tmp_dir
  
  prob="${hmmer_result_summary_dir}/${f}/top_hit_result.txt"
  marker_db_total=($(awk '{print $1}' $prob))
  query_seq_total=($(awk '{print $(NF)}' $prob))

  int=1
  while (( $int <= 120 ))
  do
    marker_dbid=${marker_db_total[$int]}
    query_seqid=${query_seq_total[$int]}
    result="${marker_dbid}___${query_seqid}.m8"
    if [ $marker_dbid == $query_seqid ]
    then
      echo 0 > $out_dir/$f/$result
    else
      grep -wA 1 $query_seqid $split_genomes_dir/$f/*.faa > $split_genomes_dir/$f/$query_seqid.seq
      mmseqs easy-search $split_genomes_dir/$f/$query_seqid.seq $mmseqs_marker_db_dir/$marker_dbid $out_dir/$f/$result $split_genomes_dir/$f/mmseqs_tmp_dir/$query_seqid \
                         --max-seqs 70000 --split-memory-limit 50G \
                         --alignment-mode 3 --threads 1  -s 7.5 --format-mode 4 \
                         --format-output "query,target,fident,evalue,bits"
    fi
    ((int+=1))
    done
    echo "*****************************************$f, done********************************************************"
done


	

























