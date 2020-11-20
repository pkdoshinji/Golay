#!/usr/bin/env python3

'''
Golay.py: Golay encoding and decoding for transmission of data across a noisy channel
Author: Patrick Kelly
Email: patrickyunen@gmail.com
Last revised: April 2, 2020
'''

import random

wordlength = 12

I = [[1,0,0,0,0,0,0,0,0,0,0,0],
     [0,1,0,0,0,0,0,0,0,0,0,0],
     [0,0,1,0,0,0,0,0,0,0,0,0],
     [0,0,0,1,0,0,0,0,0,0,0,0],
     [0,0,0,0,1,0,0,0,0,0,0,0],
     [0,0,0,0,0,1,0,0,0,0,0,0],
     [0,0,0,0,0,0,1,0,0,0,0,0],
     [0,0,0,0,0,0,0,1,0,0,0,0],
     [0,0,0,0,0,0,0,0,1,0,0,0],
     [0,0,0,0,0,0,0,0,0,1,0,0],
     [0,0,0,0,0,0,0,0,0,0,1,0],
     [0,0,0,0,0,0,0,0,0,0,0,1]]

B = [[1,1,0,1,1,1,0,0,0,1,0,1],
     [1,0,1,1,1,0,0,0,1,0,1,1],
     [0,1,1,1,0,0,0,1,0,1,1,1],
     [1,1,1,0,0,0,1,0,1,1,0,1],
     [1,1,0,0,0,1,0,1,1,0,1,1],
     [1,0,0,0,1,0,1,1,0,1,1,1],
     [0,0,0,1,0,1,1,0,1,1,1,1],
     [0,0,1,0,1,1,0,1,1,1,0,1],
     [0,1,0,1,1,0,1,1,1,0,0,1],
     [1,0,1,1,0,1,1,1,0,0,0,1],
     [0,1,1,0,1,1,1,0,0,0,1,1],
     [1,1,1,1,1,1,1,1,1,1,1,0]]


#Randomization function to simulate transmission over a noisy channel
def randomize(bitstring, p=0.05):
    result = ''
    for bit in bitstring:
        if random.uniform(0,1) <= p:
            if bit == '0':
                bit = '1'
            else:
                bit = '0'
        result += bit
    return result


# Multiply two matrices over the Galois field GF2
def GF2_matrix(A,B):
    C_rows = len(A)
    C_cols = len(B[0])
    C = [[0 for k in range(C_cols)] for i in range(C_rows)]

    for i in range(C_rows):
        for k in range(C_cols):
            for j in range(len(A[0])):
                C[i][k] ^= (A[i][j] & B[j][k])
    return C


# Given the (n x i) matrix A and the (n X j) matrix B,
# return the (n x (i + j)) matrix (A|B)
def conjoin(A,B):
    columns = len(A[0]) + len(B[0])
    rows = len(A)
    conjoined = [0] * rows
    for row in range(rows):
        conjoined[row] = A[row] + B[row]
    return conjoined


# Return the transpose of a matrix
def transpose(matrix):
    t_rows = len(matrix[0])
    t_cols = len(matrix)
    transposed = [[0 for k in range(t_cols)] for i in range(t_rows)]

    for i in range(t_rows):
        for j in range(t_cols):
            transposed[i][j] = matrix[j][i]
    return transposed


# Return column n of a matrix
def get_column(matrix, col_num):
    B_col = [[0] * len(matrix[0])]
    for k in range(len(B[0])):
        B_col[0][k] = B[col_num][k]
    return B_col


# Add two vectors over the Galois field GF2
def add_vectors(A,B):
    length = len(A[0])
    C = [[0]*length]
    for index in range(length):
        C[0][index] = A[0][index] ^ B[0][index]
    return C


# Join the elements of a vector & return bitstream string
def string_from_vector(vector):
    return ''.join([str(j) for j in vector[0]])


# Return filename as a bitstream string
def get_bitstream(filename):
    with open(filename, 'rb') as fh:
        bytestream = fh.read()
        bitstream = ''
        for byte in bytestream:
        #     ascii = ord(char)
            binary = '{0:08b}'.format(byte)
            bitstream += binary
    return bitstream


# Pad bitstream with 1s so that # of bits is multiple of wordlength
# Add prefix indicating # of 1s added
def padder(bitstream, wordlength=12):
    prefix, padding = '',''
    length = len(bitstream)
    remainder = length % wordlength
    if remainder != 0:
        padlength = wordlength - remainder
        prefix = '{0:012b}'.format(padlength)
        padding = '1' * padlength
    return prefix + bitstream + padding


# Remove prefix and padding bits
def unpadder(bitstream, wordlength=12):
    padlength = int(bitstream[:wordlength],2)
    return bitstream[wordlength:-padlength]


# Convert bitstream string into GF2 vector
def get_vector(word):
    vector = [[]]
    for char in word:
        vector[0].append(int(char))
    return vector


# Get generator matrix for the extended binary Golay code (G24)
G = conjoin(I,B)


# Get transpose of parity-check matrix for G24
Ht = transpose(conjoin(B,I))


'''Encoding'''

# bitstream = get_bitstream('gettysburgh.txt')
bitstream = get_bitstream('flower.png')
padstream = padder(bitstream)

# Initialize string for encoded data
encoded = ''

# Split the data into 12-bit words, encode each word using
# extended binary Golay code, and convert to string
for index in range(0,len(padstream),wordlength):
    word = padstream[index:index+wordlength]
    vector = get_vector(word)
    Golay_vector = GF2_matrix(vector,G)
    Golay_word = string_from_vector(Golay_vector)
    encoded += Golay_word

bitstream_len = len(bitstream)
encoded_len = len(encoded)


'''Randomize and Decode'''
errbits = ''
outbits = ''

#Get 24-bit segments of the encoded bitstream and rndomize them
for index in range(0,encoded_len,24):
    word = encoded[index:index+24]
    orig = word
    word = randomize(word)
    errbits += word #Add the randomized bits to errbits (received mssg)

    #Transform 24-bit word into vector and calculate syndrome
    wordvector = get_vector(word)
    syndrome1 = GF2_matrix(wordvector,Ht)
    weight = sum(syndrome1[0]) #Weight of the syndrome


    # Case 1: if Hamming weight of syndrome <= 3, we know the error vector
    if weight <= 3:
        error_L = [0] * 12
        error = [error_L + syndrome1[0]]

    # Case 2: Otherwise (wt>3), we process it further...
    else:
        S1_dict = {}
        small_weights = {}
        for j in range(12):
            sum_vec = add_vectors(syndrome1,get_column(B,j)) #S1 + Bi
            syn_weight = sum(sum_vec[0]) #wt(S1 + Bi)
            wt = (syn_weight, sum_vec)
            if syn_weight <= 2:
                small_weights[j] = wt

        # Case 2.1: one subvector weight <= 2
        if len(small_weights) == 1:
            error = [I[list(small_weights.keys())[0]] + sum_vec[0]]

        # Case 2.2: several subvector weights <= 2
        elif len(small_weights) > 1:
            weightlist = [small_weights[key][0] for key in small_weights]
            smallest = min(weightlist)
            for key in small_weights:
                if small_weights[key][0] == smallest:
                    error = small_weights[key][1]
                    break

        # Case 2.3: all subvector weights > 3
        else:
            # Calculate syndrome2
            syndrome2 = GF2_matrix(syndrome1, transpose(B))
            weight2 = sum(syndrome2[0])

            # Case 2.3.1: If the weight of syndrome2 <= 3, we know the error
            if weight2 <= 3:
                error_R = [0] * 12
                error = [syndrome2[0] + error_R]

            # Case 2.3.2: Otherwise, we process further...
            else:
                small_weights = {}
                for j in range(12):
                    wt = ()
                    sum_vec = add_vectors(syndrome2, get_column(B, j))
                    syn_weight = sum(sum_vec[0])
                    wt = (syn_weight, sum_vec)
                    if syn_weight <= 2:
                        error = [sum_vec[0] + I[j]]
                        break
                    else:
                        error = [[0] * 24]


    if not error:
        error = [[0] * 24]
    # Corrected Golay word = (received vector) - (error vector)
    corrected = add_vectors(wordvector,error)
    corr_str = string_from_vector(corrected)
    # Transmitted text = first half of corrected Golay word
    outbits += corr_str[:12]


# Get the uncorrected received message bits (to compare with corrected message)
errbits_out = ''
for j in range(0,len(errbits),24):
    errbits_out += errbits[j:j+12]

mssg = ''
errmssg = ''

# Remove the padding
outbits = outbits[12:]
errbits_out = errbits_out[12:]

# Convert corrected message bits to string
for i in range(0,len(outbits),8):
    charbits = outbits[i:i+8]
    outchar = chr(int(charbits,2))
    mssg += outchar

# Convert uncorrected message bits to string
for i in range(0,len(errbits_out),8):
    charbits = errbits_out[i:i+8]
    outchar = chr(int(charbits,2))
    errmssg += outchar

# Output
print(errmssg)
print(mssg)
