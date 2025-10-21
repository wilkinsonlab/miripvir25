# Diversity correlations
# 

library(lme4)
library(MASS)
# ------------------------------------------------------------  SITE LEVEL 
data <- read.csv("output/diversity.all.csv", sep=";")

# Initialize a data frame to store the results
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

# Function to extract model attributes and append to results
extract_model_info_glm <- function(model, model_name) {
    m <- summary(model)
    loglik <- m$twologlik / 2
    for (i in 2:nrow(m$coefficients)) {
        results <<- rbind(results, data.frame(
            Model = paste(model_name, rownames(m$coefficients)[i], sep = " - "),
            Estimate = m$coefficients[i, "Estimate"],
            StdError = m$coefficients[i, "Std. Error"],
            ZValue = m$coefficients[i, "z value"],
            PValue = m$coefficients[i, "Pr(>|z|)"],
            DFres = m$df.residual,
            LogLik = loglik
        ))
    }
}

extract_model_info_glmer <- function(model, model_name) {
  m <- summary(model)
  loglik <- as.numeric(m$logLik)
  for (i in 2:nrow(m$coefficients)) {
    results <<- rbind(results, data.frame(
      Model = paste(model_name, rownames(m$coefficients)[i], sep = " - "),
      Estimate = m$coefficients[i, "Estimate"],
      StdError = m$coefficients[i, "Std. Error"],
      ZValue = m$coefficients[i, "z value"],
      PValue = m$coefficients[i, "Pr(>|z|)"],
      DFres = attr(logLik(model), "df"),
      LogLik = loglik
    ))
  }
}

# Model 1
model1 <- glm.nb(species_richness_bact ~ species_richness_vir, data = data)
extract_model_info_glm(model1, "Model 1")

# Model 2
model2 <- glm.nb(species_richness_bact ~ species_richness_plant, data = data)
extract_model_info_glm(model2, "Model 2")

# Model 3
model3 <- glm.nb(species_richness_bact ~ species_richness_plant + species_richness_vir, data = data)
extract_model_info_glm(model3, "Model 3")

# Model 4
model4 <- glmer.nb(species_richness_bact ~ species_richness_vir + (1|habitat), data = data)
extract_model_info_glmer(model4, "Model 4")

# Model 5
model5 <- glmer.nb(species_richness_bact ~ species_richness_plant + (1|habitat), data = data)
extract_model_info_glmer(model5, "Model 5")

# Model 6
model6 <- glmer.nb(species_richness_bact ~ species_richness_plant + species_richness_vir + (1|habitat), data = data)
extract_model_info_glmer(model6, "Model 6")

# Model 7
model7 <- glmer.nb(species_richness_bact ~ species_richness_vir + (1|disturbed), data = data)
extract_model_info_glmer(model7, "Model 7")

# Model 8
model8 <- glmer.nb(species_richness_bact ~ species_richness_plant + (1|disturbed), data = data)
extract_model_info_glmer(model8, "Model 8")

# Model 9
model9 <- glmer.nb(species_richness_bact ~ species_richness_plant + species_richness_vir + (1|disturbed), data = data)
extract_model_info_glmer(model9, "Model 9")

# Print the results table
print(results)

write.csv(results, "output/regression.site-level.csv")


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