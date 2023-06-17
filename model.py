from llama_index import SimpleDirectoryReader,GPTListIndex,GPTVectorStoreIndex,LLMPredictor,PromptHelper,ServiceContext,StorageContext,load_index_from_storage
import os
from langchain import OpenAI
os.environ['OPENAI_API_KEY'] = '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'

def create_index(path):
    max_input = 4096
    tokens = 200
    chunk_size = 1000 #for LLM, we need to define chunk size
    max_chunk_overlap = 0
    
    #define prompt
    promptHelper = PromptHelper(max_input,tokens,max_chunk_overlap,chunk_size_limit=chunk_size)
    
    #define LLM — there could be many models we can use, but in this example, let’s go with OpenAI model
    llmPredictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="gpt-3.5-turbo",max_tokens=tokens))
    
    #load data — it will take all the .txtx files, if there are more than 1
    docs = SimpleDirectoryReader(path).load_data()
    return docs,promptHelper,llmPredictor

def answerMe(question):
    storage_context = StorageContext.from_defaults(persist_dir = 'Store')
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return response

if __name__ == '__main__':
    docs,promptHelper,llmPredictor = create_index(os.path.join(os.getcwd(), 'data'))
    #create vector index
    service_context = ServiceContext.from_defaults(llm_predictor=llmPredictor,prompt_helper=promptHelper)
        
    vectorIndex = GPTVectorStoreIndex.from_documents(documents=docs,service_context=service_context)
    vectorIndex.storage_context.persist(persist_dir = 'Store')

    question = """compare all the repositories based on the given parameters.
                Use the following paranter for judgement : [ "Lines of Code (LOC)","Cyclomatic Complexity",
                "Code Coverage", "Code Smells", "Code Duplication", "Code Comment Ratio", "Code Complexity Metrics", 
                "Code Dependency Analysis", "Code Performance Analysis", "Code Security Analysis" ]
                Choose the repository which is most technically complex an give justification for you choice.
                Be confident in you choice, no need to second guess.
                Also add a link to the project selected at the end"""
    response =  answerMe(question)
    print(response.response)