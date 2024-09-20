#!/bin/bash

# copy to /usr/local/bin
# runner_script.sh venv https://github.com/gimlin0610/python-fritzhome.git /srv/python-fritzhome "-f fritz.box -u api -p Rapi2018 writelongterm"
# crontab -e
# */15 * * * * /usr/local/bin/runner_script.sh /srv/python-fritzhome/venv https://github.com/gimlin0610/python-fritzhome.git /srv/python-fritzhome "-f fritz.box -u api -p Rapi2018 writelongterm"
export INFLUXDB_TOKEN=VrmRq6LReMXLUUASYblbNidcNyR-_pywXJAeYqO1FvzLsd17zYF4pBjSuMXVNqi_od89MMUgpe00_sA8h6xy4A==
# Function to handle errors and provide informative messages
error_exit() {
  local code="${1:-1}"  # Default exit code is 1
  local message="${2:-"An error occurred."}"
  echo "Error: $message" >&2
  exit "$code"
}

# Validate the presence of required arguments
if [[ $# -lt 4 ]]; then
  error_exit 2 "Usage: $0 <venv_dir> <github_repo> <working_dir> <script_args>"
fi

# Extract arguments
venv_dir="$1"
github_repo="$2" # https://github.com/gimlin0610/python-fritzhome.git
working_dir="$3"
script_args="$4"

# Check if virtual environment directory exists
if [[ ! -d "$venv_dir" ]]; then
  error_exit 3 "Virtual environment directory '$venv_dir' does not exist."
fi

# Source the virtual environment activation script (adjust based on your tool)
source "$venv_dir/bin/activate"  # Example for venv

if [[ $? -ne 0 ]]; then
  error_exit 4 "Failed to activate virtual environment. Check activation script path."
fi

# Navigate to the working directory
cd "$working_dir" || error_exit 5 "Failed to change directory to '$working_dir'."

# Update the Python script from GitHub using a robust approach (adapt as needed)
# This example uses Git directly. Consider tools like pipenv or poetry if necessary
git fetch --all  # Fetch all branches and tags
git reset --hard origin/dev_branch  # Ensure you're on the latest master branch (modify as needed)

# Alternatively, for more complex update logic with pip:
# pip install --upgrade -U -r requirements.txt

# Execute the Python script with parameters
python3 "pyfritzhome/cli.py" $script_args

# Deactivate the virtual environment (adjust based on your tool)
deactivate

echo "Script execution completed."

