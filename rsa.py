from primesieve import primes as get_primes
from random import shuffle, randint
from math import gcd
import streamlit as st

@st.experimental_memo
def get_keys():
    shuffle(primes)

    p, q = primes[:2]
    N = p*q
    phi_N = phi(p, q)

    e = phi_N
    d = -1
    while gcd(e, phi_N) > 1 or d < 0:
        e = randint(2, phi_N-1)
        g, d, k = extended_gcd(e, phi_N)

    public_key = e
    private_key = d

    return public_key, private_key, N

def phi(p, q):
    return (p-1)*(q-1)

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, x, y = extended_gcd(b % a, a)
        return g, y - (b // a) * x, x

def get_char(i):
    i = i % len(char_indices)
    return chr(char_indices[i])

def get_char_index(c):
    return char_indices.index(ord(c))

def get_encrypted_string(encrypted):
    string = ''
    for m in encrypted:
        string += str(m).rjust(len(str(N)), '0')
    return string

def split_encrypted_string(encrypted_string, N):
    encrypted = [int(encrypted_string[i:i+len(str(N))]) for i in range(0, len(encrypted_string), len(str(N)))]
    return encrypted

char_indices = [10] + list(range(32, 127+1)) + [196, 214, 220, 223, 228, 246, 252]

exp = 3
primes = list(get_primes(10**exp, 10**(exp+1)))

public_key, private_key, N = get_keys()

st.header('meine Schlüssel')

st.write('öffentlicher Schlüssel - dieser Schlüssel ist für alle zugänglich')
st.code(str(public_key) + '-' + str(N))

st.write('privater Schlüssel - diesen Schlüssel NIE weitergeben')
st.code(private_key)

button = st.button('neues Schlüsselpaar erstellen')
if button:
    st.experimental_memo.clear()

st.header('verschlüsseln')
message = st.text_input('Klartext', '')
puplic_key_pair = st.text_input('öffentlicher Schlüssel', '')

if len(message) and len(puplic_key_pair):
    public_key2, N2 = puplic_key_pair.split('-')
    public_key2 = int(public_key2)
    N2 = int(N2)

    int_list = [get_char_index(c) + i for i, c in enumerate(message)]
    encrypted_list = [pow(m, public_key2, N2) for m in int_list]
    encrypted_string = get_encrypted_string(encrypted_list)

    st.write('Geheimtext')
    st.code(encrypted_string)

st.header('entschlüsseln')
encrypted_string = st.text_input('Geheimtext', '')
private_key = st.text_input('privater Schlüssel', '')

if len(encrypted_string) and len(private_key):
    private_key = int(private_key)
    encrypted_list = split_encrypted_string(encrypted_string, N)
    decrypted_list = [pow(m, private_key, N) for m in encrypted_list]
    message = ''.join([get_char(m-i) for i, m in enumerate(decrypted_list)])

    st.write('Klartext:', message)







d = primes[3]
