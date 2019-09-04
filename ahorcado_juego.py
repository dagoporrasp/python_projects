import random

IMAGES = ['''
	
    +---+
    |   |
        |
        |
        |
        |
        =========''', '''

    +---+
    |   |
    O   |
        |
        |
        |
        =========''', '''

    +---+
    |   |
    O   |
    |   |
        |
        |
        =========''', '''

    +---+
    |   |
    O   |
   /|   |
        |
        |
        =========''', '''

    +---+
    |   |
    O   |
   /|\  |
        |
        |
        =========''', '''

    +---+
    |   |
    O   |
   /|\  |
    |   |
        |
        =========''', '''

    +---+
    |   |
    O   |
   /|\  |
    |   |
   /    |
        =========''', '''	

    +---+
    |   |
    O   |
   /|\  |
    |   |
   / \  |
        ========='''
        ]

WORDS = [
	'lavadora', 'secadora',
	'sofa', 'gobierno',
	'diputado', 'democracia',
	'computadora', 'teclado']

def display_board(hidden_word, tries, separator_lst): 
	print(IMAGES[tries])
	print('')
	print(hidden_word)
	print(''.join(separator_lst))

def random_word():
	return WORDS[random.randint(0,len(WORDS)-1)]

def separator():
	lst_lengths = [len(w) for w in WORDS]
	return ['--- *']*max(lst_lengths)

def run():
	separator_lst = separator()
	word = random_word()
	hidden_word = ['-']*(len(word))
	tries = 0

	while True:
		display_board(hidden_word, tries, separator_lst)
		current_letter = str(input('Escoge una letra: '))

		letter_idx = []
		for idx in range(len(word)):
			if word[idx] == current_letter:
				letter_idx.append(idx)

		if len(letter_idx) == 0:
			tries += 1
			if tries == len(IMAGES)-1:
				display_board(hidden_word, tries, separator_lst)
				print('G A M E  O V E R')
				print('La palabra era {}'.format(word))
				break
		else:
			for idx in letter_idx:
				# print(idx)
				hidden_word[idx] = current_letter

			letter_idx = []

		try:
			hidden_word.index('-')
		except ValueError:
			display_board(hidden_word, tries, separator_lst)
			print('')
			print('¡Felicidades! Ganaste. La palabra es: {}'.format(word))
			break


		# Otra forma de Ganar
		# if ''.join(hidden_word) == word:
		# 	print('Felicidades! Ganaste')
		# 	break

if __name__ == '__main__':
	print('B I E N V E N I D O S  A  A H O R C A D O S')
	run()
