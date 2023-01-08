import ast
import sys
import os

def preprocess(program_text):
    # Parse the program text into an AST
    tree = ast.parse(program_text)

    # Use a list to store the tokens in the program
    tokens = []

    # Use the AST visitor pattern to iterate over the nodes in the tree
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            tokens.append(node.id)
        elif isinstance(node, ast.FunctionDef):
            tokens.append(node.name)
        elif isinstance(node, ast.ClassDef):
            tokens.append(node.name)

    # Return the list of tokens
    return tokens

def levenshtein_distance(s1, s2):
    # base cases
    if s1 == s2:
        return 0
    elif len(s1) == 0:
        return len(s2)
    elif len(s2) == 0:
        return len(s1)

    # recursive case
    cost = 0
    if s1[-1] != s2[-1]:
        cost = 1

    return min(
        levenshtein_distance(s1[:-1], s2) + 1,
        levenshtein_distance(s1, s2[:-1]) + 1,
        levenshtein_distance(s1[:-1], s2[:-1]) + cost
    )

def compare_programs(filename1, filename2):
    with open(filename1, 'r') as file1, open(filename2, 'r') as file2:
        # Read in the contents of the two files
        file1_text = file1.read()
        file2_text = file2.read()

        # Preprocess the program text
        file1_tokens = preprocess(file1_text)
        file2_tokens = preprocess(file2_text)

        # Compute the Levenshtein distance between the two programs
        distance = levenshtein_distance(file1_tokens, file2_tokens)

        # Write the distance to the output file
        return str(distance)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python compare.py <input> <scores>")
        sys.exit(1)

    input_files = sys.argv[1]
    scores = sys.argv[2]

    if not os.path.exists(input_files):
        print("Error: file does not exist.")
        sys.exit(1)
    
    # Read the list of filenames from input_files
    with open(input_files, 'r') as f:
        filenames = [line.strip().split() for line in f]
    
    # Open scores for writing
    with open(scores, 'w') as f:
        for filename1, filename2 in filenames:
            if not os.path.exists(filename1) or not os.path.exists(filename2):
                print("Error: one or both files do not exist.")
                continue

            similarity_score = compare_programs(filename1, filename2)
            f.write(similarity_score + '\n')
