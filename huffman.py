from collections import Counter
from collections import namedtuple
import pickle
import heapq as hq
import os


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
    filenameIn = input("Enter name of file you want to decode without '.encoded': ")
    fpIn = open(filenameIn + ".encoded", "r")
    fpOut = open(filenameIn, "w")
    
    with open(filenameIn + '.pickle', 'rb') as f: # Берём дамп словаря с кодировкой 
        code_new = pickle.load(f)

    message = fpIn.read()

    simbCode = ""
    for char in message:  # Цикл идущий по закодированному сообщению
        simbCode += char  
        for enc_char in code_new: # цикл, сверящий набор двоичных символов с элементами словаря кодировки
            if(simbCode == code_new.get(enc_char)):
                fpOut.write(enc_char)  # сразу записываем в файл
                simbCode = ""
                break
    print("[+] Decoding of " + filenameIn + ".encoded complited!!!") 
    os.remove(filenameIn + '.pickle') # Удаляем словарь с кодировкой за безнабностью
    print("Decoder file: " + filenameIn + ".pickle removed")
    fpIn.close()
    fpOut.close()
    os.remove(filenameIn + '.encoded') # Удалем закодированный файл
    print("Encoded file: " + filenameIn + ".encoded removed")

def code_writing():
    fileName = input("Enter name of file you want to encode: ")
    fileNameOut = fileName + ".encoded"
    fpIn = open(fileName, "r")
    fpOut = open(fileNameOut, "w")
    
    s = fpIn.read() # Текст сообщения
    
    code = huffman_encoding(s) # Здесь лежит словарь с кодами
    
    encoded_message = "".join(code[char] for char in s) #Закодированное сообщение
    
    with open(fileName + ".pickle", 'wb') as f: # Дампаем словарь с кодами символов
        pickle.dump(code, f)

    fpOut.write(encoded_message) # Запись сообщения в файл
    
    print("[+] Encoding complete\nCreated file: " + fileNameOut + "\nCreated code file: " + fileName + ".pickle")

    fpIn.close()
    fpOut.close()


def main():
    i = input("Enter 1 to encrypt, or 2 to decrypt: ")
    if (int(i) == 1):
        code_writing()
    elif (int(i) == 2):
        decode_writing()

if __name__ == "__main__":
    main()
