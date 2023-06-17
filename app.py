import streamlit as st
import shutil
import os
from getRepos import fetch_user_repositories, clone_repositories
from repoPreprocessing import repo_directory_to_gpt_input, all_contents_to_txt_file
from llama_index import SimpleDirectoryReader,GPTListIndex,GPTVectorStoreIndex,LLMPredictor,PromptHelper,ServiceContext,StorageContext,load_index_from_storage
import os
from langchain import OpenAI
from model import create_index, answerMe

os.environ['OPENAI_API_KEY'] = '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'

def url_to_predict(github_url):
    progress_text = st.empty()  # Placeholder for progress updates

    if os.path.isdir(os.path.join(os.getcwd(), 'AllRepositories')) == False:
        os.mkdir(os.path.join(os.getcwd(), 'AllRepositories'))
    else:
        shutil.rmtree(os.path.join(os.getcwd(), 'AllRepositories'), ignore_errors=True)
        os.mkdir(os.path.join(os.getcwd(), 'AllRepositories'))

    progress_text.text("Fetching user repositories...")
    clone_folder = os.path.join(os.getcwd(), 'AllRepositories')
    repositories = fetch_user_repositories(github_url)
    progress_text.text("Cloning repositories...")
    clone_repositories(repositories, clone_folder)
    progress_text.text("Processing repositories...")
    all_contents = repo_directory_to_gpt_input(os.path.join(os.getcwd(), 'AllRepositories'))
    all_contents_to_txt_file(all_contents)
    progress_text.text("Indexing the information collected from all the repositories. This might take some time...")
    docs, promptHelper, llmPredictor = create_index(os.path.join(os.getcwd(), 'data'))
    service_context = ServiceContext.from_defaults(llm_predictor=llmPredictor, prompt_helper=promptHelper)
    vectorIndex = GPTVectorStoreIndex.from_documents(documents=docs, service_context=service_context)
    vectorIndex.storage_context.persist(persist_dir='Store')

    question = """compare all the repositories based on the given parameters.
                Use the following parameters for judgement: ["Lines of Code (LOC)","Cyclomatic Complexity",
                "Code Coverage", "Code Smells", "Code Duplication", "Code Comment Ratio", "Code Complexity Metrics",
                "Code Dependency Analysis", "Code Performance Analysis", "Code Security Analysis"]
                Choose the repository which is most technically complex and give justification for your choice.
                Be confident in your choice, no need to second guess.
                Also add a link to the selected project at the end"""
    progress_text.text("Answering question...")
    response = answerMe(question)

    progress_text.text("Process completed!")  # Update progress text with completion message
    return response.response


# Streamlit app
def main():
    # Set Streamlit app title and description
    st.title("GitHub User Repository Analysis")
    st.write("Enter a GitHub user URL to retrieve information.")

    # User input: GitHub user URL
    github_url = st.text_input("GitHub User URL", "")

    # Process user input when button is clicked
    if st.button("Generate Information"):
        if github_url:
            # Call backend function to process the GitHub user URL
            output = url_to_predict(github_url)

            # Display the output on the frontend
            if output is not None:
                st.success("Information Generated:")
                st.write(output)
            else:
                st.error("Unable to fetch information. Please check the GitHub user URL.")
        else:
            st.warning("Please enter a valid GitHub user URL.")

# Run the Streamlit app
if __name__ == "__main__":
    main()