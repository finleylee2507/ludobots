import os
import matplotlib.pyplot as plt

DATA_DIR = "fitness"
CURVES_DIR = "curves"

if not os.path.exists(CURVES_DIR):
    os.mkdir(CURVES_DIR)
# Get all the files containing data
files = [f for f in os.listdir(DATA_DIR) if os.path.isfile(os.path.join(DATA_DIR, f))]
if not files:
    print("NO DATA TO ANALYZE")
    exit()

# Loop through the filenames
for file in files:
    # Get the metadata for the legend
    split_name = file.split("_")
    legend = f"{split_name[0]} Creatures, {split_name[1]} Generations, Seed {split_name[2][0]}"

    # Read the data and plot the curve
    with open(os.path.join(DATA_DIR, file)) as f:
        data = [float(line.strip()) for line in f if line.strip()]
        plt.plot(data, label=legend)

# Format and plot
plt.ylabel("Fitness Value")
plt.xlabel("Generation")
plt.title("Fitness Curves")
plt.legend()

# Save the figure
fig_number = len(os.listdir(CURVES_DIR)) + 1
plt.savefig(os.path.join(CURVES_DIR, f"Curve{fig_number}.png"))
