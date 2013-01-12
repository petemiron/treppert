import trollop
import argparse
from datetime import datetime

#####################################################################
# uses trello to create a listing of:
# - simple display of all cards on a board.
# - cards without due dates.
# - members of board without in cards in a specific list.
#####################################################################
ARGS = None

def lists():
    """
    List all lists and cards for a single trello board.
    """
    conn = trollop.TrelloConnection(ARGS.trello_dev_key, ARGS.trello_user_token)
    # for each of your boards, find the one that matches.
    board_id = get_id_for_name(conn.me.boards, ARGS.board_name)
    print board_id
    for trello_list in conn.get_board(board_id).lists:
        print trello_list.name
        for card in trello_list.cards:
            if (card.closed is False):
                if (hasattr(card, "due")):
                    due_date = card.due
                else:
                    due_date = "no due date"
                print "--", card.name, due_date, card.url 

def no_dates():
    """
    List all cards and the associated members that don't have due dates.
    """
    # find everything on a given board:list that doesn't have a due date.
    # print out the members of that card.
    conn = trollop.TrelloConnection(ARGS.trello_dev_key, ARGS.trello_user_token)
    board_id = get_id_for_name(conn.me.boards, ARGS.board_name)
    list_id = get_id_for_name(conn.get_board(board_id).lists, ARGS.list_name)
    list = conn.get_list(list_id)
    for card in list.cards:
        if (card.closed is False):
            if ((hasattr(card, "due") is False) or (card.due.replace(tzinfo=None) < datetime.now())):
                print card.name, " - ", card.url
                for member in card.members:
                    print "-- ", member.username, member.fullname, member.url

def no_cards():
    """
    List all users with no cards assigned to them for the specified list.
    """
    # create two sets.
    # - members on cards in specified list.
    # - all members of board.
    board_members = {} 
    list_card_members = {} 
    
    conn = trollop.TrelloConnection(ARGS.trello_dev_key, ARGS.trello_user_token)
    board_id = get_id_for_name(conn.me.boards, ARGS.board_name)
    board = conn.get_board(board_id)
    
    for member in board.members:
        board_members[member._id] = member

    list_id = get_id_for_name(board.lists, ARGS.list_name)
    list = conn.get_list(list_id)
    for card in list.cards:
        if (card.closed is False):
            for member in card.members:
                list_card_members[member._id] = member

    not_in_list = set(board_members.keys()).difference(set(list_card_members.keys()))
    
    for member_id in not_in_list:
        member = board_members[member_id]
        print member.username, member.fullname

# convenience method for finding an
# id by name from trello api.
def get_id_for_name(list, name):
    for i in list:
        if (i.name == name):
            return i._id


def main():
    dispatcher = {
            'lists':lists,
            'no_dates':no_dates,
            'no_cards':no_cards
    }

    parser = argparse.ArgumentParser(description="useful, simple, cmd-based \
            reports from trello.")
    parser.add_argument("trello_dev_key", 
            help="Your dev key the trello API")
    parser.add_argument("trello_user_token",
            help="Your user token for the trello API")
    parser.add_argument("board_name",
            help="The board to list")
    parser.add_argument("-l", "--list_name",
            help="The name of the trello list.")

    parser.add_argument("cmd", choices=dispatcher.keys(),
            help="show the lists on a board, show all cards with no dates, \
                    show all users with no cards.")

    global ARGS
    ARGS = parser.parse_args()

    # runs the sent command with all passed args
    eval("%s()" % ARGS.cmd,{'__builtins__':None},dispatcher)

if __name__ == "__main__":
    main()
