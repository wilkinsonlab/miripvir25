

# # Cooccurrence network properties

# ## Summary
# this script aims to enable the study of the network properties of the bipartite
# cooccurrence matrix taking place between virus-bacteria.


library(bipartite)

u <- read.csv("scratch/adjmat.cooccurrence-virus-bacteria.csv", header = TRUE, row.names = 1, sep=";")
features =  c("NODF", "connectance", "modularity")
observed <- networklevel(u, index = features)

nulls <- nullmodel(web=u, N=1000, method="r2d")
null_results <- sapply(nulls, function(x) networklevel(x, index=features))