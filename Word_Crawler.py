import requests
from bs4 import BeautifulSoup
import os
from time import sleep
import threading
from queue import Queue
global a_list
global b_list
a_list=[]
b_list=[]
q=Queue()

def permutations(string, step = 0):
    if step == len(string):
        a_list.append(string)

    for i in range(step, len(string)):
        string_copy = [character for character in string]
        string_copy[step], string_copy[i] = string_copy[i], string_copy[step]
        permutations(string_copy, step + 1)
    
def browse(string):
    string=str(string)
    l=len(string)
    url="http://www.dictionary.com/browse/"+string+"?s=ts"
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text,'lxml')
    s=""
    for a in soup.find_all('title')[0].get_text():
        s+=a
    b_list.append(s[:-(28+l)])

def threader():
    worker=q.get()
    browse(worker)
    q.task_done()
    
def main():
    try:
        a=input("Enter the string :")
        permutations(a)
        z=[]
        n=int(input("Enter the length of the word to search(eg. 3): "))
        s=""
        for i in range(len(a_list)):
            s=""
            for j in range(n):
                s+=a_list[i][j]
            z.append(s)
        sleep(1)
        print()
        print("Please Wait while Parsing the string to the internet")
        print("and getting the correct and existing only elements.")
        alpha=list(set(z))
        for i in alpha:
            q.put(i)

        for i in range(len(alpha)):
            t=threading.Thread(target=threader)
            t.daemon=True
            t.start()
        q.join()   
        print()
        asd=list(set(b_list))
        print()
        asd.remove("")
        for j in range(len(asd)):
            print("{}. {}".format(j+1,asd[j]))
            
        print()
        input("Enter to continue for the next string")
        os.system('cls')
        a_list.clear()
        b_list.clear()
        main()
    except Exception as e:
        print("\n\n")
        print("Error Ocured!!!\n")
        print(e)
        print()
        main()

if __name__=="__main__":
    main()
