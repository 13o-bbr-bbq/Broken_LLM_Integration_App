from langchain.chains import LLMChain
from langchain_experimental.pal_chain.base import PALChain

from .llm_models import create_chat_openai_model


# Create Shell chain.
def create_shell_chain(prompt_template, user_prompt):
    pal_chain = PALChain.from_math_prompt(llm=create_chat_openai_model(), verbose=True)
    return pal_chain.run(user_prompt)
