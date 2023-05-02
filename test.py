from dotenv import load_dotenv
from prompt_wrangler import PromptWrangler

load_dotenv()


pw = PromptWrangler(base_url="http://localhost:3002/api")
prompt = pw.prompt("test-workspace/test-json")

result = prompt.run(args={"input": "animal"})

# Get prediction
prediction = result.prediction

# Get Animal
animal = prediction.get("animal")
# Assert prediction exists
print(animal)
