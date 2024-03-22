from enum import Enum
from pydantic import BaseModel, Field
from langchain.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os
import streamlit as st 

class ActionOptions(str, Enum):
    fold = "fold"
    check = "check"
    call = "call"
    bet = "bet"
    raise_ = "raise"

class StatusOptions(str, Enum):
    active = "active"
    eliminated = "eliminated"
    showdown = "showdown"
    bet = "bet"
    raise_ = "raise"

class Action(BaseModel):
    action: ActionOptions = Field(description="The action of the player (you) whether it be to fold, bet, check, call, or raise")
    bet: float = Field(default=0.0, description="The amount of money out of the player's (your) current stack")
    status: StatusOptions = Field(description="The status of the player (you) as in whether or not they are in the hand (active) or not due to a fold action (eliminated) or in showdown (showdown) if all betting stages are over and players must reveal their cards")
    action_time: float = Field(default=0.0, description="The amount of time the player (you) takes to decide (in this situation simulate deciding) on the action")

def opponent_decision_langchain(poker_data):
    # load api key
    load_dotenv()

    # model
    model = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
    model = model.bind_tools([Action])

    # define parser
    parser = PydanticToolsParser(tools=[Action])

    # prompt setup
    prompt = ChatPromptTemplate.from_messages([
        ("system",  """
                        You are a level {opp_difficulty} poker player 
                    """),
        ("user",    """
                        Current Game Context:\n{poker_data}\n---\n 
                        Use the information above to return information about an action such as the action itself, bet, status, and action time 
                        for the current betting stage based on your hand and the community cards currently present (if there are any) defined within the game context provided.
                        For each round take into account the play style of other players at the table 
                        including the user using the game context available which will hold information about each player's actions from previous rounds.
                        Understand that folding your hand is a reasonable move in cases where your odds of winning the pot are low, with or without 
                        consideration of the chance of bluffing out opponents. Keep in mind, you are trying to earn maximum value in your earnings through
                        the pot for winning hands assuming the odds are in your favor so maintain a balance of 
         
                        Take into consideration:
                            - the dictionary of game context will change per betting stage (preflop, post flop, post turn, post river) and after each player bets.
                            - cards are displayed as a value, suit code formatted as a number or letter for the value followed by the letter representing a suit. e.g: AH is Ace of Hearts, 10S is 10 of Spades   
                    """)
    ])
    
    # pipeline
    chain = prompt | model | parser

    # invoke using recipe data
    result = chain.invoke(input={"poker_data": poker_data, "opp_difficulty": poker_data["current player (you)"]["current game data"]["opp_difficulty"]})

    # access the parsed recipe data
    opponent_decision = result[0]

    return opponent_decision