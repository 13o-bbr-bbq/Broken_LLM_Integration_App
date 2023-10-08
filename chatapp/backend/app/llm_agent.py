import asyncio
from fastapi import HTTPException
from langchain import PromptTemplate, LLMChain
from langchain.llms import OpenAI


def ask_question(question: str) -> str:
    llm = OpenAI(
        openai_api_key='Please indicate the Your OpenAI API Key',
        model_name="gpt-3.5-turbo-0613",
        max_tokens=256,
        temperature=0.9,
        top_p=0.95
    )
    template = """Question: {question}

    Answer:"""

    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    try:
        answer = asyncio.wait_for(llm_chain.run(question), timeout=10)
        return answer
    except asyncio.TimeoutError as e:
        print(e)
        raise HTTPException(status_code=408, detail="Request timed out")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
