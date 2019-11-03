from collections import Counter
import math
from termcolor import colored
    




class Unigram:

    def __init__(self):

        #OPEN FILES TRAIN AND TEST
        self.text=self.openfile("train.txt")
        self.test_text=self.openfile("test2.txt")
        
        
        self.unigram_fr=Counter(list(self.unigram_frequency()))
        self.unigram_fr=dict(self.unigram_fr)
        self.vocab_unigram=list(self.unigram_fr.keys())
        self.vocab_unigram_size=len(self.vocab_unigram) #vocab for unigram
       
        
    def openfile(self,filename):
        with open(filename,"r",encoding="UTF-8-sig") as file :
            return str(file.read())

    def unigram_frequency(self):
        self.unigram_corpus_length=0 #corpus length
        self.sentences=self.text.split("\n")
        for sentence in self.sentences:
            for word in sentence.split(" "):
                self.unigram_corpus_length+=1
                yield word

    def unigram_test_frequency_words(self):
        
        self.test_sentences=self.test_text.split("\n")
        self.test_words=[]
        for sentence in self.test_sentences:
            self.test_words+=sentence.split(" ")
        return self.test_words
        
    def unigram_word_prob(self):
        self.probability_of_words_unigram=1
        
        for word in self.test_words:
            if(word!='<s>' and word!='</s>'):
                self.unigram_numerator=self.unigram_fr.get(word,0)
                self.unigram_dominator=self.unigram_corpus_length
                self.probability_of_word_unigram=(self.unigram_numerator/self.unigram_dominator)
                self.probability_of_words_unigram*=self.probability_of_word_unigram

        return self.probability_of_words_unigram

    def unigram_word_prob_smth(self):
        self.probability_of_words_unigram_smth=1
        for word in self.test_words:
            if(word!='<s>' and word!='</s>'):
                self.unigram_numerator_smth=self.unigram_fr.get(word,0)+1 
                self.unigram_dominator_smth=self.unigram_corpus_length+self.vocab_unigram_size  #is it correct ?  vocabsize + corpus length 
                self.probability_of_unigram_smth=(self.unigram_numerator_smth/self.unigram_dominator_smth)
                self.probability_of_words_unigram_smth*=self.probability_of_unigram_smth
        return self.probability_of_words_unigram_smth

    def perplexity_unigram(self):
       self.unigram_prob=self.unigram_word_prob() #prob
       self.unigram_prob_smth=self.unigram_word_prob_smth() #prob laplace
       self.test_sentence_corpus_length=len(self.test_words) #word size = -1/N deki N
      
       try:
           self.pp_unigram=math.pow(self.unigram_prob,(-1/self.test_sentence_corpus_length))
       except ValueError:
           self.pp_unigram="ERROR"
       
       self.pp_unigram_smth=math.pow(self.unigram_prob_smth,(-1/self.test_sentence_corpus_length))
       
       
       return self.pp_unigram,self.pp_unigram_smth # unsmth , smth

class Bigram(Unigram):
     
    def __init__(self):
        Unigram.__init__(self) #unigram in init call
        
        # iterator_bigram = iter(self.bigram_frequency())
        # self.bigram_fr=commonModul.Counter(next(iterator_bigram))
        self.bigram_fr=Counter(self.bigram_frequency())
        self.bigram_fr=dict(self.bigram_fr)
       
        
        self.test_pairs=self.bigram_test_frequency_pairs()
        self.test_words=self.unigram_test_frequency_words() #unigram model using despite of written on bigram model
    def bigram_frequency(self):

        sentences=self.text.split("\n") #unigram init call
        self.words=[]
        self.pairs=[]
        for sentence in sentences:
            self.words.append(sentence.split(" "))
        for word in self.words:
            for w,next_w in zip(word,word[1:]):
                pair=(w,next_w)
                yield pair
                # self.pairs.append(pair)
        # yield self.pairs
        # return self.pairs


    def bigram_test_frequency_pairs(self):
 
        test_sentences=self.test_text.split("\n") #unigram init call
        self.test_words=[]
        self.test_pairs=[]
        for sentence in test_sentences:
            self.test_words.append(sentence.split(" "))
        for word in self.test_words:
            for w,next_w in zip(word,word[1:]):
                pair=(w,next_w)
                self.test_pairs.append(pair)
        return self.test_pairs
        
    
   
       

# There is Zero division problem for Test Data 1 but it is working in test data 2
    def bigram_word_prob(self):
        self.probability_of_words_bigram=1
      
        numerators=[]
        denominators=[]
        counter=0
        for pair in self.test_pairs:
            self.bigram_numerator=self.bigram_fr.get(pair,0)
            
            numerators.append(self.bigram_numerator)
           
        for word in self.test_words:
            if(counter<len(self.test_pairs)):
                self.bigram_denominator=self.unigram_fr.get(word,0) 
            
                denominators.append(self.bigram_denominator)
                counter+=1

        try:

            for n,d in zip(numerators,denominators):
                    self.probability_of_bigram=n/d
                    self.probability_of_words_bigram*=self.probability_of_bigram
       
            return self.probability_of_words_bigram
        except ZeroDivisionError:
            self.probability_of_words_bigram="ERROR"
            return self.probability_of_words_bigram 

    def bigram_word_prob_smth(self):

        self.probability_of_words_bigram_smth=1
        numerators=[]
        denominators=[]
        counter=0
        for pair in self.test_pairs:
            self.bigram_numerator=self.bigram_fr.get(pair,0)
            numerators.append(self.bigram_numerator)
        for word in self.test_words:
            if(counter<len(self.test_pairs)):
                self.bigram_denominator=self.unigram_fr.get(word,0) 
                denominators.append(self.bigram_denominator)
                counter+=1

        for n,d in zip(numerators,denominators):
                self.probability_of_bigram=(n+1)/(d+self.vocab_unigram_size)
                self.probability_of_words_bigram_smth*=self.probability_of_bigram
        
      
        return self.probability_of_words_bigram_smth

    def perplexity_bigram(self):
       self.bigram_prob=self.bigram_word_prob() #prob
       self.bigram_prob_smth=self.bigram_word_prob_smth() #prob laplace
       self.test_sentence_corpus_length=len(self.test_pairs) #pair size= -1/N deki N


       try:
           self.pp_bigram=math.pow(self.bigram_prob,(-1/self.test_sentence_corpus_length))
           
       except (ValueError,TypeError):
           self.pp_bigram="ERROR"

       
       self.pp_bigram_smth=math.pow(self.bigram_prob_smth,(-1/self.test_sentence_corpus_length)) # 
       
       
       return self.pp_bigram,self.pp_bigram_smth # unsmth , smth


    

obj_bi=Bigram()

print("")
print("")
print (colored("----------------------------------------------------------------",'yellow'))
print (colored("-------------------- PROBABILITY","yellow"),colored("(UNIGRAM)","magenta"),colored("---------------------",'yellow'))
print (colored("----------------------------------------------------------------",'yellow'))

prob_unigram=obj_bi.unigram_word_prob()
prob_smth_unigram=obj_bi.unigram_word_prob_smth()

print(colored("P(unsmoothed) =","green"),colored(prob_unigram,"green"))
print(colored("P(smoothed) =","green"),colored(prob_smth_unigram,"green"))


print (colored("----------------------------------------------------------------",'yellow'))
print (colored("-------------------- PERPLEXITY","yellow"),colored("(UNIGRAM)","magenta"),colored("----------------------",'yellow'))
print (colored("----------------------------------------------------------------",'yellow'))
pp_unigram=obj_bi.perplexity_unigram()[0]
pp_unigram_smth=obj_bi.perplexity_unigram()[1]
if(pp_unigram=="ERROR"):
    print(colored("ERROR: Ehtimal sıfıra bərabər olduğu üçün qüvvətə yüksəldilməsi (yəni kök alta salınması N-ci dərəcədən) mümkün deyil!","red"))
    print(colored("PP(unsmoothed) =","green"),colored("ERROR","red"),colored("\nPP(smoothed) =","green"),colored(pp_unigram_smth,"green"))
else:
    print(colored("PP(unsmoothed)=","green"),colored(pp_unigram,"green"),colored("\nPP(smoothed)=","green"),colored(pp_unigram_smth,"green"))



print (colored("----------------------------------------------------------------",'yellow'))
print (colored("--------------------- PROBABILITY","yellow"),colored("(BIGRAM)","magenta"),colored("---------------------",'yellow'))
print (colored("----------------------------------------------------------------",'yellow'))

prob_bigram=obj_bi.bigram_word_prob()
prob_smth_bigram=obj_bi.bigram_word_prob_smth()
if(prob_bigram=="ERROR"):
   print (colored("ERROR: Bigram modeldə adi ehtimalın hesablanması zamanı Test DATA set səbəbindən sıfıra bölmə yoxdur!","red"))
   print(colored("P(unsmoothed) =","green"),colored(prob_bigram,"red"))
   print(colored("P(smoothed) =","green"),colored(prob_smth_bigram,"green"))
else:   
   print(colored("P(unsmoothed) =","green"),colored(prob_bigram,"green"))
   print(colored("P(smoothed) =","green"),colored(prob_smth_bigram,"green"))






print (colored("----------------------------------------------------------------",'yellow'))
print (colored("--------------------- PERPLEXITY","yellow"),colored("(BIGRAM)","magenta"),colored("----------------------",'yellow'))
print (colored("----------------------------------------------------------------",'yellow'))
pp_bigram=obj_bi.perplexity_bigram()[0]
pp_bigram_smth=obj_bi.perplexity_bigram()[1]
if(pp_bigram=="ERROR"):
    print(colored("ERROR: Ehtimal sıfıra bərabər olduğu(və ya heç olmadığı) üçün qüvvətə yüksəldilməsi (yəni kök alta salınması N-ci dərəcədən) mümkün deyil!","red"))
    # print(colored("ERROR: Ehtimalı göstərilməyən ","red"))
    print(colored("PP(unsmoothed) =","green"),colored("ERROR","red"),colored("\nPP(smoothed) =","green"),colored(pp_bigram_smth,"green"))
else:
    print(colored("PP(unsmoothed)=","green"),colored(pp_bigram,"green"),colored("\nPP(smoothed)=","green"),colored(pp_bigram_smth,"green"))

print("")
print("")




     


