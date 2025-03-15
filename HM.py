import sys
import numpy as np

np.set_printoptions(threshold=sys.maxsize)

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
    
def main():
    user = input("Enter jth Power of 2")
    num = int(user)
    matrix = hadamard_matrix(num)
    print(matrix)


if __name__ == "__main__":
    main()