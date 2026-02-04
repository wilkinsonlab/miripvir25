# Diversity correlations
# 

library(lme4)
library(MASS)
library(lmtest)
# ------------------------------------------------------------  SITE LEVEL 
data <- read.csv("output/TableS3.csv", sep=";")
model_base <- glm.nb(species_richness_bact ~ species_richness_plant, data = data)


model_rhabitat <- glmer.nb(species_richness_bact ~ species_richness_plant + (1|habitat), data = data)
lrtest(model_base, model_rhabitat)
model_fdist <- glm.nb(species_richness_bact ~ species_richness_plant + disturbed, data = data)
lrtest(model_base, model_fdist)

data <- read.csv("output/TableS4.csv", sep=";")
model_base <- glm.nb(species_richness_bact ~ species_richness_plant, data = data)


# ------------------------------------------------------------  HABITAT LEVEL 
results <- data.frame(
  Model = character(),
  Estimate = numeric(),
  StdError = numeric(),
  ZValue = numeric(),
  PValue = numeric(),
  LogLik = numeric(),
  DFres = numeric(),
  stringsAsFactors = FALSE
)

data <- read.csv("output/diversity-by-habitat.all.csv", sep=";")
model_alpha <- glm.nb(species_richness_bact ~ species_richness_vir, data = data)
extract_model_info_glm(model_alpha, "Model 1")

model_beta <- glm.nb(species_richness_bact ~ species_richness_plant, data = data)
extract_model_info_glm(model_beta, "Model 2")

model_gamma <- glm.nb(species_richness_bact ~ species_richness_plant + species_richness_vir, data = data)
extract_model_info_glm(model_gamma, "Model 3")

write.csv(results, "output/regression.habitat-level.csv")