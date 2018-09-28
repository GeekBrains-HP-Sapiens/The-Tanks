from textgenrnn import textgenrnn
import os

PATH = "path-to-model"

maps = int(input())

textgen_prod = textgenrnn.load('model.hdf5')


for map in maps:

	textgen_prod.generate_to_file('PATH + level{}.txt'.format([i for i in range(len(maps))], n = 24)



