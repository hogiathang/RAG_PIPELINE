import pydantic

class RAGSearchResult(pydantic.BaseModel):
    contexts : list[str]
    sources: list[str]
    