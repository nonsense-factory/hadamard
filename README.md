# Hadamard Error Correction codes

In the late 1960s, NASA was planning missions to send un-manned probes to Mars
to take images of the planet from orbit for the first time. They had to solve 
many difficult technical problems in order to achieve this feat. I will be
examining one problem that they were able to solve related to the transmission
of information from the probe through the harsh environment of space. 

NASA developed and used a process called Hadamard Error Codes, which will be 
demonstrated in this code. 

## Hadamard Matrix: 

A Hadamard Matrix is a matrix that contains values of either -1, or 1, and whose
rows are mutually orthogonal. Each row in the matrix will have values that match
exactly half of every other row in the matrix. The method that was used to 
construct such a matrix is called the Sylvester method and has the following 
form:

To construct a Hadamard Matrix HM_n, 

For n = 1
     
     HM = [1]

For n = 2:

    [HM_1,  HM_1]
    [HM_1, -HM_1]

For n > 2 and n is a power of 2: let k = log_2(n)

    [HM_(2^k-1),  HM_(2^k-1)]
    [HM_(2^k-1), -HM_(2^k-1)]

Example: If n = 4, then k = log_2(4) => k = 2

    [HM_(2^2-1),  HM_(2^2-1)]
    [HM_(2^2-1), -HM_(2^2-1)]

    [HM_(2),  HM_(2)]
    [HM_(2), -HM_(2)]

    {[HM_1,  HM_1]   [HM_1,  HM_1]}
    {[HM_1, -HM_1] , [HM_1, -HM_1]}
    {[HM_1,  HM_1]  -[HM_1,  HM_1]}
    {[HM_1, -HM_1] ,-[HM_1, -HM_1]}

    [1,  1,  1,  1]
    [1, -1,  1, -1]
    [1,  1, -1, -1]
    [1, -1, -1,  1]

Note that the resulting matrix has the property above by comparing each row with
each other row: 

    Row 1:      [1,  1,  1,  1]
    Row 2:      [1, -1,  1, -1]
    Differences:[X,  O,  X,  O] => 2 differences

    Row 1:      [1,  1,  1,  1]
    Row 3:      [1,  1, -1, -1]
    Differences:[X,  X,  O,  O] => 2 differences

    Row 1:      [1,  1,  1,  1]
    Row 4:      [1, -1, -1,  1]
    Differences:[X,  O,  O,  X] => 2 differences
    
    Row 2:      [1, -1,  1, -1]
    Row 3:      [1,  1, -1, -1]
    Differences:[X,  O,  X,  O] => 2 differences
    
    Row 2:      [1, -1,  1, -1]
    Row 4:      [1, -1, -1,  1]
    Differences:[X,  X,  O,  O] => 2 differences
    
    Row 3:      [1,  1, -1, -1]
    Row 4:      [1, -1, -1,  1]
    Differences:[X,  O,  O,  X] => 2 differences

Note also that there are no differences in the first column. This can be 
corrected by creating a new Hadamard Codebook matrix of the following form: 

    HC = [ HM]
         [-HM]

Example from above: 

    [ 1,  1,  1,  1]
    [ 1, -1,  1, -1]
    [ 1,  1, -1, -1]
    [ 1, -1, -1,  1]
    [-1, -1, -1, -1]
    [-1,  1, -1,  1]
    [-1, -1,  1,  1]
    [-1,  1,  1, -1]



## Encoding a message: 

Hadamard encoding works similarly to a substitution cipher. We will be 
associating some arbitrary 'words' with entries into our codebook, which uses
the HC (Hadamard Codebook) to determine what encoded string to send per 'word'.

In the simple example, we can associate each codeword in our codebook with the
binary representation of the number of the row of the HC starting with 0, since
we are working in the realm of computers here. 

A 'word' could be any arbitrary thing of course, but a binary number is simple,
and also counts the number of possible encoded words for us. This number will
be equal to 2xN for the NxN Hadamard Matrix.

Our full codebook then is the following: 

    | Message |  Binary | Hadamard Codeword |
    | ------- | ------- | ----------------- |
    |       0 | 0, 0, 0 |  [ 1,  1,  1,  1] |
    |       1 | 0, 0, 1 |  [ 1, -1,  1, -1] |
    |       2 | 0, 1, 0 |  [ 1,  1, -1, -1] |
    |       3 | 0, 1, 1 |  [ 1, -1, -1,  1] |
    |       4 | 1, 0, 0 |  [-1, -1, -1, -1] |
    |       5 | 1, 0, 1 |  [-1,  1, -1,  1] |
    |       6 | 1, 1, 0 |  [-1, -1,  1,  1] |
    |       7 | 1, 1, 1 |  [-1,  1,  1, -1] |

## Decoding the message

Let us say that Alice sent the message "3" to a recipient, Bob. Alice first 
encodes this message 3 using the codebook generated above, and finds that the 
code-word is [1, -1, -1, 1], then sends the message. Once Bob recieves the 
message, he must recover it. To recover the original message, he can multiply 
the vector of the codeword with the original Matrix HM.

    [ 1, -1, -1,  1]  x [ 1,  1,  1,  1]
                        [ 1, -1,  1, -1]
                        [ 1,  1, -1, -1]
                        [ 1, -1, -1,  1]

    [x1, x2, x3, x4]

    x1 = (1 * 1) + (-1 *  1) + (-1 *  1) + (1 *  1)
     0 =      1  +       -1  +       -1  +       1 
    
    x2 = (1 * 1) + (-1 * -1) + (-1 *  1) + (1 * -1)
     0 =      1  +        1  +       -1  +      -1 
    
    x3 = (1 * 1) + (-1 *  1) + (-1 * -1) + (1 * -1)
     0 =      1  +       -1  +        1  +      -1 
    
    x4 = (1 * 1) + (-1 * -1) + (-1 * -1) + (1 *  1)
     4 =      1  +        1  +        1  +       1 

     [0, 0, 0, 4]
     
     All values therefore are 0, except for the 3rd index, using 0 indexing.

     Refer back to the codebook to discover the message. The third message is 

    0, 1, 1 == [ 1, -1, -1,  1]

Note 1: In this example where the messages are numbers, the index is exactly the
original message when the message is in the "top half" of the codebook. For 
messages in the "bottom half", the value of the matrix multiplication will be
negative. Therefore, if the value is negative, recover the message by finding 
the index into HM^-1.

    [-1, -1,  1,  1]  x [ 1,  1,  1,  1]
                        [ 1, -1,  1, -1]
                        [ 1,  1, -1, -1]
                        [ 1, -1, -1,  1]

    [0, 0,-4, 0]

    Since the value is negative, the lookup will use the index into the HM^-1 
    portion of the codebook.

    | Message |  Binary | Hadamard Codeword |
    | ------- | ------- | ----------------- |
    |       4 | 1, 0, 0 |  [-1, -1, -1, -1] |
    |       5 | 1, 0, 1 |  [-1,  1, -1,  1] | 
    |       6 | 1, 1, 0 |  [-1, -1,  1,  1] |  <--
    |       7 | 1, 1, 1 |  [-1,  1,  1, -1] |

    The message is 6

This is of course a bit silly, since we could just compare the message directly,
there isn't much point to multiplying the vector by the matrix if there are no 
errors. Further, in this simple case, the Hamming distance, or number of 
different elements per row, is 2. We will show that this distance is not 
sufficient to recover from any error.

## Correcting Errors

It has been shown that using Hadamard encoding, a Hadamard code of size 2^J can 
represent all messages of length J + 1. In our example, the Hadamard codes are 
size 4 vectors. 4 is 2^2, so J = 2. We can therefore calculate the number of 
messages that can be encoded as 2^(j+1) = 2^3 = 8 messages.

It has also been shown that for a given message, Hadamard encoding allows for 
error correction in a number of bits equal to the following: 

    Error correction of X bits where 
    
    X = floor( 2^(J-2) - 1/2 )

    In the above example, J = 2, therefore

    X = floor( 2^(2-2) - 1/2 )
    X = floor( 2^0     - 1/2 )
    X = floor(   1     - 1/2 )
    X = floor(1/2)
    X = 0

Therefore we cannot show error correction with the above example. 

However increasing the size of the matrix will allow us to recover from errors,
and this feature will be shown in detail through the included python script 
hadamard.py.
There will also be a video to go along with the code.

## Sources:

https://www.mdpi.com/1424-8220/24/10/3062

