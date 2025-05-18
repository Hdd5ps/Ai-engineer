import os
from urllib.request import urlopen, Request
import base64
from pathlib import Path

# Add references
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.inference.models import (
     SystemMessage,
     UserMessage,
     TextContentItem,
     ImageContentItem,
     ImageUrl,
)

def main(): 

    # Clear the console
    os.system('cls' if os.name=='nt' else 'clear')
        
    try: 
    
        # Get configuration settings 
        load_dotenv()
        project_connection = os.getenv("PROJECT_CONNECTION")
        model_deployment =  os.getenv("MODEL_DEPLOYMENT")



        # Initialize the project client
        project_client = AIProjectClient.from_connection_string(
             conn_str = project_connection,
             credential = DefaultAzureCredential()
        )

        

        # Get a chat client
        chat_client = project_client.inference.get_chat_completions_client(model = model_deployment)



        # Initialize prompts
        system_message = "You are an AI assistant in a grocery store that sells fruit."
        prompt = ""

        # Loop until the user types 'quit'
        while True:
            prompt = input("\nAsk a question about the image\n(or type 'quit' to exit)\n")
            if prompt.lower() == "quit":
                break
            elif len(prompt) == 0:
                    print("Please enter a question.\n")
            else:
                print("Getting a response ...\n")


                # Get a response to image input
                image_url = "https://github.com/MicrosoftLearning/mslearn-ai-vision/raw/refs/heads/main/Labfiles/08-gen-ai-vision/orange.jpeg"
                image_format = "jpeg"
                request = Request(image_url, headers=("User-Agent": "Mozilla/5.0"))
                image_data = base64.b64encode(urlopen(request).read()).decode("utf-8")
                data_url = f"data:image/{image_format};base64,{image_data}"

                response = chat_client.complete(
                     messages = [
                          SystemMessage(system_message),
                          UserMessage(content=[
                               TextContentItem(text=prompt),
                               ImageContentItem(image_url=ImageUrl(url=data_url))
                          ])
                     ]
                )
                print(response.choices[0].message.content)
                
    except Exception as ex:
        print(ex)


if __name__ == '__main__': 
    main()