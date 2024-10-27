from fastapi import FastAPI, HTTPException
from graph import app, GraphStateDict
from models import QueryRequest, QueryResponse
from uvicorn import run
from data_handler import load_documents_from_folder, create_chunks, embed_and_store


# FastAPI setup
fast_api = FastAPI()


@fast_api.post("/query", response_model=QueryResponse)
async def query_endpoint(request: QueryRequest):
    try:
        initial_state: GraphStateDict = {
            "query": request.query,
            "retrieved_data": [],
            "initial_response": "",
            "refinement": "",
            "chat_history": [],
            "output": "",
            "steps": [],
            "next": "",
        }

        final_state = app.invoke(initial_state)

        return QueryResponse(response=final_state["output"], steps=final_state["steps"])
    except Exception as e:
        print(f"error : {e}")
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {e}"
        )


# Load data to Chroma
# @fast_api.on_event("startup")
# async def startup_event():
# Load documents
#    documents = load_documents_from_folder("data")
# Split documents into chunks
#    chunks = create_chunks(documents)
# Embed and store chunks
#    embed_and_store(chunks)


if __name__ == "__main__":
    run(fast_api, host="0.0.0.0", port=8080)
