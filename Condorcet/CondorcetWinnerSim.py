# Import dependencies
import random
from collections import defaultdict
import csv


def has_condorcet_winner(profile, alternatives):
    '''
    Determines whether a given profile has a unique winner.
    '''
    winners = list()

    # Iterate through alternatives to compare to the other ones
    for alt in alternatives:

        # Create list and dictionary of the other choices in order to make comparisons and tracking scores easier
        others = list(set(alternatives) - set([alt]))
        others_scores = defaultdict(int)

        # Iterate through every ballot and compare to the other alternatives
        for diff_alt in others:
            for i in range(len(profile)):

                # index i < index j implies voter prefers i to j
                # if they prefer anything other than current choice, increment value associated with that alternative in dictionary
                if (profile[i].index(alt) > profile[i].index(diff_alt)):
                    others_scores[diff_alt] += 1

        if (all(value <= len(profile)/2 for value in others_scores.values())):
            # If the other choices all got less or equal to half the vote, then current alternative is a Condorcet Winner
            winners.append(alt)

    return winners


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

    # Set Dictionary to track how many times each number of winners occurs
    num_condorcet_winners = defaultdict(int)

    for i in range(num_sims):

        # Create alternatives, then profiles, then determine condorcet winner each time
        alternatives = createAlternatives(num_alternatives)
        profile = generateProfile(num_voters, alternatives)
        winners = has_condorcet_winner(profile, alternatives)

        # Update dictionary when that number of winners occurs
        num_condorcet_winners[len(winners)] += 1

    # Convert dictionary values to percentages and return
    num_condorcet_winners_percentages = {
        k: (str(100*v/num_sims)+"%") for k, v in num_condorcet_winners.items()}
    return num_condorcet_winners_percentages


def outputData(dataframe):
    '''
    Outputs the given data as a csv file.
    '''
    with open("CondorcetData.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(dataframe)


if __name__ == "__main__":
    # Set up environment
    num_sims = 100000
    num_voters_range = (2, 100)
    num_alternatives_range = (2, 10)

    data = []
    columns = ["num_voters", "num_alternatives"] + \
        [str(i) + "_winners" for i in range(num_alternatives_range[1]+1)
         ] + ["has_winner"]
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

            for i in range(num_alternatives_range[1] + 1):
                if i in result.keys():
                    row.append(result[i])
                else:
                    row.append(0)

            # Find percent where number of winners >= 1
            if 0 in result.keys():
                row.append(str(float(100) - float(result[0][:-1])) + '%')
            else:
                row.append("100%")

            data.append(row)
            print(num_voters, num_alternatives)

    outputData(data)
