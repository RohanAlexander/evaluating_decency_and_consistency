#### Preamble ####
# Purpose: Clean the ratings from the individual coders
# Author: Rohan Alexander
# Date: 29 March 2024
# Contact: rohan.alexander@utoronto.ca
# License: MIT
# Pre-requisites: -
# Any other information needed? -

#### Workspace setup ####
library(tidyverse)
library(arrow)


#### Clean data ####
data <- read_csv("data/raw/responses_with_human_coding.csv")

data <- 
  data |>
  mutate(Prompt_n = factor(Prompt_n, levels = c("Name", "Describe", "Simulate", "Example")),
         Temperature = factor(Temperature),
         Role_n = factor(Role_n, levels = c("Helpful", "Expert")),
         Shot_n = factor(Shot_n, levels = c("Zero", "One", "Few")),
         Version = factor(Version)
  )

data <- 
  data |>
  rowwise() |>
  mutate(
    consistency_median = median(c(consistency_coder_1, consistency_coder_2, consistency_coder_3), na.rm = TRUE),
    decency_median = median(c(decency_coder_1, decency_coder_2, decency_coder_3), na.rm = TRUE)) |> 
  ungroup()


#### Save data ####
write_parquet(data, "data/cleaned/analysis_data.parquet")

