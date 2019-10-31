import commonModul
import unigramModel
    

class Bigram:

    def bigram_frequency(self):
        self.text=commonModul.openfile("train.txt")
        sentences=self.text.split("\n")
        self.words=[]
        self.pairs=[]
        for sentence in sentences:
            self.words.append(sentence.split(" "))
        for word in self.words:
            for w,next_w in zip(word,word[1:]):
                pair=(w,next_w)
                self.pairs.append(pair)
        # yield self.pairs
        return self.pairs


    def bigram_test_frequency_pairs(self):
        self.test_text=commonModul.openfile("test2.txt")
        test_sentences=self.test_text.split("\n")
        self.test_words=[]
        self.test_pairs=[]
        for sentence in test_sentences:
            self.test_words.append(sentence.split(" "))
        for word in self.test_words:
            for w,next_w in zip(word,word[1:]):
                pair=(w,next_w)
                self.test_pairs.append(pair)
        return self.test_pairs
        

    def __init__(self):

        # iterator_bigram = iter(self.bigram_frequency())
        # self.bigram_fr=commonModul.Counter(next(iterator_bigram))
        self.bigram_fr=commonModul.Counter(self.bigram_frequency())
        self.bigram_fr=dict(self.bigram_fr)
        self.vocab_bigram=list(self.bigram_fr.keys())
        self.corpus_length_bigram=len(self.vocab_bigram)

        # unigram
        self.corpus_length_unigram=unigramModel.obj_uni.corpus_length_unigram # from unigrammodel 
        self.unigram_fr=unigramModel.obj_uni.unigram_fr
        
      
        self.bigram_word_prob(self.bigram_test_frequency_pairs(),unigramModel.obj_uni.unigram_test_frequency_words())

        self.bigram_word_prob_smth(self.bigram_test_frequency_pairs(),unigramModel.obj_uni.unigram_test_frequency_words())
        # self.bigram_word_prob(('<s>', 'BƏLİ'),'<s>')



# There is Zero division problem for Test Data 1 but it is working in test data 2
    def bigram_word_prob(self,pairs,words):
        self.probability_of_words_bigram=1
        numerators=[]
        denominators=[]
        counter=0
        for pair in pairs:
            self.bigram_numerator=self.bigram_fr.get(pair,0)
            numerators.append(self.bigram_numerator)
        for word in words:
            if(counter<len(pairs)):
                self.bigram_denominator=self.unigram_fr.get(word,0) 
                denominators.append(self.bigram_denominator)
                counter+=1

        try:

            for n,d in zip(numerators,denominators):
                    self.probability_of_bigram=n/d
                    self.probability_of_words_bigram*=self.probability_of_bigram
            print("1. Hesablama: Unsmoothed\nP =",self.probability_of_words_bigram)

        except ZeroDivisionError:
            
            print("1.Hesablama: \nBigram modelde adi ehtimalin hesablamasinda Test data sebebinden sifira bolme yoxdur")
            

    def bigram_word_prob_smth(self,pairs,words):
        self.probability_of_words_bigram_smth=1
        numerators=[]
        denominators=[]
        counter=0
        for pair in pairs:
            self.bigram_numerator=self.bigram_fr.get(pair,0)
            numerators.append(self.bigram_numerator)
        for word in words:
            if(counter<len(pairs)):
                self.bigram_denominator=self.unigram_fr.get(word,0) 
                denominators.append(self.bigram_denominator)
                counter+=1

        for n,d in zip(numerators,denominators):
                self.probability_of_bigram=(n+1)/(d+self.corpus_length_unigram)
                self.probability_of_words_bigram_smth*=self.probability_of_bigram
        
        print("2. Hesablama: Smoothed\nP =",self.probability_of_words_bigram_smth)

obj_bi=Bigram()
     