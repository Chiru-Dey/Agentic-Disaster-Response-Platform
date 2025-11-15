# system1_manager/agents/inventory_agent.py

from google.adk.agents import LlmAgent
# In a real implementation, you would use:
# from google.adk.tools.bigquery import BigQueryToolset, BigQueryCredentialsConfig, BigQueryToolConfig, WriteMode
# For this capstone, we will define a placeholder tool.

# Placeholder for BigQueryToolset
# In a real scenario, this would connect to a BigQuery database.
class PlaceholderBigQueryToolset:
    def __init__(self):
        self.name = "PlaceholderBigQueryTool"
        self.description = "A placeholder tool for BigQuery to check inventory. Responds with dummy data."

    def get_stock(self, resource: str) -> str:
        """Checks the stock level of a given resource."""
        dummy_stock = {"water": 1000, "food": 500, "medical": 200}
        stock_level = dummy_stock.get(resource.lower(), 0)
        return f"Stock level for {resource}: {stock_level} units."

inventory_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="InventoryAgent",
    description="Manages and queries resource inventory levels (food, water, medical).",
    instruction="You are an inventory specialist. Based on the user's request, check for resource availability using your tools and provide a summary.",
    tools=[PlaceholderBigQueryToolset()],
    output_key="inventory_research"
)