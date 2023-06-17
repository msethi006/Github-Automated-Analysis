import os

def get_python_files_inside_a_directory(directory):
    python_files = []
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                python_files.append(file_path)
    return python_files

def prepare_file_for_gpt(file_path):
    # Takes a python file as input and return list of strings for that file
    
    max_token_limit = 4050

    # Get the relative path of the file with respect to the project directory
    relative_path = os.path.relpath(file_path, os.getcwd())

    # Read the file content
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        content = file.read()

    # Split the content into tokens
    tokens = content.split()

    # Check if content exceeds the maximum token limit
    if len(tokens) <= max_token_limit:
        # Append the relative path and add markers
        prepared_content = f"<FilePathStart> {relative_path} <FilePathEnd>\n<FileStart>\n{content}\n<FileEnd>"
        return [prepared_content]
    else:
        # Split the content into multiple parts
        prepared_contents = []
        num_parts = len(tokens) // max_token_limit + 1

        for i in range(num_parts):
            start = i * max_token_limit
            end = (i + 1) * max_token_limit
            part_tokens = tokens[start:end]
            part_content = ' '.join(part_tokens)

            # Append the relative path to the first part
            if i == 0:
                prepared_content = f"<FilePathStart> {relative_path} <FilePathEnd>\n<FileStart>\n{part_content}"
            else:
                prepared_content = part_content

            prepared_contents.append(prepared_content)

        # Add <FileEnd> marker to the last part
        prepared_contents[-1] += "\n<FileEnd>"

        return prepared_contents


def project_directory_to_gpt_input(project_path):
    
    # Takes path of the project repository and processes all the python files into a list of strings
    all_files_contents = []
    project_files = get_python_files_inside_a_directory(project_path)
    for file_path in project_files:
        file_contents = prepare_file_for_gpt(file_path)
        all_files_contents.extend(file_contents)
    
    return all_files_contents

def repo_directory_to_gpt_input(repo_path):

    # Takes all the repositorie inside a director and convert to GPT-input format

    all_contents = []
    project_names = os.listdir(os.path.join(os.getcwd(), 'AllRepositories'))
    for project_name in project_names:
        
        project_path = os.path.join(repo_path,project_name)
        project_content = project_directory_to_gpt_input(project_path)
        all_contents.extend(project_content)
    return all_contents

def all_contents_to_txt_file(all_contents):
    current_dir = os.getcwd()
    if os.path.isdir(os.path.join(os.getcwd(), 'data')) == False:
        os.mkdir(os.path.join(current_dir, 'data'))
    
    file_path = os.path.join(os.path.join(current_dir, 'data'),'file.txt')
    with open(file_path, 'w') as file:
        for line in all_contents:
            file.write(line + '\n')

if __name__ == '__main__':
     all_contents = repo_directory_to_gpt_input(os.path.join(os.getcwd(), 'AllRepositories'))
     all_contents_to_txt_file(all_contents)