# You did this wrong! Transition matrix is only for future probabilites, not next probabilities. Use Markov property.

import random
from math import exp

song_filename = 'lupe_fiasco'



def multiply(matrix, vector):
    new_vector = []
    for r in range(len(vector)):
        i = sum([ matrix[r][i]*vector[i] for i in range(len(matrix[r])) ])
        new_vector.append(i)
    return(new_vector)


########## Read in the input song lyrics.
with open(song_filename) as song_file:
    all_words = []
    sum_so_far = 0
    num_lines = 0
    for line in song_file:
        line.replace('\n',' \n')
        line.replace('(',' ')
        line.replace(')',' ')
        line.replace(',',' , ')
        sum_so_far = sum_so_far + len(line.split(' '))
        num_lines = num_lines + 1
        all_words.extend([ word.lower() for word in line.split(' ') ])
    avg_line_len = sum_so_far / num_lines
all_words = [ word for word in all_words if word != '' ]
unique_words = sorted(list(set(all_words)))


########## Compute transition matrix.
# Make blank matrix.
matrix = []
row = [0] * len(unique_words)
for i in range(len(unique_words)):
    matrix.append(row[:])
# Add counts for each time the column-word is followed by the row-word.
for i in range(len(all_words)-1):
    c = unique_words.index(all_words[i])
    r = unique_words.index(all_words[i+1])
    matrix[r][c] = matrix[r][c] + 1
# Divides each column element by the sum of the column so that
# column sums to 1 (since it's a probability).
for c in range(len(unique_words)):
    sum_column = sum([ matrix[r][c] for r in range(len(unique_words)) ])
    if sum_column == 0:
        matrix[unique_words.index('\n')][c] = 1
        sum_column = 1
    for r in range(len(unique_words)):
        matrix[r][c] = matrix[r][c] / sum_column

# NOTE: Use 1-e^(-x) somehow where x = current line len - avg line len
########## Generate rap.
# Define initial probability vector.
probability_vector = [1]
probability_vector.extend([0] * (len(unique_words)-1))
num_words = 100
rap = ''
len_line = 0
for i in range(num_words):
    len_line = len_line + 1
    # Pick word given currect probability vector.
    rand = random.random()
    sum_so_far = 0
    for j in range(len(probability_vector)):
        sum_so_far = sum_so_far + probability_vector[j]
        if rand < sum_so_far:
            rap = rap + unique_words[j] + ' '
            if unique_words[j] == '\n':
                len_line = 0
            break
    # Update probability vector.
    probability_vector = multiply(matrix, probability_vector)


print(rap)
