# Import packages
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits import mplot3d
from scipy.interpolate import griddata

# Import data, remove index and percentage sign
df = pd.read_csv("./Coombs/CoombsData.csv")
df['has_winner'] = df['has_winner'].str.rstrip('%').astype(float) / 100.0

# Create X, Y, and Z coordinates
X = df['num_voters']
Y = df['num_alternatives']
Z = df['has_winner']

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
ax.set_title(
    "Percentage of Times a Unique Winner Occured with Variable\nVoters and Alternatives Over 10,000 Simulations")
ax.set_xlabel('Number of Voters')
ax.set_ylabel('Number of Alternatives')
ax.set_zlabel('Unique Winner Percentage')
# ax.set_zlabel('')
# ax.set_zticks([])
fig.colorbar(surface, label='Percentage', location="left")

# Show the plot
plt.show()


plt.style.use("ggplot")

### Average unique winner percentage by num_voters ###

avgWinnerPctByVoters = []
for i in range(2, 101):
    df_ = df.loc[df['num_voters'] == i]
    avgWinnerPctByVoters.append(df_['has_winner'].mean())

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
    evenWinPct.append(df_['has_winner'].mean())

for i in range(3, 101, 2):
    df_ = oddDf.loc[oddDf['num_voters'] == i]
    oddWinPct.append(df_['has_winner'].mean())

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

print("Overall Unique Winner Percentage: ",
      df["has_winner"].mean()*100)  # 94.92272727272728
print("Even Population Unique Winner Percentage: ",
      evenDf["has_winner"].mean()*100)  # 93.8316
print("Odd Population Unique Winner Percentage: ",
      oddDf["has_winner"].mean()*100)  # 96.03612244897959
