from langchain.agents import initialize_agent
from langchain.llms import OpenAI
from tools.google_maps_tool import GoogleMapsTool

class SearchAgent:
    def __init__(self, maps_api_key: str):
        self.llm = OpenAI(temperature=0)
        self.maps_tool = GoogleMapsTool(maps_api_key).as_tool()
        self.agent = initialize_agent(
            tools=[self.maps_tool],
            llm=self.llm,
            agent="zero-shot-react-description",
            verbose=True
        )

    def run(self, query: str):
        return self.agent.run(query)
