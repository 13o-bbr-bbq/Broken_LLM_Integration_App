from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from .llm_models import create_openai_model
from .llm_prompt_templates import *
from .llm_db_chain import create_db_chain


# Ask questions to the LLM using Database.
def p2sql_injection_lv1(question: str) -> str:
    try:
        prompt = p2sql_injection_lv1_template.format(
            top_k=5,
            table_info="users",
            question=question
        )
        answer = create_db_chain().run(prompt)
        return ','.join(answer) if isinstance(answer, list) else str(answer)
    except Exception as e:
        return f"Error in ask_question_db: {', '.join(map(str, e.args))}"


# Ask questions to the LLM using Database.
def p2sql_injection_lv2(question: str) -> str:
    try:
        prompt = p2sql_injection_lv2_template.format(
            top_k=5,
            table_info="users",
            question=question
        )
        answer = create_db_chain().run(prompt)
        return ','.join(answer) if isinstance(answer, list) else str(answer)
    except Exception as e:
        return f"Error: {', '.join(map(str, e.args))}"


# Ask questions to the LLM.
def prompt_leaking_lv1(question: str) -> str:
    prompt = PromptTemplate(template=prompt_leaking_lv1_template, input_variables=["question"])
    llm_chain = LLMChain(prompt=prompt, llm=create_openai_model())
    answer = llm_chain.run(question)
    return answer
