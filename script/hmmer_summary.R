#! /usr/bin/env Rscript
#parameters
args <- commandArgs(trailingOnly = TRUE)

#hmmer_result
hmmer_result_path <- args[1]
hmmer_result_list <- list.files(hmmer_result_path)

marker_gene_set <- read.table("./config/marker_gene.list", quote="\"", comment.char="")
marker_gene_set <- marker_gene_set$V1

dir.create("./hmmer_result_summary/")

for (i in 1:length(hmmer_result_list)){
  cat("file:", i, hmmer_result_list[i], "\n")
  top_hit_result <- as.data.frame(matrix(data = 0, nrow = length(marker_gene_set), ncol = 2))
  rownames(top_hit_result) <- marker_gene_set
  colnames(top_hit_result) <- c("marker_gene", "target_sequence")
  top_hit_result$marker_gene <- marker_gene_set
  
  sgenome_hmmer_result_dir <- paste(hmmer_result_path, hmmer_result_list[i], sep="")
  sgenome_hmmer_result <- list.files(sgenome_hmmer_result_dir)
  for (j in 1:length(sgenome_hmmer_result)){
    smarker_gene_result_name <- sgenome_hmmer_result[j]
    hmmer_result <- read.csv(file = paste0(sgenome_hmmer_result_dir,"/",smarker_gene_result_name), header=F, sep="", skip = 12, nrows = 3)
    target_sequence_name <- hmmer_result[3,9]
    marker_gene_name <- sub('.out', '', smarker_gene_result_name)
    top_hit_result[marker_gene_name,"target_sequence"] <- target_sequence_name
  }
  new_dir <- paste("./hmmer_result_summary/",hmmer_result_list[i],sep="")
  dir.create(new_dir)
  write.table(top_hit_result, file = paste(new_dir, "/top_hit_result.txt", sep = ""),
              row.names = F, col.names = TRUE, sep = "\t", quote = F)
}
