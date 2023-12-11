# Import packages
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from scipy.interpolate import griddata

# Import data, remove index and percentage sign
df = pd.read_csv("./Condorcet/CondorcetData.csv")
df['1_winners'] = df['1_winners'].str.rstrip('%').astype(float) / 100.0

# Create X, Y, and Z coordinates
X = df['num_voters']
Y = df['num_alternatives']
Z = df['1_winners']

# Define the regular grid for the 3D surface plot
X_interp = np.linspace(X.min(), X.max(), 100)
Y_interp = np.linspace(Y.min(), Y.max(), 100)
X_interp, Y_interp = np.meshgrid(X_interp, Y_interp)

# Interpolate the Z values onto the regular grid
Z_interp = griddata((X, Y), Z, (X_interp, Y_interp), method='cubic')

# Create the 3D surface plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surface = ax.plot_surface(X_interp, Y_interp, Z_interp, cmap='viridis')

# Add labels and a color bar
ax.set_title("Percentage of Times a Unique Condorcet Winner Occured with Variable\nVoters and Alternatives Over 100,000 Simulations")
ax.set_xlabel('Number of Voters')
ax.set_ylabel('Number of Alternatives')
ax.set_zlabel('Condorcet Unique Winner Percentage')
fig.colorbar(surface, label='Percentage', location="left")

# Show the plot
plt.show()

plt.style.use("ggplot")

### Average unique winner percentage by num_voters ###

avgWinnerPctByVoters = []
for i in range(2, 101):
    df_ = df.loc[df['num_voters'] == i]
    avgWinnerPctByVoters.append(df_['1_winners'].mean())

plt.plot([i for i in range(2, 101)], avgWinnerPctByVoters, c="b")
plt.title("Average Unique Winner Percentage by Number of Voters", pad=10)
plt.xlabel("Number of Voters", fontsize=10)
plt.ylabel("Percentage of Time Unique Winner Occured", fontsize=10)
plt.show()

### Even Odd Num Voters Analysis ###

evenDf = df.loc[df['num_voters'] % 2 == 0]
oddDf = df.loc[df['num_voters'] % 2 == 1]
evenWinPct = []
oddWinPct = []

for i in range(2, 101, 2):
    df_ = evenDf.loc[evenDf['num_voters'] == i]
    evenWinPct.append(df_['1_winners'].mean())

for i in range(3, 101, 2):
    df_ = oddDf.loc[oddDf['num_voters'] == i]
    oddWinPct.append(df_['1_winners'].mean())

plt.plot([i for i in range(2, 101, 2)], evenWinPct,
         c='b', label="Even Popultation")
plt.plot([i for i in range(3, 101, 2)],
         oddWinPct, c='r', label="Odd Population")
plt.legend(loc="center right")
plt.title("Average Unique Winner Percentage by Number of Voters, By Parity", pad=10)
plt.xlabel("Number of Voters", fontsize=10)
plt.ylabel("Percntage of Time Unique Winner Occured", fontsize=10)
plt.show()

### Aggregate Numbers ###

# 71.41585634118968 % Unique winner percentage overall
print("Overall Unique Winner Percentage: ", df["1_winners"].mean())
print("Even Population Unique Winner Percentage: ",
      evenDf["1_winners"].mean())  # 70.20626666666665 % odd population
# 72.65013151927437 % even population
print("Odd Population Unique Winner Percentage: ", oddDf["1_winners"].mean())
