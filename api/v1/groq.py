#!/usr/bin/env python
import typing

import pydantic
from fastapi import Header
from fastapi.routing import APIRouter
from openai import AsyncClient

groq_router = APIRouter()


class ChatArgs(pydantic.BaseModel):
    model: str
    messages: typing.List[typing.Dict[str, str]]


@groq_router.post("/chat/completions")
async def groq_api(args: ChatArgs, authorization: str = Header(...)):
    api_key = authorization.split(" ")[1]
    client = AsyncClient(base_url="https://api.groq.com/openai/v1",
                         api_key=api_key)
    return await client.chat.completions.create(
        model=args.model,
        messages=args.messages,
    )

supported_models = [
    "llama3-8b-8192",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
]

groq_unspported_fields = [
    "logprobs",
    "logit_bias",
    "top_logprobs",
    "functions",
    "function_call",
]


# @groq_router.get("/models")
# async def get_models():
#     return ModelsResponse(
#         object="list",
#         data=[
#             Datum(
#                 id=model,
#                 object="model",
#                 created=int(time.time()),
#                 owned_by="groq",
#             )
#             for model in supported_models
#         ],
#     )


# @groq_router.post("/chat/completions")
# async def chat_completions(
#     chat: ChatCompletions,
#     authorization: Annotated[str | None, Header()],
# ):
#     client = Groq(
#         api_key=authorization.removeprefix("Bearer "),
#     )
#     chat_params = chat.model_dump()
#     # remove unsupported fields
#     for field in groq_unspported_fields:
#         chat_params.pop(field, None)

#     chat_params["n"] = 1
#     chat_completion = client.chat.completions.create(**chat_params)
#     if not chat.stream:
#         return chat_completion

#     def chat_stream():
#         for response in chat_completion:
#             yield response.model_dump_json()

#     return EventSourceResponse(chat_stream())