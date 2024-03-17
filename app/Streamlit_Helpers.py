import streamlit as st
import math

# converts suit letters to emojis
class Streamlit_Card:
    @staticmethod
    def parse_card(card_str):
        card_rank = card_str[:-1]
        card_suit = card_str[-1]
        return card_rank, card_suit
    
    @staticmethod
    def suit_convert(card_str):
        _, card_suit = Streamlit_Card.parse_card(card_str)

        if card_suit in ["S", "Spades", "Spade"]:
            return "<span style='color: black;'>♠️</span>"
        elif card_suit in ["D", "Diamonds", "Diamond"]:
            return "<span style='color: red;'>♦️</span>"
        elif card_suit in ["C", "Clubs", "Club"]:
            return "<span style='color: black;'>♣️</span>"
        elif card_suit in ["H", "Hearts", "Heart"]:
            return "<span style='color: red;'>♥️</span>"

    # displays cards in a specified streamlit column with customizable spacing
    def display_cards_in_column(opp_num, column, card_strs, space_between_cards_px, space_above_cards_px, space_below_cards_px):
        # if cards are hidden display an emoji
        if card_strs == ["dealt"]:
            cards_html = "<span>🃏</span>"
        if card_strs == ["hidden"]:
            cards_html = "<span>🖐</span>"
        if card_strs == ["burn"]:
            cards_html = "<span>🔥</span>"
        elif card_strs == ["hidden", "hidden"]:
            cards_html = "<span>✋&nbsp;🤚</span>"
        elif card_strs == ["dealt", "hidden"]:
            cards_html = "<span>🃏&nbsp;🤚</span>"
        elif card_strs == ["dealt", "dealt"]:
            cards_html = "<span>🃏&nbsp;🃏</span>"
        elif card_strs == [""]:
            cards_html = "<span>&nbsp;</span>"
        elif card_strs == ["",""]:
            cards_html = "<span>&nbsp;</span>"
        else:
            # convert each card_str to a span element with margin for spacing
            cards_html = ''
            for card_str in card_strs:
                # Parse the card string to get rank and suit
                card_rank, card_suit = Streamlit_Card.parse_card(card_str)
                # Convert the suit to an HTML string with color
                suit_html = Streamlit_Card.suit_convert(card_suit)
                cards_html += f"<span style='margin-right: {space_between_cards_px}px;'>{card_rank}{suit_html}</span>"

        # display the space above cards
        column.markdown(f"<div style='height: {space_above_cards_px}px;'>&nbsp;</div>", unsafe_allow_html=True)
        
        # display the cards
        column.markdown(f"<h1 style='text-align: center;'>{cards_html}</h1>", unsafe_allow_html=True)
        
        if opp_num == "":
            column.markdown(f"&nbsp;", unsafe_allow_html=True)
        elif opp_num == "User":
            column.markdown(f"You", unsafe_allow_html=True)
        else:
            # display opponent
            column.markdown(f"Opponent {opp_num}", unsafe_allow_html=True)
        
        # display the space below cards
        column.markdown(f"<div style='height: {space_below_cards_px}px;'>&nbsp;</div>", unsafe_allow_html=True)

class Streamlit_Player:
    @staticmethod
    def get_position(num_opponents):
        positions_list = ["","","","","","User","","","",""]
        hand_positions_list = [["", ""],["", ""],["", ""],["", ""],["", ""],["hidden", "hidden"],["", ""],["", ""],["", ""],["", ""]]

        if num_opponents == 1:
            positions_list = ["","1","","","","User","","","",""] 
            hand_positions_list = [["", ""],["hidden", "hidden"],["", ""],["", ""],["", ""],["hidden", "hidden"],["", ""],["", ""],["", ""],["", ""]]
        elif num_opponents == 2:
            positions_list = ["","1","","","","User","","","2",""] 
            hand_positions_list = [["", ""],["hidden", "hidden"],["", ""],["", ""],["", ""],["hidden", "hidden"],["", ""],["", ""],["hidden", "hidden"],["", ""]]
        elif num_opponents == 3:
            positions_list = ["","1","","2","","User","","3","",""]
            hand_positions_list = [["", ""],["hidden", "hidden"],["", ""],["hidden", "hidden"],["", ""],["hidden", "hidden"],["", ""],["hidden", "hidden"],["", ""],["", ""]] 
        elif num_opponents == 4:
            positions_list = ["","1","","2","","User","","3","","4"] 
            hand_positions_list = [["", ""],["hidden", "hidden"],["", ""],["hidden", "hidden"],["", ""],["hidden", "hidden"],["", ""],["hidden", "hidden"],["", ""],["hidden", "hidden"]]
        elif num_opponents == 5:
            positions_list = ["1","","2","3","","User","","4","","5"] 
            hand_positions_list = [["hidden", "hidden"],["", ""],["hidden", "hidden"],["hidden", "hidden"],["", ""],["hidden", "hidden"],["", ""],["hidden", "hidden"],["", ""],["hidden", "hidden"]]
        elif num_opponents == 6:
            positions_list = ["1","","2","3","","User","","4","5","6"] 
            hand_positions_list = [["hidden", "hidden"],["", ""],["hidden", "hidden"],["hidden", "hidden"],["", ""],["hidden", "hidden"],["", ""],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"]]
        elif num_opponents == 7:
            positions_list = ["1","2","3","4","","User","5","6","","7"] 
            hand_positions_list = [["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["", ""],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["", ""],["hidden", "hidden"]]
        elif num_opponents == 8:
            positions_list = ["1","2","3","4","","User","7","8","","9"] 
            hand_positions_list = [["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["", ""],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["", ""],["hidden", "hidden"]]
        elif num_opponents == 9:
            positions_list = ["1","2","3","4","","User","7","8","9","10"] 
            hand_positions_list = [["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["", ""],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"]]
        elif num_opponents == 10:
            positions_list = ["1","2","3","4","5","User","7","8","9","10"] 
            hand_positions_list = [["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"],["hidden", "hidden"]]
        
        pos_10 = positions_list[9]
        pos_9 = positions_list[8]
        pos_8 = positions_list[7]
        pos_7 = positions_list[6]
        pos_6 = positions_list[5]
        pos_5 = positions_list[4]
        pos_4 = positions_list[3]
        pos_3 = positions_list[2]
        pos_2 = positions_list[1]
        pos_1 = positions_list[0]

        hand_pos_10 = hand_positions_list[9]
        hand_pos_9 = hand_positions_list[8]
        hand_pos_8 = hand_positions_list[7]
        hand_pos_7 = hand_positions_list[6]
        hand_pos_6 = hand_positions_list[5]
        hand_pos_5 = hand_positions_list[4]
        hand_pos_4 = hand_positions_list[3]
        hand_pos_3 = hand_positions_list[2]
        hand_pos_2 = hand_positions_list[1]
        hand_pos_1 = hand_positions_list[0]

        return pos_1, pos_2, pos_3, pos_4, pos_5, pos_6, pos_7, pos_8, pos_9, pos_10, hand_pos_1, hand_pos_2, hand_pos_3, hand_pos_4, hand_pos_5, hand_pos_6, hand_pos_7, hand_pos_8, hand_pos_9, hand_pos_10
        


