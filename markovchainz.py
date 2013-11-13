import random
from math import exp

song_filename = 'lupe_fiasco'


########## Functions
# Standard matrix-on-vector multiplication.
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
    line_replacements = (('\n',' \n '), ('\r',' '), ('(',' '), (')',' '),
                         ('"',' '))
    for line in song_file:
        for replacement in line_replacements:
            line = line.replace(replacement[0], replacement[1])
        sum_so_far = sum_so_far + len(line.split(' '))
        num_lines = num_lines + 1
        all_words.extend([ word.lower().strip(' ')
                           for word in line.split(' ') ])
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
# Divide each column element by the sum of the column so that
# column sums to 1 (since it's a probability).
for c in range(len(matrix)):
    sum_column = sum([ matrix[r][c] for r in range(len(matrix)) ])
    if sum_column == 0:
        matrix[unique_words.index('\n')][c] = 1
        sum_column = 1
    for r in range(len(matrix)):
        matrix[r][c] = matrix[r][c] / sum_column
        

########## Generate rap.
# Define initial word by its index in unique_words and set word length of rap.
word_index = 0 # (Start with newline.)
len_rap = 100
rap = unique_words[word_index]
len_line = 0
# Pick next words given probability vector of the curent word in the matrix.
for i in range(len_rap):
    len_line = len_line + 1
    prob_vector = [ matrix[r][word_index] for r in range(len(matrix)) ]
    if prob_vector[unique_words.index('\n')] != 1:
        # Modify the probability vector to account for line length by
        # setting probability of newline to the weighted average of
        # 1-e^(-0.5*len_line) and probability of newline in transition matrix.
        # (1-e^(-.05x) has about .5 chance at x=11 and .7 at x=20)
        weight = 0.9
        newline_probability = ((1-weight)*prob_vector[unique_words.index('\n')]
                               + weight*(1-exp(-0.06*len_line)))/2
        prob_vector[unique_words.index('\n')] = newline_probability
        prob_vector = [ i/sum(prob_vector) for i in prob_vector ]
    # Draw from uniform distribution and pick word in probability vector.
    rand = random.random()
    sum_so_far = 0
    for j in range(len(prob_vector)):
        sum_so_far = sum_so_far + prob_vector[j]
        if rand < sum_so_far:
            word_index = j
            rap = rap + unique_words[word_index]
            if unique_words[word_index] == '\n':
                len_line = 0
            else:
                rap = rap + ' '
            break


print(rap)
