def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ''
    for ch in plaintext:
        if not ch.isalpha():
            ciphertext += ch
        elif 'A' <= ch <= 'Z':
            ciphertext += chr((ord(ch) + 3 - ord('A')) % 26 + ord('A'))
        elif 'a' <= ch <= 'z':
            ciphertext += chr((ord(ch) + 3 - ord('a')) % 26 + ord('a'))

    return ciphertext
# зашифровали


def decrypt_caesar(ciphertext):
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
    plaintext = ''
    for ch in ciphertext:
        if not ch.isalpha():
            plaintext += ch
        elif 'A' <= ch <= 'Z':
            plaintext += chr((ord(ch) - 3 - ord('A')) % 26 + ord('A'))
        elif 'a' <= ch <= 'z':
            plaintext += chr((ord(ch) - 3 - ord('a')) % 26 + ord('a'))
    return plaintext
# расшифровали
