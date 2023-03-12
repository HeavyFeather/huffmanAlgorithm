from collections import Counter
from collections import namedtuple
import pickle
import heapq as hq
import struct


class Leaf(namedtuple("Leaf", ["char"])): # Описание листьев древа
    def step(self, code, encSimb):
        code[self.char] = encSimb or "0"

class Node(namedtuple("Node", ["left", "right"])): # Описание промежуточных узлов древа
    def step(self, code, encSimb):
        self.left.step(code, encSimb + '0')
        self.right.step(code, encSimb + '1')

def huffman_encoding(s):  # Фукция по созданию словаря с кодами 
    pq = [] #priority queue

    for char, frequency in Counter(s).items():
        pq.append((frequency, len(pq), Leaf(char)))

    hq.heapify(pq) # hq = heapq

    count = len(pq)

    while(len(pq) > 1):
        freq1, count1, left = hq.heappop(pq)
        freq2, count2, right = hq.heappop(pq)
        hq.heappush(pq, (freq1 + freq2, count, Node(left, right)))
        count += 1

    code = {}

    if pq:
        [(r_freq, r_count, root)] = pq
        root.step(code, "")

    return code


def decode_writing(): # Функция для декодирования и записи
    filenameIn = input("Enter name of file you want to decode: ")
     
    with open(filenameIn, 'rb') as f: # Берём дамп словаря с кодировкой и само сообщение
        code_new = pickle.load(f)
        unpack = f.read()

    code_unpack = ''

    for i in unpack:
        code_unpack += '{0:08b}'.format(i)

    fileName = filenameIn.replace(".encoded", "")
    fpOut = open(fileName, 'w')
    
    simbCode = ""
    for char in code_unpack:  # Цикл идущий по закодированному сообщению
        simbCode += char  
        for enc_char in code_new: # цикл, сверящий набор двоичных символов с элементами словаря кодировки
            if(simbCode == code_new.get(enc_char)):
                fpOut.write(enc_char)  # сразу записываем в файл
                simbCode = ""
                break

    print("[+] Decoding of " + fileName + " complited!!!") 
    fpOut.close()

def code_writing():
    fileName = input("Enter name of file you want to encode: ")
    fpIn = open(fileName, "r")

    s = fpIn.read() # Текст сообщения
    
    code = huffman_encoding(s) # Здесь лежит словарь с кодами
    
    print(code) 
    
    pack = b''
    
    encM = ''.join(code[char] for char in s)

    for i in range(0, len(encM), 8):
        pack += struct.pack('B', int(encM[i: i + 8], 2))


    with open(fileName + ".encoded", 'wb') as f: # Дампаем словарь с кодами символов, затем записываем сообщение
        pickle.dump(code, f)
        f.write(pack)

    print("[+] Encoding complete\nCreated file: " + fileName + ".encoded")

    fpIn.close()


def main():
    i = input("Enter 1 to encrypt, or 2 to decrypt: ")
    if (int(i) == 1):
        code_writing()
    elif (int(i) == 2):
        decode_writing()

if __name__ == "__main__":
    main()
