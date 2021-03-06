import socket
import threading
import random

#длина слова
wordlen=76

def convertToBinary(text, encoding='utf-8', errors='surrogatepass'):
	bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
	return bits.zfill(8* ((len(bits)+7) // 8))
	
	#return ''.join(format(ord(i), '08b') for i in test_str)
	#return ' '.join(format(ord(x), 'b') for x in test_str)
	#res = ' '.join(format(x, 'b') for x in bytearray(test_str, 'utf-8')) 
	#byte_array = "abc".encode()
    #binary_int = int.from_bytes(byte_array, 'big')
	#binary_string = bin(binary_int)
	#return binary_string
	




def addingBit(s):
        curpow = 0;
        while(2 ** curpow < len(s)):
            s.insert(2 ** curpow - 1, 0)
            curpow += 1
        return s


def wordCoding(a, num_mist):
        b = 1
        while b < len(a):
            for i in range(b - 1, len(a), b*2):
                for j in range(i, min(i+b, len(a)), 1):
                    a[b-1] = a[b-1] ^ a[j]
            b *= 2
        if num_mist == 1:
            i = random.randrange(len(a))
            a[i] = a[i] ^ 1
        if num_mist == 2:
            for j in range(len(a)):
                if (random.randrange(10) == 0):
                    a[j] = a[j] ^ 1
        return a





def hamCoding(s, num_mist ):
        ls = [int(s[i]) for i in range(len(s))]
        b = []
        code = ''
        for j in range(0, len(ls), wordlen):            
            a = ls[j : j + wordlen]
            a = addingBit(a)
            a =  wordCoding(a, num_mist)
            b += a
        for i in b:
            code += str(i)
        return code




HOST = '127.0.0.1'  
PORT = 65432        #порт

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #res = convertToBinary('привет hello')
    #print(res)
    print("Введите количество ошибок:")
    num_mist=int(input())
    mytext = open('txt1.txt', 'r', encoding = 'UTF-8').read()
    mytext = convertToBinary(mytext)
    mytext = hamCoding(mytext, num_mist)
    #print(mytext)
    s.sendall(mytext.encode())
    print("success send\n")
    mes=''
    data = s.recv(32768).decode()
print('Полученное сообщение от сервера:')
print(data)

