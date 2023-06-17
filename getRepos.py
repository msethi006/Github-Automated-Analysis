import requests
import os
from git import Repo
import shutil
from tqdm import tqdm

def fetch_user_repositories(github_url):
    # Extract the username from the GitHub URL
    username = github_url.split("/")[-1]

    # Make an initial GET request to fetch the user's repositories
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        repositories = response.json()
        
        # Check if there are additional pages
        while "next" in response.links:
            url = response.links["next"]["url"]
            response = requests.get(url)
            
            if response.status_code == 200:
                repositories.extend(response.json())
            else:
                print("Failed to fetch additional repositories.")
                break

        return repositories
    else:
        print("Failed to fetch repositories. Please check the GitHub URL or try again later.")
        return []
    
def clone_repositories(repositories, clone_folder):
    with tqdm(total=len(repositories), desc="Cloning Repositories", unit="repo") as pbar:
        for repository in repositories:
            repo_url = repository['clone_url']
            repo_name = repository['name']
            repo_path = os.path.join(clone_folder, repo_name)
            Repo.clone_from(repo_url, repo_path)
            pbar.update(1)

if __name__ == '__main__':
    if os.path.isdir(os.path.join(os.getcwd(), 'AllRepositories')) == False:
        os.mkdir(os.path.join(os.getcwd(), 'AllRepositories'))
    else:
        shutil.rmtree(os.path.join(os.getcwd(), 'AllRepositories'), ignore_errors=True)
        os.mkdir(os.path.join(os.getcwd(), 'AllRepositories'))
        
    clone_folder = os.path.join(os.getcwd(), 'AllRepositories')
    repositories = fetch_user_repositories('https://github.com/msethi006')
    clone_repositories(repositories, clone_folder)