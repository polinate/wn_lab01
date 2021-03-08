import socket
import random

#длина слова
wordlen = 76


def convertBinaryToText(b):
	#return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(b)]*8))
	binary_int = int(b, 2)
	byte_number = (binary_int.bit_length()+7) // 8
	binary_array = binary_int.to_bytes(byte_number, 'big')
	#print(binary_array)
	ascii_text = binary_array.decode("utf-8")
	return ascii_text.rstrip()


   

   # print(ascii_text)
	#return ''.join([chr(int(s, 2)) for s in b.split()])




def wordCoding(a, num_mist):
        b = 1
        while b < len(a):
            for i in range(b - 1, len(a), b*2):
                for j in range(i, min(i+b, len(a)), 1):
                    a[b-1] = a[b-1]  ^ a[j]
            b *= 2
        if num_mist == 1:
            i = random.randrange(len(a))
            a[i] = a[i] ^ 1
        if num_mist == 2:
            for j in range(len(a)):
                if (random.randrange(10) == 0):
                    a[j] = a[j] ^ 1
        return a





def hamDecoding(s):
        ls = [int(s[i]) for i in range(len(s))]
        ch = ls.copy()
        wrong_words=0
        right_words=0
        hamlen=wordlen+7
        ans=''
        for j in range(0, len(ls), hamlen):
            a = ls[j : j + hamlen]
            cntmist = 0
            while True:
                curch = ch[j : j + hamlen]
                ipow = 0
                while 2 ** ipow < len(a):
                    a[2 ** ipow - 1] = 0
                    ipow += 1
                a = wordCoding(a,0)
                numbad = 0
                ipow = 0
                while 2 ** ipow < len(a):
                    if a[2 ** ipow - 1] != curch[2 ** ipow - 1]:
                        numbad += 2 ** ipow
                    ipow += 1
                ipow = 0
                if numbad == 0:
                    break
                f = True
                while 2 ** ipow < len(a):                
                    if numbad == 2 ** ipow:
                        f = False
                        break
                    ipow += 1
                if f == False:
                    break
                cntmist += 1
                if (numbad >= len(a)):
                    break 
                a[numbad - 1] = a[numbad - 1] ^ 1  
            if cntmist > 0:
                wrong_words += 1
            else:
                right_words += 1
            cursumbit = 0
            for i in range(len(a)):
                if (i == cursumbit):
                    cursumbit = (cursumbit + 1) * 2 - 1
                else:
                    ans += str(a[i])
 
        print('Всего слов: ', right_words+wrong_words)
        print('Количество слов без ошибок: ', right_words)
        print('Количество слов с ошибками: ', wrong_words)
        return ans




HOST = '192.168.0.76' 
PORT = 65432


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    mes=''
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(32768).decode()
            if not data:
                break
            mes += data
            mes=hamDecoding(data)
            mes = convertBinaryToText(mes)
            print("Полученное сообщение:")
            print(mes)
            conn.sendall(mes.encode())
conn.close()


