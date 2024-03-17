from langchain.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain_openai import ChatOpenAI
from typing import List, Optional
import os
import streamlit as st 
import json


def opponent_decision_langchain(poker_data):
    # define the opponent as a structured object
    class Opponent(BaseModel):
        decision: str = Field(description="The decision of the ")
        bet: float = Field(description="")
        status: str = Field(description="")

    # model
    model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0, openai_api_key="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")
    model = model.bind_tools([Opponent])

    # define parser
    parser = PydanticToolsParser(tools=[Opponent])

    # prompt setup
    prompt = ChatPromptTemplate.from_messages([
        ("system",  """
                        You are a poker player 
                    """),
        ("user",    """
                        Current Game Context:\n{raw_recipe}\n---\n 
                        Use the information above to develop your decision for the current betting stage based on your hand and the community 
                        cards currently present (if there are any). For each round take into account the play style of other players at the table 
                        including the user.
                    """)
    ])