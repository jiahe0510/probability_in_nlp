from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from string import punctuation
from string import ascii_uppercase
from string import digits
from nltk.stem import porter


class Readfile:

    def __init__(self, path, lang):
        input_file = open(path, 'r')
        self.sentence_file = []
        self.punc_word = set(punctuation)
        self.word_file = []
        self.word_dictionary = {}
        self.letter_dictionary = {}
        self.word_set = set()
        self.totalword = 0
        self.totalletter = 0
        self.word_unigram = {"<s>": 0, "</s>": 0}
        self.letter_unigram = {}
        self.letter_set = set()
        self.turing_prob = {}
        self.trigram_dic = {}
        self.word_index_dic = {}
        self.index_word_dic = {}
        self.stop_word = set(stopwords.words(lang))

        for lines in input_file:
            self.sentence_file.append(lines)

    def change_str2word(self):
        # word_file is a 2D array, which each array contains only one sentence.
        # this function is to transfer a paragraph to several senctences
        for line in self.sentence_file:
            sent_token = sent_tokenize(line)
            for singleSentence in sent_token:
                word_tok = word_tokenize(singleSentence)
                temparr = []
                temparr.append("<s>")
                self.word_unigram["<s>"] += 1
                for word in word_tok:
                    if word not in self.punc_word:
                        self.__build_letter_unigram(word)
                        temparr.append(word)
                        if word in self.word_unigram:
                            self.word_unigram[word] += 1
                        else:
                            self.word_unigram[word] = 1
                temparr.append("</s>")
                self.word_unigram["</s>"] += 1
                self.word_file.append(temparr)

    def build_word_dic(self):
        ps = porter.PorterStemmer()
        index = 1
        for line in self.word_file:
            for word in line:
                self.word_set.add(word)
                word2 = ps.stem(word)
                if word2 not in self.word_index_dic and word2 not in self.stop_word:
                    self.word_index_dic[word2] = index
                    self.index_word_dic[index] = word2
                    index += 1
        self.totalword = len(self.word_set)

        for word in self.word_set:
            temp_dict = {}
            for next_word in self.word_set:
                temp_dict[next_word] = 0

            self.word_dictionary[word] = temp_dict

    def build_probability(self):
        for line in self.word_file:
            length = len(line)
            start = 1
            while start < length:
                self.word_dictionary[line[start - 1]][line[start]] += 1
                start += 1

    def test_word_dictionary(self):
        # print(self.word_dictionary["<s>"])
        for key in self.word_dictionary:
            temp_dic = self.word_dictionary[key]
            for seckey in temp_dic:
                if temp_dic[seckey] != 0:
                    print("Ah!!Works!!")
                    return
        print("suck!")

    def turing_count(self, k):
        turing = {}
        for key in self.word_dictionary:
            for sec_key in self.word_dictionary[key]:
                count = self.word_dictionary[key][sec_key]
                if count in turing:
                    turing[count] += 1
                else:
                    turing[count] = 1
        for c in range(0, k):
            temp_up = (c + 1) * (turing[c + 1] / turing[c]) - c * k * turing[k] / turing[0]
            temp_down = 1 - k * turing[k] / turing[0]
            self.turing_prob[c] = float(temp_up / temp_down)

    def build_trigram_dic(self):
        temp_set = self.word_index_dic.keys()
        for w1 in temp_set:
            firstdic = {}
            for w2 in temp_set:
                seconddic = {}
                for w3 in temp_set:
                    seconddic[self.word_index_dic[w3]] = 0
                firstdic[self.word_index_dic[w2]] = seconddic
            self.trigram_dic[self.word_index_dic[w1]] = firstdic

    def build_trigram_probability(self):
        print("Build trigram probability works")
        for line in self.word_file:
            length = len(line)
            start = 2
            while start < length:
                self.trigram_dic[line[start - 2]][line[start - 1]][line[start]] += 1
                start += 1

# -------------------------  functions below are used for letter bigram  ------------------------

    def __build_letter_unigram(self, word):
        for i in word:
            if i in self.punc_word or i in set(digits):
                continue
            if i in set(ascii_uppercase):
                i = i.lower()
            if i in self.letter_unigram:
                self.letter_unigram[i] += 1
            else:
                self.letter_unigram[i] = 1
            self.letter_set.add(i)

    def build_letter_dic(self):
        self.totalletter = len(self.letter_set)
        for letter in self.letter_set:
            temp_dict = {}
            for next_letter in self.letter_set:
                temp_dict[next_letter] = 0

            self.letter_dictionary[letter] = temp_dict

    def build_letter_probability(self):
        for line in self.sentence_file:
            word_token = word_tokenize(line)
            for word in word_token:
                if word not in self.punc_word:
                    length = len(word)
                    start = 1
                    while start < length:
                        if word[start - 1] in self.letter_unigram and word[start] in self.letter_unigram:
                            self.letter_dictionary[word[start - 1]][word[start]] += 1
                        start += 1
