import os
import sys

def get_env_vars(input_args=None):
  """
  Retrieves and categorizes environment variables, includes script arguments with 
  positions, lists files in /input, and lists files in the directory specified 
  by the PYENV_DIR environment variable.

  Args:
    input_args: A list of command-line arguments.

  Returns:
    A string containing categorized environment variables, formatted arguments, 
    the list of files in /input, and the list of files in PYENV_DIR.
  """
  system_vars = {}
  user_vars = {}

  for key, value in os.environ.items():
    if key in ('PATH', 'HOME', 'SHELL', 'TERM', 'USER', 'PWD', 
              'SYSTEMROOT', 'WINDIR', 'TEMP', 'TMP'): 
      system_vars[key] = value
    else:
      user_vars[key] = value

  output = "## System Environment Variables:\n"
  for key, value in system_vars.items():
    output += f"{key}={value}\n"

  output += "\n## User-Provided Environment Variables:\n"
  for key, value in user_vars.items():
    output += f"{key}={value}\n"

  if input_args:
    output += "\n## Script Arguments:\n"
    for i, arg in enumerate(input_args):
      output += f"Argument {i+1}: {arg}\n"

  # Add the list of files in /input
  try:
    input_files = os.listdir("/input")
    output += "\n## Files in /input:\n"
    for file in input_files:
      output += f"  - {file}\n"
  except FileNotFoundError:
    output += "\n## /input directory not found.\n"

  # Add the list of files in PYENV_DIR
  pyenv_dir = os.environ.get("PYENV_DIR")
  if pyenv_dir:
    try:
      pyenv_files = os.listdir(pyenv_dir)
      output += f"\n## Files in PYENV_DIR ({pyenv_dir}):\n"
      for file in pyenv_files:
        output += f"  - {file}\n"
    except FileNotFoundError:
      output += f"\n## PYENV_DIR directory not found ({pyenv_dir}).\n"
  else:
    output += "\n## PYENV_DIR environment variable not set.\n"

  return output

if __name__ == "__main__":
  input_args = sys.argv[1:]  # Get all arguments
  output_data = get_env_vars(input_args)

  output_dir = "/output"
  if not os.path.exists(output_dir):
    try:
      os.makedirs(output_dir)
      print(f"Created directory: {output_dir}")
    except Exception as e:
      print(f"Error creating directory: {e}")
      sys.exit(1) 

  try:
    with open(os.path.join(output_dir, "environment_data.txt"), "w") as f:
      f.write(output_data)
    print("Environment variables and input data saved to /output/environment_data.txt")
  except Exception as e:
    print(f"Error writing to file: {e}")