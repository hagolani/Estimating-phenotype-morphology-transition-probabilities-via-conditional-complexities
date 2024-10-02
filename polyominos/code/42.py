from collections import Counter

# Open the file and read all lines
with open('data/binary_rep_1.txt', 'r') as file:
    lines = file.readlines()

# Count occurrences of each unique line
line_counts = Counter(lines)
total_lines = len(lines)

# Write results to a new file
with open('data/results.txt', 'w') as result_file:
    for line, count in line_counts.items():
        probability = count / total_lines
        result_file.write(f"{line.strip()} {count} {probability:.6f}\n")

