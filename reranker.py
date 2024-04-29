#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import uvicorn
from fastapi import FastAPI, Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from BCEmbedding import RerankerModel
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()
security = HTTPBearer()
env_bearer_token = 'BCEEEEEEEEEEEE'

class QADocs(BaseModel):
    query: Optional[str]
    documents: Optional[List[str]]


class Singleton(type):
    def __call__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class ReRanker(metaclass=Singleton):
    def __init__(self):
        self.reranker = RerankerModel(model_name_or_path="/Users/helingfeng/.cache/modelscope/hub/maidalun/bce-reranker-base_v1", use_fp16=False)

    def compute_score(self, pairs: List[List[str]]):
        if len(pairs) > 0:
            result = self.reranker.compute_score(pairs, normalize=True)
            if isinstance(result, float):
                result = [result]
            return result
        else:
            return None

class Chat(object):
    def __init__(self):
        self.reranker = ReRanker()

    def fit_query_answer_rerank(self, query_docs: QADocs) -> List:
        if query_docs is None or len(query_docs.documents) == 0:
            return []

        pair = [[query_docs.query, doc] for doc in query_docs.documents]
        scores = self.reranker.compute_score(pair)

        new_docs = []
        for index, score in enumerate(scores):
            new_docs.append({"index": index, "text": query_docs.documents[index], "score": score})
        results = [{"index": documents["index"], "relevance_score": documents["score"]} for documents in list(sorted(new_docs, key=lambda x: x["score"], reverse=True))]
        return results

@app.post('/v1/rerank')
async def handle_post_request(docs: QADocs, credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if env_bearer_token is not None and token != env_bearer_token:
        raise HTTPException(status_code=401, detail="Invalid token")
    chat = Chat()
    try:
        results = chat.fit_query_answer_rerank(docs)
        return {"results": results}
    except Exception as e:
        print(f"报错：\n{e}")
        return {"error": "重排出错"}

if __name__ == "__main__":
    token = os.getenv("ACCESS_TOKEN")
    if token is not None:
        env_bearer_token = token
    try:
        uvicorn.run(app, host='0.0.0.0', port=6006)
    except Exception as e:
        print(f"API启动失败！\n报错：\n{e}")
