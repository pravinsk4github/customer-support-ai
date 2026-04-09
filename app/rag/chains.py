from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from app.rag.prompts import SUPPORT_SYSTEM_PROMPT

def build_support_chain(llm):
    '''
    This chain expects:
    * context
    * history
    * question
    '''
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SUPPORT_SYSTEM_PROMPT),
            ("human", "{question}")
        ]
    )

    chain = prompt | llm | StrOutputParser()
    return chain