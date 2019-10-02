def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    keyword *= len(plaintext) // len(keyword) + 1
    i = 0
    for ch in plaintext:
        if keyword[i].isupper():
            shift = ord(keyword[i]) - 65
        else:
            shift = ord(keyword[i]) - 97
        if ch.isupper():
            ciphertext += chr((ord(ch) + shift - 65) % 26 + 65)
        else:
            ciphertext += chr((ord(ch) + shift - 97) % 26 + 97)
        i += 1

    return ciphertext
# зашифровали

def decrypt_vigenere(ciphertext):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    # put ur code here
    return plaintext