# Cooccurrence analysis Bacteria-Virus - by library
# This script enables the calculation of virus-bacteria cooccurrences
library(cooccur)

coocurrence_data <- read.csv("scratch/adjmat.virusbact-library.csv", sep=';', row.names = 1)
coocurrence_analysis_results <- cooccur(coocurrence_data, type = "spp_site", thresh = TRUE, spp_names = TRUE)
write.csv(prob.table(coocurrence_analysis_results), "output/coocurrence.virusbact-bylibrary.csv", sep=';')