# -*- coding: utf-8 -*-

import numpy
import soundex

def topns(matrix, n):

	matrix = numpy.array(matrix)

	flatted = matrix.flatten()

	idx_1d = numpy.argsort(flatted)

	idx_2d = numpy.vstack(numpy.unravel_index(idx_1d, matrix.shape)).transpose()

	idx_2d = list(reversed(idx_2d))

	for index in idx_2d:

		print index[0], index[1], matrix[index[0]][index[1]]

	return idx_2d

def leven(gnodes, tnodes, pairs):

	pass

def sondx(gnodes, tnodes, pairs):

	similaritys = []

	for pair in pairs:

		str1 = gnodes[pair[1]]

		str2 = tnodes[pair[0]]

		similarity = soundex.Soundex().compare(str1, str2)

		similaritys.append(similarity)

	return similaritys

def start(matrix, gnodes, tnodes):

	numpy.set_printoptions(threshold="nan")

	print matrix

	# for node in gnodes:
	
	# 	print node

	# for node in tnodes:
	
	# 	print node

	gnodes = list(gnodes)

	tnodes = list(tnodes)

	pairs = topns(matrix, matrix.shape[0] * matrix.shape[1])

	similaritys = sondx(gnodes, tnodes, pairs)

	results = []

	for pair, similarity in zip(pairs, similaritys):

		results.append([gnodes[pair[1]], tnodes[pair[0]], matrix[pair[0]][pair[1]], similarity])

		print results[-1]

	return results

