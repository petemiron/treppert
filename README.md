treppert
========

uses trello to create a listing of:
    - simple display of all cards on a board.
    - cards without due dates.
    - members of board without in cards in a specific list.

depends on
==========

- Python 2.7
- [trollop](https://bitbucket.org/pmiron/trollop)

usage
=====

    usage: treppert.py [-h] [-l LIST_NAME]
                       trello_dev_key trello_user_token board_name
                       {no_cards,lists,no_dates}

    useful, simple, cmd-based reports from trello.

    positional arguments:
        trello_dev_key        Your dev key the trello API
        trello_user_token     Your user token for the trello API
        board_name            The board to list
            {no_cards,lists,no_dates} 
            show the lists on a board, show all cards with no dates, show all users with no cards.
    
    optional arguments:
    -h, --help            show this help message and exit
    -l LIST_NAME, --list_name LIST_NAME     The name of the trello list.
    

