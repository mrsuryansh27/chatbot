# import os
# from dotenv import load_dotenv
# from openai import OpenAI
# from pinecone import Pinecone, ServerlessSpec, CloudProvider, AwsRegion

# # Load environment variables from .env
# load_dotenv()

# # Initialize OpenAI (Gemini/Deep Seek) client
# _openai = OpenAI(api_key=os.getenv("GEMINI_API_KEY"))

# # Initialize Pinecone client
# _pc = Pinecone(
#     api_key=os.getenv("PINECONE_API_KEY"),
#     environment=os.getenv("PINECONE_ENVIRONMENT")
# )
# index_name = os.getenv("PINECONE_INDEX")

# # Define serverless spec for AWS us-east-1
# spec = ServerlessSpec(
#     cloud=CloudProvider.AWS,
#     region=AwsRegion.US_EAST_1
# )

# # Create index if it doesn't exist
# existing_indexes = _pc.list_indexes().names()
# if index_name not in existing_indexes:
#     _pc.create_index(
#         name=index_name,
#         dimension=1536,
#         metric="cosine",
#         spec=spec
#     )

# # Reference the Pinecone index
# _index = _pc.Index(name=index_name)

# async def query_similar(site_id: str, text: str, top_k: int = 5):
#     """
#     Context retrieval stub — always returns empty.
#     """
#     return []
# app/vector_store.py
# Stubbed context retrieval: no external dependencies

def query_similar(site_id: str, text: str, top_k: int = 5):
    """
    Stub implementation that returns no context.
    Replace with actual embedding + vector DB calls when available.
    """
    return []
