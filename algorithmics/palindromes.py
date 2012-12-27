# -------------------------------------------------------------------------------
# Name:        palindromes
# 
# Author:      mourad mourafiq
# -------------------------------------------------------------------------------


def longest_subpalindrome(string):
    """
    Returns the longest subpalindrome string from the current string
    Return (i,j)
    """
    #first we check if string is ""
    if string == "": return (0, 0)

    def length(slice): a, b = slice; return b - a

    slices = [grow(string, start, end)
              for start in range(len(string))
              for end in (start, start + 1)
    ]
    return max(slices, key=length)


def grow(string, start, end):
    """
    starts with a 0 or 1 length palindrome and try to grow bigger 
    """
    while (start > 0 and end < len(string)
           and string[start - 1].upper() == string[end].upper()):
        start -= 1;
        end += 1
    return (start, end)
