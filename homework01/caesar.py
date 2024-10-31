def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    for i in range(len(plaintext)):
        if plaintext[i].isalpha():
            kod = ord(plaintext[i])
            if (90 - shift + 1) <= kod <= 90 and shift > 0:
                ciphertext += chr(kod - 26 + shift)
            elif kod >= (122 - shift + 1) and shift > 0:
                ciphertext += chr(kod - 26 + shift)
            else:
                ciphertext += chr(kod + shift)
        else:
            ciphertext += plaintext[i]
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    for i in range(len(ciphertext)):
        if ciphertext[i].isalpha():
            kod = ord(ciphertext[i])
            if 65 <= kod <= (65 + shift - 1) and shift > 0:
                plaintext += chr(kod + 26 - shift)
            elif 97 <= kod <= (97 + shift - 1) and shift > 0:
                plaintext += chr(kod + 26 - shift)
            else:
                plaintext += chr(kod - shift)
        else:
            plaintext += ciphertext[i]
    return plaintext
