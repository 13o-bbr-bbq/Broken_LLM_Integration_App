from langchain.utilities.sql_database import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain

from .settings import settings
from .llm_models import *


# Create DB chain.
def create_db_chain():
    db = SQLDatabase.from_uri(settings.DB_DATABASE_URL)
    return SQLDatabaseChain.from_llm(
        llm=create_chat_openai_model(),
        db=db,
        verbose=True
    )

# Execute SQL query.
def run_sql_chain(query: str) -> str:
    db_chain = create_db_chain()
    return db_chain.run(query)
