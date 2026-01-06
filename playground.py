import os
import logging
import asyncio
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_openai import ChatOpenAI
from langchain_core.prompts import SystemMessagePromptTemplate, PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from prompt import PROMPT_TEMPLATE

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    logger.error("OPENAI_API_KEY not found in environment variables.")

if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

# Configuration
MODEL_NAME = "gpt-5"
TEMPERATURE = 0


ARTICLE_TEXT = """
How Elon Musk Changed Course to Go All Out for Trump

The billionaire has poured nearly $120 million into a pro-Trump voting effort and used his social media platform, X, to spread misinformation, despite public statements he made in the past about political neutrality.
Two weeks after making a stunning $44 billion bid to buy Twitter in April 2022, Elon Musk began to lay out a vision for his ownership of the social network. The company’s management had become biased in favor of left-wing values, Mr. Musk argued, and he would stamp out political partisanship.

"""

PROMPT = SystemMessagePromptTemplate.from_template(PROMPT_TEMPLATE)

# Finaly reminder to follow the instructions (as shown in the langchain tutorial)
FINAL_TIP = HumanMessagePromptTemplate(
    prompt=PromptTemplate.from_template("""
Tip: Make sure to answer in the correct format and do not include any explanations. Use the given format to extract information from the following input: {input}
""")
)

chat_prompt = ChatPromptTemplate.from_messages([PROMPT, FINAL_TIP])

async def main():
    if not ARTICLE_TEXT.strip():
        logger.warning("ARTICLE_TEXT is empty. Please paste an article text in the script.")
        return

    logger.info("Initializing LLM and Transformer...")
    # Initialize LLM
    llm = ChatOpenAI(temperature=TEMPERATURE, model_name=MODEL_NAME)

    # Create transformer
    llm_transformer = LLMGraphTransformer(
        llm=llm,
        relationship_properties=["topic", "medium", "accusation_sentence"],
        strict_mode=True,
        prompt=chat_prompt
    )

    logger.info("Processing article text...")
    
    try:
        docs = [Document(page_content=ARTICLE_TEXT)]
        graph_docs = await llm_transformer.aconvert_to_graph_documents(docs)
        
        if graph_docs:
            logger.info(f"Found {len(graph_docs[0].relationships)} relationships:")
            for i, rel in enumerate(graph_docs[0].relationships, 1):
                print(f"\n--- Relationship {i} ---")
                print(f"Accuser: {rel.source.id} ({rel.source.type})")
                print(f"Accused: {rel.target.id} ({rel.target.type})")
                print(f"Type: {rel.type}")
                
                props = rel.__dict__.get('properties', {})
                print(f"Topic: {props.get('topic', '')}")
                print(f"Medium: {props.get('medium', '')}")
                print(f"Sentence: {props.get('accusation_sentence', '')}")
        else:
            logger.info("No relationships found.")
            
    except Exception as e:
        logger.error(f"Error processing text: {e}")

if __name__ == "__main__":
    asyncio.run(main())
