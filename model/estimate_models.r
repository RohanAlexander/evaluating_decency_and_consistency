#### Preamble ####
# Purpose: Models for consistency and decency
# Author: Rohan Alexander
# Date: 29 March 2024
# Contact: rohan.alexander@utoronto.ca
# License: MIT
# Pre-requisites: Need to have run clean_data.R
# Any other information needed?


#### Workspace setup ####
# Not loading MASS because of the select conflict
library(tidyverse)
library(arrow)
library(rstanarm)


#### Read data ####
data <- read_parquet("data/cleaned/analysis_data.parquet")


### Model data ####
## Getting something working
# Use MASS while getting something working
consistency_model_MASS <-
    MASS::polr(factor(consistency_median) ~ Version + Prompt_n + Temperature + Role_n + Shot_n, data = data)

decency_model_MASS <-
    MASS::polr(factor(decency_median) ~ Version + Prompt_n + Temperature + Role_n + Shot_n, data = data)


## Proper
# Use rstanarm for what we report in the paper
consistency_model_rstanarm <-
    stan_polr(
        factor(consistency_median) ~ Version + Prompt_n + Temperature + Role_n + Shot_n,
        data = data,
        prior = R2(0.3, "mean"),
        seed = 853)

saveRDS(
  consistency_model_rstanarm,
  file = "model/consistency_model_rstanarm.rds"
)

decency_model_rstanarm <-
   stan_polr(
        factor(decency_median) ~ Version + Prompt_n + Temperature + Role_n + Shot_n,
        data = data,
        prior = R2(0.3, "mean"),
        seed = 853)

saveRDS(
  decency_model_rstanarm,
  file = "model/decency_model_rstanarm.rds"
)
