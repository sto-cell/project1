import pandas as pd
import math

# Load the Excel file
file_path = 'k10.xlsx'  # Update with your actual file path
df = pd.read_excel(file_path)

# Determine how many rows (emails) are in the file
total_rows = len(df)

# Number of rows per file
rows_per_file = 250

# Calculate how many files we need
num_files = math.ceil(total_rows / rows_per_file)

# Split the DataFrame and save each chunk to a new Excel file
for i in range(num_files):
    # Calculate the start and end indices for each chunk
    start_row = i * rows_per_file
    end_row = (i + 1) * rows_per_file

    # Get the chunk of data
    chunk_df = df.iloc[start_row:end_row]

    # Save the chunk to a new Excel file
    output_file = f'emails_part{i+1}.xlsx'
    chunk_df.to_excel(output_file, index=False)

    print(f'File {output_file} saved with rows {start_row + 1} to {min(end_row, total_rows)}')
