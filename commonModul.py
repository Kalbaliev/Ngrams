from collections import Counter
import math

def openfile(filename):
    with open(filename,"r",encoding="UTF-8-sig") as file :
      return str(file.read())
        