import sys
import random
import numpy as np
import matplotlib.pyplot as plt

np.set_printoptions(threshold=sys.maxsize)

codebook = [
    " a | [ 1  1  1  1  1  1  1  1  1  1  1  1  1  1  1  1] | 1111111111111111 ",
    " b | [ 1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1] | 1010101010101010 ",
    " c | [ 1  1 -1 -1  1  1 -1 -1  1  1 -1 -1  1  1 -1 -1] | 1100110011001100 ",
    " d | [ 1 -1 -1  1  1 -1 -1  1  1 -1 -1  1  1 -1 -1  1] | 1001100110011001 ",
    " e | [ 1  1  1  1 -1 -1 -1 -1  1  1  1  1 -1 -1 -1 -1] | 1111000011110000 ",
    " f | [ 1 -1  1 -1 -1  1 -1  1  1 -1  1 -1 -1  1 -1  1] | 1010010110100101 ",
    " g | [ 1  1 -1 -1 -1 -1  1  1  1  1 -1 -1 -1 -1  1  1] | 1100001111000011 ",
    " h | [ 1 -1 -1  1 -1  1  1 -1  1 -1 -1  1 -1  1  1 -1] | 1001011010010110 ",
    " i | [ 1  1  1  1  1  1  1  1 -1 -1 -1 -1 -1 -1 -1 -1] | 1111111100000000 ",
    " j | [ 1 -1  1 -1  1 -1  1 -1 -1  1 -1  1 -1  1 -1  1] | 1010101001010101 ",
    " k | [ 1  1 -1 -1  1  1 -1 -1 -1 -1  1  1 -1 -1  1  1] | 1100110000110011 ",
    " l | [ 1 -1 -1  1  1 -1 -1  1 -1  1  1 -1 -1  1  1 -1] | 1001100101100110 ",
    " m | [ 1  1  1  1 -1 -1 -1 -1 -1 -1 -1 -1  1  1  1  1] | 1111000000001111 ",
    " n | [ 1 -1  1 -1 -1  1 -1  1 -1  1 -1  1  1 -1  1 -1] | 1010010101011010 ",
    " o | [ 1  1 -1 -1 -1 -1  1  1 -1 -1  1  1  1  1 -1 -1] | 1100001100111100 ",
    " p | [ 1 -1 -1  1 -1  1  1 -1 -1  1  1 -1  1 -1 -1  1] | 1001011001101001 ",
    " q | [-1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1 -1] | 0000000000000000 ",
    " r | [-1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1 -1  1] | 0101010101010101 ",
    " s | [-1 -1  1  1 -1 -1  1  1 -1 -1  1  1 -1 -1  1  1] | 0011001100110011 ",
    " t | [-1  1  1 -1 -1  1  1 -1 -1  1  1 -1 -1  1  1 -1] | 0110011001100110 ",
    " u | [-1 -1 -1 -1  1  1  1  1 -1 -1 -1 -1  1  1  1  1] | 0000111100001111 ",
    " v | [-1  1 -1  1  1 -1  1 -1 -1  1 -1  1  1 -1  1 -1] | 0101101001011010 ",
    " w | [-1 -1  1  1  1  1 -1 -1 -1 -1  1  1  1  1 -1 -1] | 0011110000111100 ",
    " x | [-1  1  1 -1  1 -1 -1  1 -1  1  1 -1  1 -1 -1  1] | 0110100101101001 ",
    " y | [-1 -1 -1 -1 -1 -1 -1 -1  1  1  1  1  1  1  1  1] | 0000000011111111 ",
    " z | [-1  1 -1  1 -1  1 -1  1  1 -1  1 -1  1 -1  1 -1] | 0101010110101010 ",
    " . | [-1 -1  1  1 -1 -1  1  1  1  1 -1 -1  1  1 -1 -1] | 0011001111001100 ",
    " , | [-1  1  1 -1 -1  1  1 -1  1 -1 -1  1  1 -1 -1  1] | 0110011010011001 ",
    " ' | [-1 -1 -1 -1  1  1  1  1  1  1  1  1 -1 -1 -1 -1] | 0000111111110000 ",
    " ? | [-1  1 -1  1  1 -1  1 -1  1 -1  1 -1 -1  1 -1  1] | 0101101010100101 ",
    " ! | [-1 -1  1  1  1  1 -1 -1  1  1 -1 -1 -1 -1  1  1] | 0011110011000011 ",
    "   | [-1  1  1 -1  1 -1 -1  1  1 -1 -1  1 -1  1  1 -1] | 0110100110010110 ",
    "   |                          Hadamard Codebook Vector |   Encoded Binary ",
    "---|---------------------------------------------------|----------------- ",
]

def hadamard_matrix(n: int) -> np.ndarray:
    """
    For a given n, generate a hadamard matrix using Sylvester construction 
    
    Recursive algorithm
    """
    if n == 0:
        return np.array([[1]])
    else:
        H = hadamard_matrix(n - 1)
        return np.block([[H, H], [H, -H]])


def encode(message: str, Codebook: np.ndarray):
    """
    Encode a binary message using a Hadamard matrix.
    Message is converted to a row index of the Hadamard matrix.
    This holds the association from plaintext to indexes into the codebook.
    """
    convert = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
               "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
               ".", ",", "'", "?", "!", " " ]
    encoded = None
    list_of_indexes = []
    message = message.lower()
    for c in message:
        index = convert.index(c)
        list_of_indexes.append(index)
        if encoded is None:
            encoded = Codebook[index:index+1,:]
        else:
            encoded = np.concatenate((encoded, Codebook[index:index+1,:]), axis=0)
    return encoded, list_of_indexes

def convert_to_binary(encoded_message: np.ndarray) -> str:
    """
    Convert a hadamard encoded set of vectors into a single Binary String
    """
    convert_bin = ["0", "1"]
    binary_string = ""

    for i in encoded_message:
        # binary_string += "\n"
        for j in i:
            if j == 1:
                binary_string += convert_bin[1]
            else:
                binary_string += convert_bin[0]

    return binary_string

def introduce_error(codeword: np.ndarray, num_errors: int) -> np.ndarray :
    """
    Introduce a specified number of random bit-flip errors in each.
    """
    corrupted = codeword
    for i in corrupted:
        errors = random.randint(0, num_errors)
        change = random.sample(range(0, codeword.shape[1]), errors)
        for j in change:
            i[j] = 1 if i[j] == -1 else -1


    return corrupted

def get_index(X :list):
    max_val = max(X)
    min_val = min(X)
    print("Max: ", max_val, " ind: ", X.index(max_val), " Min: ", min_val, " ind: ", X.index(min_val))

    ind = X.index(max_val) if max_val > (min_val * -1) else X.index(min_val) * -1

    print("Take the index of the largest absolute value: ", ind, "\n")
    return ind

def decode(corrupted: np.ndarray, HM: np.ndarray):
    """
    Decode a corrupted codeword using Hadamard decoding.
    """
    print("Create a new vector X which is the result of corrupted * HM")
    print("X = [x1, x2, x3, x4... x16]")
    waits = 3
    X = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]    
    recovered_index = []
    # for messages M in corrupted
    for M in corrupted:
        for j in range(0, 16):
            X[j] = 0
            for i in range(0, 16):
                X[j] += int(M[i]) * int(HM[i, j])
            
        # X is computed here
        print("Vector complete:")
        print(X)
        print("Finding Max or Min value...")
        index = get_index(X)
        if waits >= 0:
            input()
            waits -= 1
        else :
            print("\n")
        recovered_index.append(index)

    return recovered_index

def display_decoded_message(nums :list):
    convert = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
            ".", ",", "'", "?", "!", " " ]
    
    string = ""
    for i in nums:
        string += convert[i]
    
    return string


def main():
    if len(sys.argv) == 1:
        print("\n\n\t\tHadamard Error Correction Demonstration\n")
        print("Please re-run the script with the following syntax: \n\n"
        "python3 hadamard.py {List of words to transmit}\n\n"
        "Valid characters are A-Z (case insensitive) plus the following"
        " punctuation: . , ' \" ? !")
        return

    ### Recursively call the generating function 5 times to produce a 16x16 
    ### hadamard matrix
    HM = hadamard_matrix(4)
    print("\n\n\t\t***************************************\n")
    print("\t\tHadamard Error Correction Demonstration\n")
    print("\t\t***************************************\n\n")
    print("First we generate an NxN Hadamard matrix using the Sylvester method."
    "For this demonstration we will be using N = 16. This will be the size of\n"
    "the encoded 'word'.")
    print(HM)
    print("To create a codebook, we can take the Hadamard Matrix HM, and append"
    " -HM\nto the bottom, creating an N x 2N matrix C. Each row in C will be "
    "used to\nencode a 'word', in this case we will encode one character per word."
    "\nNote that because there are 16 rows in HM, and another 16 rows in -HM, "
    "we\ncan encode 16 * 2 = 32 different 'words', which will include all the "
    "\nlower case letters plus some common punctuation.\nFor mdetails see the"
    " completed codebook in codebook.md.")
    
    try:
        user = input("\nPlease enter the maximum number of bit flip errors "
        "posible per 'word': ")
        if user == "":
            print("Using default = 3")
            num_errors = 3
        else:
            num_errors = int(user)
        if num_errors < 0 or num_errors > 16:
            print("Error: Cannot have less than 0 or more than 16 errors per "
            "'word'\n")
    except:
        print("Invalid input")
        return
    
    ### Generate the Hadamard Codebook.
    Codebook = np.concatenate((HM, -HM), axis=0)
    Message = sys.argv[1]
    for i in sys.argv[2:] :
        Message = Message + " " + i
    


    input("\nConfirming message: \"" + Message + "\"\nPress enter to continue...")
    encoded_message, sending_num_list = encode(Message, Codebook)
    print("\nConvert message to numeric values:")
    print(sending_num_list)
    
    
    input("\nPress enter to continue...")
    print("\nThe codewords for the message are the following vectors:")
    print(codebook[32])
    print(codebook[33])
    for i in sending_num_list:
        print(codebook[i])
    
    
    input("\nPress enter to continue...")
    print("\nConverted to a single Binary string: ")
    binary_string = convert_to_binary(encoded_message)
    print(binary_string)
    

    input("\nPress enter to continue...")
    print("\nIntroducing error:")
    corrupted_message = introduce_error(encoded_message, num_errors)
    corrupted_binary = convert_to_binary(corrupted_message)
    print(corrupted_binary)
    

    input("\nPress enter to continue...")
    print("Convert error string back into vectors of size 16 with values {1, -1}")
    print(corrupted_message)


    input("\nPress enter to continue...")
    print("For each recieved vector of 16 bits, multiply\nit by the original matrix\n"
    "HM to recover the message.\n") 
    recieving_num_list = decode(corrupted_message, HM)


    print("\nRecovered messages: ", recieving_num_list)
    print("Convert negative indexes I with transformation I' = I * -1 + 16")
    for i in range(0, len(recieving_num_list)):
        recieving_num_list[i] = (recieving_num_list[i]) if recieving_num_list[i] >= 0 else recieving_num_list[i] * -1 + 16
    print(recieving_num_list)
    input("\nPress enter to continue...")
    print("Recall the original message:", Message)
    print("Numeric encoding was : ", sending_num_list)
    print("Recieved decoding is : ", recieving_num_list)

    print("\nIf you chose a number larger than 3, you will likely see the errors in"
    " the\nresulting string.")
    msg = display_decoded_message(recieving_num_list)
    print("\n\tOriginal message: \"" + Message + "\"")
    print("\t Decoded message: \"" + msg + "\"\n")
    print("\t  ***********************\n")
    print("\t  Demonstration complete!\n")
    print("\t  ***********************")


if __name__ == "__main__":
    main()
