import asyncio
from fastapi import HTTPException
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

from .llm_models import create_openai_model
from .llm_prompt_templates import vulnerable_template
from .settings import settings


# Ask questions to the LLM using Database.
def ask_question_db(question: str) -> str:
    try:
        prompt = vulnerable_template.format(
            top_k=5,
            table_info="users",
            question=question
        )
        db = SQLDatabase.from_uri(settings.DB_DATABASE_URL)
        db_chain = SQLDatabaseChain.from_llm(
            llm=create_openai_model(),
            db=db,
            verbose=True
        )
        answer = db_chain.run(prompt)
        return ','.join(answer) if isinstance(answer, list) else str(answer)
    except Exception as e:
        print(e.args)
        return "Error in ask_question_db"


# Ask questions to the LLM.
def ask_question(question: str) -> str:
    template = """
    Question: {question}\n
    Answer:
    """
    prompt = PromptTemplate(template=template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=create_openai_model())
    answer = llm_chain.run(question)
    return answer


# LLM agent.
def llm_controller(question: str) -> str:
    try:
        # Use DB access from LLM.
        answer = ask_question_db(question)
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
