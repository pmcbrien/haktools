import struct, subprocess, sys, argparse
from subprocess import PIPE, TimeoutExpired 

# Define the maximum value for padding
max_padding = 99999
# Store the program to be tested for buffer overflow
program = ""

# Function to check for buffer overflow given a padding size
def check_overflow(padding_size): 
    # Construct the command to execute the program
    command = program
    # Generate payload with 'A's of given size
    payload = "A" * padding_size
    try:
        # Run the program with input payload
        process = subprocess.run(command.split(" "), 
                                 stdout=PIPE, 
                                 stderr=PIPE, 
                                 input=payload,  
                                 encoding="ascii",
                                 timeout=0.1)
        
        # Check if the program crashed (return code -11 indicates segmentation fault)
        if(process.returncode == -11):
            return True
        return False

    except TimeoutExpired:
        return False

# Function to test for buffer overflow with maximum possible padding size
def insane_overflow():
    return check_overflow(max_padding)

# Function to find the minimum padding required to cause buffer overflow
def find_min_padding_in_interval(start, end):
    if (start == end):
        return start
    # Calculate the middle point of the interval
    mid = (int)((start + end) / 2)
    # Check if overflow occurs with the middle padding size
    if (check_overflow(mid)):
        return find_min_padding_in_interval(start, mid)
    return find_min_padding_in_interval(mid + 1, end)

# Function to find the minimum padding required
def find_min_padding():
    return find_min_padding_in_interval(1, max_padding)

# Function to initialize the program and maximum padding from command line arguments
def init_program():
    global program, max_padding

    # Create argument parser
    parser = argparse.ArgumentParser(description='Options',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Add argument for maximum padding size
    parser.add_argument("-m","--max", 
                        help="maximum number of bytes to test", 
                        type=int,
                        default=max_padding)

    # Add argument for program to be tested
    parser.add_argument("program", 
                        help="program to perform the check on")

    # Parse command line arguments
    args = parser.parse_args()

    # Store program and maximum padding size
    program = args.program
    max_padding = args.max

# Main function to execute the program
def main():
    # Initialize program and maximum padding size
    init_program()

    # Check for buffer overflow
    if (insane_overflow()):
        minimum_padding = find_min_padding()
        # Print the minimum padding required to cause buffer overflow
        print("Program needs at least %d bytes to break." % minimum_padding)
        print("That means your padding should be %d bytes long" % (minimum_padding - 4))
        
    else:
        # If program is not vulnerable to buffer overflow
        print("%s is not vulnerable to buffer overflow. Better luck next time" % program)

# Call the main function
main()
