# Import dependencies
import numpy as np
import random
from collections import defaultdict
import csv


def has_unique_irv_winner(profile):
    '''
    Determines whether a given profile has a unique winner.
    '''
    # Get Vars
    num_alternatives = len(profile[0])
    num_voters = len(profile)

    # Initialize dict to track first place votes
    scores = dict()
    for i in range(num_alternatives):
        scores[i] = 0

    while len(profile[0]) > 1:
        # Get first choice votes, add to score
        for voter in range(num_voters):
            ballot = profile[voter]
            firstChoice = int(ballot[0])
            scores[firstChoice] += 1

        # Eliminate alternative with fewest votes
        minReceived = min(scores.values())
        elim = [key for key in scores.keys() if scores[key] == minReceived]

        for elimAlt in elim:
            # Remove bad alternative from scores
            del scores[elimAlt]

            for voter in range(num_voters):
                # Remove bad alternative from profile
                profile[voter].remove(str(elimAlt))

    return len(profile[0]) == 1


def createAlternatives(num):
    '''
    Create list with desired number of alternatives. Example: createAlternatives(5) = ['0', '1', '2', '3', '4'].
    '''
    return [str(i) for i in range(num)]


def generateProfile(num_voters, alternatives):
    '''
    Given the number of voters and alternatives, this function returns a profile with each ballot a randomized shuffle of the alternatives.
    '''

    # Initialize empty list for profile
    profile = []

    for i in range(num_voters):
        # For every voter, randomize ranking of alternatives and add to profile
        ballot = random.sample(alternatives, len(alternatives))
        profile.append(ballot)

    return profile


def runSim(num_sims, num_alternatives, num_voters):
    '''
    Performs the simulation and returns the results
    '''

    numUniqueWinners = 0
    # Set Dictionary to track how many times each number of winners occurs
    for i in range(num_sims):

        # Create alternatives, then profiles, then determine condorcet winner each time
        alternatives = createAlternatives(num_alternatives)
        profile = generateProfile(num_voters, alternatives)

        if has_unique_irv_winner(profile):
            numUniqueWinners += 1

    return str(100*numUniqueWinners/num_sims)+"%"


def outputData(dataframe):
    '''
    Outputs the given data as a csv file.
    '''
    with open("./Instant Runoff/InstantRunoffData.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(dataframe)


if __name__ == "__main__":
    # Set up environment
    num_sims = 10000
    num_voters_range = (2, 100)
    num_alternatives_range = (2, 10)

    data = []
    columns = ["num_voters", "num_alternatives", "has_winner"]
    data.append(columns)

    # Run simulation for every pair of num_alternatives and num_voters in the given range
    for num_alternatives in range(num_alternatives_range[0], num_alternatives_range[1]+1, 1):
        for num_voters in range(num_voters_range[0], num_voters_range[1]+1, 1):

            result = runSim(num_sims, num_alternatives, num_voters)

            # Initialize list for data to be entered (eventually will be appended to data)
            row = []

            # Enter results into row

            row.append(num_voters)
            row.append(num_alternatives)
            row.append(result)

            data.append(row)
            print(num_voters, num_alternatives)

    outputData(data)
