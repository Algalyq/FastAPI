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

        return query
        # llm = OpenAI(api_key=openai_api_key, model='gpt-3.5-turbo',temperature=0)

        # tools = load_tools(["serpapi","llm-math","wolfram-alpha"],llm=llm,serpapi_api_key=serpapi,
        #                                                                wolfram_alpha_appid=wolf)

        # agent = initialize_agent(tools,llm, agent="zero-shot-react-description",verbose=True)

        # self.conversation.append({"role": "user", "content": query})

        # # Append additional content to the conversation history
        # self.conversation.append({"role": "assistant", "content": "This is an additional message from the assistant."})

        # # Append the conversation history to the messages for the agent
        # messages = self.conversation

        # # Generate a response from the agent
        # response = agent.run(messages)

        # # Extract and return the agent's reply
        # reply = response['replies'][-1]
        # return reply


        # return agent.run(query)
