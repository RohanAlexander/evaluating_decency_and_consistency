# We want to read in some different options for temperatures and prompts from CSV files, and 
# then use the OpenAI API to generate some responses. We save the responses to a CSV file.


# Import packages
import csv
import os
import openai
import time
from dotenv import load_dotenv


# Load API key for OpenAI
load_dotenv()
# Fetch the API key from environment variable
openai_api_key = os.getenv('OPENAI_API_KEY')
# Check if the API key is available
if not openai_api_key:
    raise ValueError("OpenAI API key not found in the environment variables.")
# Use the API key for OpenAI
openai.api_key = openai_api_key


# Define a function to load a file into a list of strings separated by '---'
def load_file_into_list(file_path):
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()

        # Split the file contents using '---' as the delimiter
        prompts = file_contents.split('---')
        
        # Remove leading and trailing whitespace from each prompt
        # prompts = [prompt.strip() for prompt in prompts if prompt.strip()]
        
        return prompts
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{file_path}' not found.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

# Define a function to calculate the number of tokens used in an API response
def calculate_tokens_used(response):
    """
    Calculate the number of tokens used in an API response.

    Args:
        response (dict): The API response from OpenAI.

    Returns:
        int: The number of tokens used in the response.
    """
    return response['usage']['total_tokens']


# Load prompts, temperatures, roles, and shots from text files
# Set the folder path
# Change this as necessary
folder_path = "scripts/test_settings/"
# Create file paths using the folder path
prompts_file = f'{folder_path}prompts.txt'
temperatures_file = f'{folder_path}temperatures.txt'
roles_file = f'{folder_path}roles.txt'
shots_file = f'{folder_path}shots.txt'

prompts = load_file_into_list(prompts_file)
temperatures = load_file_into_list(temperatures_file)
roles = load_file_into_list(roles_file)
shots = load_file_into_list(shots_file)

# Constants
MODEL = "gpt-3.5-turbo"
MAX_TOKENS = 1024  # Limit the response to 1024 tokens
NUM_RESPONSES = 5  # Generate 5 responses
DELAY_BETWEEN_REQUESTS = 5  # Define the delay in seconds

# Create a list to store responses
all_responses = []

# Token count
total_tokens_used = 0

# Progress tracking
progress_file = 'progress.txt'


# Load the last processed prompt index from the progress file, or start from 0
try:
    with open(progress_file, 'r') as progress:
        last_processed_prompt_index = int(progress.read().strip())
except FileNotFoundError:
    last_processed_prompt_index = 0

# Bring it all together and query the OpenAI API
# Loop through prompts starting from the last processed index
for i, prompt in enumerate(prompts):
    if i < last_processed_prompt_index:
        continue  # Skip already processed prompts

    # Loop through temperatures
    for temp_str in temperatures:
        this_temperature = float(temp_str)
        
        # Loop through roles
        for role in roles:
            # Loop through shots
            for shot in shots:
                this_prompt = shot + prompt
                
                try:
                    # Make API request for each combination of prompt, this_temperature, role, and shot
                    response = openai.ChatCompletion.create(
                        model=MODEL,
                        messages=[
                            {"role": "system", "content": role},
                            {"role": "user", "content": this_prompt},
                        ],
                        temperature=this_temperature,
                        max_tokens=MAX_TOKENS,
                        n=NUM_RESPONSES,
                    )

                    # Calculate tokens used for this API call
                    tokens_used = calculate_tokens_used(response)
                    total_tokens_used += tokens_used

                    print(f"Processing: "
                          f"Prompt {prompt}, "
                          f"Temperature {this_temperature}, "
                          f"Role {role}, "
                          f"Shot {shot}, "
                          f"Tokens used: {tokens_used}")

                    # Extract responses and add them to the list
                    responses = [choice['message']['content'] for choice in response['choices']]

                    # Append the prompt, this_temperature, role, shot, and responses to the list
                    all_responses.append([prompt, this_temperature, role, shot] + [tokens_used] + responses)

                except openai.error.OpenAIError as e:
                    print(f"API Error: {str(e)}")

                # Save progress after each prompt is processed
                with open(progress_file, 'w') as progress:
                    progress.write(str(i + 1))  # Write the next prompt index

                # Add a delay between requests
                time.sleep(DELAY_BETWEEN_REQUESTS)


# Print total tokens used
print(f"Total Tokens Used: {total_tokens_used}")

# Write responses to a structured CSV file
output_csv_file = 'structured_responses.csv'
with open(output_csv_file, 'w', newline = '') as file:
    writer = csv.writer(file)
    
    # Write header row with variable names
    header = ['Prompt', 'Temperature', 'Role', 'Shot', 'Tokens used', 'Response 1', 'Response 2', 'Response 3', 'Response 4', 'Response 5']
    writer.writerow(header)
    
    # Write data rows
    writer.writerows(all_responses)
