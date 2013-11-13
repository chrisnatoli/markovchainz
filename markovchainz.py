# Read in a song.
song_filename = 'lupefiasco_buildingmindsfaster'
song_filename = 'test'
with open(song_filename) as song_file:
    all_words = [ word.lower() for line in song_file
                  for word in line.replace('\n',' \n')
                  .replace('(','').replace(')','').replace(',','')
                  .split(' ') ]
all_words = [ word for word in all_words if word != '' ]
unique_words = sorted(list(set(all_words)))

# Make matrix.
matrix = []
row = [0] * len(unique_words)
for i in range(len(unique_words)):
    matrix.append(row[:])
for i in range(len(all_words)-1):
    c = unique_words.index(all_words[i])
    r = unique_words.index(all_words[i+1])
    matrix[r][c] = matrix[r][c] + 1
for c in range(len(unique_words)):
    sum_column = sum([ matrix[r][c] for r in range(len(unique_words)) ])
    for r in range(len(unique_words)):
        matrix[r][c] = matrix[r][c]/sum_column
