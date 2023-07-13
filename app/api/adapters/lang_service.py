from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
import os


openai_api_key = os.getenv("OPENAI_API_KEY")
serpapi = os.getenv("SERPAPI_KEY")
wolf = os.getenv("WOLFRAM_ALPHA")

class LangService:
    def __init__(self):
        pass


    def test(self,query: str):
        
        llm = OpenAI(temperature=0)

        tools = load_tools(["serpapi","llm-math","wolfram-alpha"],llm=llm,serpapi_api_key=serpapi,
                                                                       wolfram_alpha_appid=wolf)

        agent = initialize_agent(tools,llm, agent="zero-shot-react-description",verbose=True)

        return agent.run(query)
