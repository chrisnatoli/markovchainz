import random
from math import exp

song_filename = 'lupe_fiasco'


########## Read in the input song lyrics.
with open(song_filename) as song_file:
    all_words = []
    end_words = []
    sum_so_far = 0
    num_lines = 0
    line_replacements = (('\n',' \n '), ('\r',' '), ('(',' '), (')',' '),
                         ('"',' '))
    for line in song_file:
        for replacement in line_replacements:
            line = line.replace(replacement[0], replacement[1])
        words = line.split(' ')
        sum_so_far = sum_so_far + len(words)
        num_lines = num_lines + 1
        all_words.extend([ word.lower().strip(' ')
                           for word in words ])
        end_words.append(words[-2])
    avg_line_len = sum_so_far / num_lines
all_words = [ word for word in all_words if word != '' ]
unique_words = sorted(list(set(all_words)))
end_words = [ word for word in end_words if word != '' ]
unique_end_words = sorted(list(set(end_words)))

########## Compute transition matrix.
def compute_transition_matrix(words, uniqs):
    # Make blank matrix.
    matrix = []
    row = [0] * len(uniqs)
    for i in range(len(uniqs)):
        matrix.append(row[:])
    # Add counts for each time the column-word is followed by the row-word.
    for i in range(len(words)-1):
        c = uniqs.index(words[i])
        r = uniqs.index(words[i+1])
        matrix[r][c] = matrix[r][c] + 1
    # Divide each column element by the sum of the column so that
    # column sums to 1 (since it's a probability).
    for c in range(len(matrix)):
        sum_column = sum([ matrix[r][c] for r in range(len(matrix)) ])
        if sum_column == 0:
            matrix[uniqs.index('\n')][c] = 1
            sum_column = 1
        for r in range(len(matrix)):
            matrix[r][c] = matrix[r][c] / sum_column
    return matrix
all_words_matrix = compute_transition_matrix(all_words, unique_words)
end_words_matrix = compute_transition_matrix(end_words, unique_end_words)

########## Generate rap.
# Define initial word by its index in unique_words and set word length of rap.
word_index = 0 # (Start with newline.)
end_word_index = 0
len_rap = 100
rap = [unique_words[word_index]]
len_line = 0

# Pick next words given probability vector of the curent word in the matrix.
for i in range(len_rap):
    len_line = len_line + 1
    prob_vector = [ all_words_matrix[r][word_index]
                    for r in range(len(all_words_matrix)) ]

    # Modify the probability vector to account for line length by
    # setting probability of newline to the weighted average of
    # 1-e^(-0.5*len_line) and probability of newline in transition matrix.
    # (1-e^(-.05x) has about .5 chance at x=11 and .7 at x=20)
    if prob_vector[unique_words.index('\n')] != 1:
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
            if unique_words[j] == '\n':
                # If line ends here, then redo the last word of the line
                # with a modified probability vector that increases the chance
                # of a matching end word.
                # [insert code here after changing to nth order markov chain]
                end_word_index = unique_words[word_index]
                len_line = 0
            word_index = j
            rap.append(unique_words[word_index])
            break


print(' '.join(rap))
