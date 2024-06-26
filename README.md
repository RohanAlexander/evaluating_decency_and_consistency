# Evaluating the Decency and Consistency of Data Validation Tests Generated by LLMs

We investigated whether large language models (LLMs) can develop data validation tests. We considered 96 conditions each for both GPT-3.5 and GPT-4, examining different prompt scenarios, learning modes, temperature settings, and roles. The prompt scenarios were: 1) Asking for expectations, 2) Asking for expectations with a given context, 3) Asking for expectations after requesting a data simulation, and 4) Asking for expectations with a provided data sample. The learning modes were: 1) zero-shot, 2) one-shot, and 3) few-shot learning. We also tested four temperature settings: 0, 0.4, 0.6, and 1. And the two distinct roles were: 1) helpful assistant, 2) expert data scientist. To gauge consistency, every setup was tested five times. The LLM-generated responses were benchmarked against a gold standard data validation suite, created by an experienced data scientist knowledgeable about the data in question. We find there are considerable returns to the use of few-shot learning, and that the more explicit the data setting can be the better, to a point. The best LLM configurations complement, rather than substitute, the gold standard results. This study underscores the value LLMs can bring to the data cleaning and preparation stages of the data science workflow, but highlights that they need considerable evaluation by experienced analysts.

## File Structure

The repo is structured as:

- `data` contains the raw and cleaned data.
- `inputs` contains a sample of the donations dataset and the validation suite constructed by an experienced data scientist.
- `model` contains fitted models and the code to fit them.
- `paper` contains the files used to generate the paper, including the Quarto document and reference bibliography file, as well as the PDF of the paper.
- `scripts` contains the R scripts used to clean data and also Python code to interact with the OpenAI API.
