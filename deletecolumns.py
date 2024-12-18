import pandas as pd

# Read the Excel file
input_file = "0.csv"  # Replace with your input file name

data = pd.read_csv(input_file)

# Group size
group_size = 6

# Total columns and groups
num_columns = data.shape[1]
total_groups = num_columns // group_size  # Should be 119 groups

# Identify odd groups to delete (1, 3, 5, ..., 119)
odd_groups = [i for i in range(1, total_groups + 1, 2)]

# Identify columns to keep
columns_to_keep = [
    col for idx, col in enumerate(data.columns)
    if (idx // group_size + 1) not in odd_groups
]

# Filter DataFrame to keep only the desired columns
filtered_data = data[columns_to_keep]

# Save the result to a new Excel file
output_file = "0_tr.csv"  # Replace with your desired output file name
filtered_data.to_csv(output_file, index=False)

print(f"Odd-numbered groups of columns deleted. Result saved to {output_file}.")


