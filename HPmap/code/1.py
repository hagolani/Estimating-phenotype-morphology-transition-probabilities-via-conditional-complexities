file = open('HP_output_data/output_HPn25.txt','w')
with open("HP_designing/HPn25.txt", 'r') as f:
    lines = f.readlines()

# Initialize variable to hold current sequence identifier
curr_seq_id = None

for line in lines:
    # Strip whitespace from the line
    line = line.strip()

    # If line is a sequence identifier, update current sequence identifier
    if line.isalpha():
        curr_seq_id = line
    # If line is not a sequence identifier, process the header and integer lines
    else:
        h, k = line.split(maxsplit=1)
        k = int(k)
        file.write(h + "  " + curr_seq_id + " " + str(k) + "\n")
        
file.close()
