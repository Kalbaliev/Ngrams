import commonModul

    

class Unigram:

    def unigram_frequency(self):
        self.text=commonModul.openfile("train.txt")
        self.sentences=self.text.split("\n")
        for sentence in self.sentences:
            for word in sentence.split(" "):
                yield word

    def unigram_test_frequency_words(self):
        self.test_text=commonModul.openfile("test2.txt")
        self.test_sentences=self.test_text.split("\n")
        self.test_words=[]
        for sentence in self.test_sentences:
            self.test_words+=sentence.split(" ")
        return self.test_words
    def __init__(self):

        
        self.unigram_fr=commonModul.Counter(list(self.unigram_frequency()))
        self.unigram_fr=dict(self.unigram_fr)
        self.vocab_unigram=list(self.unigram_fr.keys())
        self.corpus_length_unigram=len(self.vocab_unigram) #corpus length for unigram
        

        # self.unigram_word_prob(self.unigram_test_frequency_words()) #unsmoothed
        # self.unigram_word_prob_smoothing(self.unigram_test_frequency_words()) #smoothed Laplace (Add one method)
    
    def unigram_word_prob(self,words):
        self.probability_of_words_unigram=1
        for word in words:
            self.unigram_numerator=self.unigram_fr.get(word,0)
            self.unigram_dominator=self.corpus_length_unigram #is ist correct ?
            self.probability_of_word_unigram=(self.unigram_numerator/self.unigram_dominator)
            self.probability_of_words_unigram*=self.probability_of_word_unigram
        print(self.probability_of_words_unigram)

    def unigram_word_prob_smoothing(self,words):
        self.probability_of_words_unigram_smth=1
        for word in words:
            self.unigram_numerator_smth=self.unigram_fr.get(word,0)+1 
            self.unigram_dominator_smth=(self.corpus_length_unigram*2)-2  #is it correct ? 
            self.probability_of_unigram_smth=(self.unigram_numerator_smth/self.unigram_dominator_smth)
            self.probability_of_words_unigram_smth*=self.probability_of_unigram_smth
        print(self.probability_of_words_unigram_smth)


        
obj_uni=Unigram()
     


