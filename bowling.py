import json

games_info = open('games.json','r')

games_json = json.loads(games_info.read())

# emulate the switch case trough a dictionary function mapping conditions with handlers
def score_dict(throw):
        return {
                'F': lambda: 0,
                '-': lambda: 0,
                '0': lambda: 0,
                '1': lambda: 1,
                '2': lambda: 2,
                '3': lambda: 3,
                '4': lambda: 4,
                '5': lambda: 5,
                '6': lambda: 6,
                '7': lambda: 7,
                '8': lambda: 8,
                '9': lambda: 9,
                '/': lambda: 10, 
                'X': lambda: 10,
        }.get(throw, lambda:0) ()

# defining the function responsible for computing the score
def scoreMechanism(game_throws):
    finalScore = 0
    # loop over all the individual throws found in a game
    for i in range (0, len(game_throws)):
        # the logic is wrapped into a try - except enabling exception handling
        try:
            # if current throw is a SPARE 
            if (str(game_throws[i]) == '/'):
                finalScore += score_dict(game_throws[i]) + score_dict(game_throws[i+1])

            # add all the values of the throws if no SPARE was achieved after a STRIKE 
            if (str(game_throws[i]) == 'X' and str(game_throws[i+2]) != '/'):
                finalScore += score_dict(game_throws[i]) + score_dict(game_throws[i+1]) + score_dict(game_throws[i+2])

            # if a  SPARE was achieved after a STRIKE then add only the value of the SPARE to the X's frame
            if (str(game_throws[i]) == 'X' and str(game_throws[i+2]) == '/'):
                finalScore += score_dict(game_throws[i]) + score_dict(game_throws[i+2])

            # add the throw's value if it is no SPARE or STRIKE
            if (str(game_throws[i]) != '/' and str(game_throws[i]) != 'X' and str(game_throws[i+1]) != '/'):
                finalScore += score_dict(game_throws[i])

            # skip this adding the value of the current throw if the next throw represents is a SPARE
            if (str(game_throws[i+1]) == '/'):
                finalScore += 0

         # if an IndexError exception is thrown then perform the following
        except IndexError:
            
            # if the current throw was forced by a SPARE or a STRIKE
            if (str(game_throws[i-1]) == '/' or str(game_throws[i-1]) == 'X' or str(game_throws[i-2]) == 'X'):
                # do not count it in the final score
                finalScore += 0
            # if the current throw was not forced by a SPARE or STRIKE
            else:
                # count the current value of the throw
                finalScore += score_dict(game_throws[i])

    return finalScore

    
#### CONSOLE INTERFACE ####
print("~~~~~                10 PIN BOWLING GAME                           ~~~~~")
print("~~~~~    PRESS Y to PLAY A GAME or ANY OTHER CHARACTER to EXIT     ~~~~~")
command = input()
game_index = 0
while(command=="Y" or command=="y"):
    try:
        print("GAME ID: " + games_json[game_index]['gameId'])
        print(games_json[game_index]['throws'])
        print("SCORE: " + str(scoreMechanism(games_json[game_index]['throws'])))
        game_index += 1
        print("~~~~~ PRESS Y to PLAY A GAME or ANY OTHER CHARACTER to EXIT ~~~~~")
        command = input()
    except IndexError:
        print("SORRY. THE NUMBER OF GAMES AVAILABLE HAVE BEEN EXCEEDED")
        command = "N"
print("~~~~~~~~~~~~~~~~~~~~~~~~~~ END GAME ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

