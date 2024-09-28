import sys
import unittest
import random
import string


def main():
    text1 = "attack at dawn"
    hex_text1 = text1.encode('utf-8').hex()
    # [2:] retire le préfixe 0x
    # .zfill s'assure que chaque paire d'hexa est bien exprimée sur 2 positions
    text2 = "attack at dusk"
    hex_text2 = text2.encode('utf-8').hex()

    hex_cyphered = "6c73d5240a948c86981bc294814d"

    hex_test = xor_strings(hex_text1, hex_text2)
    hex_key = xor_strings(hex_text1, hex_cyphered)

    encoded2 = xor_strings(hex_text2, hex_key)
    print(encoded2)


#//todo définir une chaine globael HEX qui permette de en pas répéter à chaque fois la liste des caractères autorisés.
def xor_strings(strA, strB):
    if len(strA) != len(strB):
        raise ValueError("the 2 strings should have the same length")
    if not (set(strA).issubset('0123456789abcdef')):
        raise ValueError("strA should contain n-only hex-alloed caracters")
    if not (set(strA).issubset('0123456789abcdef')):
        raise ValueError("strB should contain n-only hex-alloed caracters")

    # une certaine logique aurait dû faire de calculer par 2 caractère
    # puisque chaque lettre est constituée de 2 caractères hexa;
    # mais on sait aussi que l'on peut le faire lettre par lettre, cela ne changera rien.
    # (il n'en n'aurait pas été de même si nous avions voulu faire cela sur des entiers)
    return "".join(str(hex(int(chrA, 16) ^ int(chrB, 16))[2:]) for (chrA, chrB) in zip(strA, strB))


class TestXorStrings(unittest.TestCase):

    def test_same_length(self):
        # Cas de test où les chaînes ont la même longueur
        result = xor_strings("abc", "def")
        expected = '753'  # Résultat du XOR de 'abc' et 'def'    '\x05\x07\x05'
        self.assertEqual(result, expected)

    def test_empty(self):
        # Cas de test pour deux chaînes vides
        result = xor_strings("", "")
        self.assertEqual(result, "")

    def test_different_length(self):
        # Cas de test où les chaînes ont des longueurs différentes
        with self.assertRaises(ValueError):
            xor_strings("abc", "abcd")

    def test_special_chars(self):
        # Cas de test avec des caractères spéciaux
        result = xor_strings(string_to_hex("!@#"), string_to_hex("$%^"))
        expected = '05657d'  # Résultat du XOR de '!@#' et '$%^'   '\x05\x07\x05'
        self.assertEqual(result, expected)

    def test_111(self):
        length = random.randint(1, 20)
        str_test = ''.join(random.choices('0123456789abcdef', k=length))
        result_i = xor_strings(str_test, "1" * length)
        result = xor_strings(result_i, "1" * length)
        expected = str_test
        self.assertEqual(result, expected)

    def test_000(self):
        length = random.randint(1, 20)
        str_test = ''.join(random.choices('0123456789abcdef', k=length))
        result = xor_strings(str_test, "0" * length)
        expected = str_test
        self.assertEqual(result, expected)

    def test_self(self):
        length = random.randint(1, 20)
        str_test = ''.join(random.choices('0123456789abcdef', k=length))
        result = xor_strings(str_test, str_test)
        expected = "0" * length
        self.assertEqual(result, expected)


def string_to_hex(s):
    # Convertir chaque caractère en son code ASCII, puis en hexadécimal sans espaces
    return ''.join(format(ord(c), '02x') for c in s)


#main()
if __name__ == '__main__':
    unittest.main()

