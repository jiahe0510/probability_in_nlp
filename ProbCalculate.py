from nltk import word_tokenize, sent_tokenize
from string import punctuation
from string import digits


class ProbCalculate:

    punc_word = set(punctuation)

#   The below function is used for letter-bigram function
    def regular_prob_cal(self,dictionary, unigram, total, word_array):
        probability = 1
        sent_token = sent_tokenize(word_array)
        for singleSentence in sent_token:
            word_tok = word_tokenize(singleSentence)
            # print(word_tok)
            for word in word_tok:
                if word[0] in set(digits):
                    continue
                if word not in self.punc_word:

                    length = len(word)
                    start = 1
                    while start < length:
                        first_c = word[start - 1].lower()
                        second_c = word[start].lower()
                        if first_c in self.punc_word or second_c in self.punc_word:
                            start += 1
                            continue
                        if first_c in dictionary and second_c in dictionary[first_c]:
                            temp = dictionary[first_c][second_c]
                        else:
                            temp = 0
                        if first_c not in unigram:
                            probability *= 0
                        else:
                            probability *= temp / unigram[first_c]
                        start += 1

        return float(probability)

#   The below function is used for add one smooth function
    def prob_cal_add_one(self, dictionary, unigram, total, word_array):
        probability = 1
        sen_array = self.__change_word_array(word_array)
        for sen in sen_array:
            if sen[0] == '<s>' and sen[1] == '</s>': continue
            length = len(sen)
            start = 1
            while start < length:
                if sen[start - 1] in dictionary and sen[start] in dictionary[sen[start - 1]]:
                    temp = dictionary[sen[start - 1]][sen[start]] + 1
                else:
                    temp = 1
                if temp == 0: temp = 1
                if sen[start - 1] not in unigram:
                    probability *= temp / total
                else:
                    probability *= temp / unigram[sen[start - 1]]
                start += 1

        return float(probability)

#   The below function is used for turing smooth function
    def turing_prob(self, dictionary, unigram, total, word_array, turing, k):

        probability = 1
        sen_array = self.__change_word_array(word_array)
        for sen in sen_array:
            if sen[0] == '<s>' and sen[1] == '</s>':
                continue
            length = len(sen)
            start = 1
            while start < length:
                if sen[start - 1] in dictionary and sen[start] in dictionary[sen[start - 1]]:
                    temp = dictionary[sen[start - 1]][sen[start]]
                    if temp < k:
                        temp = turing[temp]
                else:
                    temp = turing[0]
                if sen[start - 1] not in unigram:
                    probability *= temp / total
                else:
                    probability *= temp / unigram[sen[start - 1]]
                start += 1
        return float(probability)

#   The function below is used for katz-backoff function
    def katz_trigram(self, dictionary, dictionary3D, unigram, word_index_dic, total, word_array, alpha1, alpha2):
        probability = 1
        sen_array = self.__change_word_array(word_array)
        for sen in sen_array:
            if sen[0] == '<s>' and sen[1] == '</s>':
                continue
            length = len(sen)
            start = 2
            while start < length:
                w1, w2, w3 = sen[start-2], sen[start-1], sen[start]

                if w1 in word_index_dic:
                    d1 = word_index_dic[w1]
                else:
                    d1 = 0
                if w2 in word_index_dic:
                    d2 = word_index_dic[w2]
                else:
                    d2 = 0
                if w3 in word_index_dic:
                    d3 = word_index_dic[w3]
                else:
                    d3 = 0

                if d1 in dictionary3D and d2 in dictionary3D[d1] and d3 in dictionary3D[d1][d2] and dictionary3D[d1][d2][d3] > 0:
                    temp = dictionary3D[d1][d2][d3] / dictionary[w1][w2]
                else:
                    if w2 in dictionary and w3 in dictionary[w2] and dictionary[w2][w3] > 0:
                        temp = dictionary[w2][w3] / unigram[w2] * alpha1
                    else:
                        if w3 in unigram:
                            temp = unigram[w3] / total * alpha2
                        else:
                            temp = 1 / total * alpha2

                probability *= temp
                start += 1

        return float(probability)

    def __change_word_array(self, word_array):
        sen_array = []
        sent_token = sent_tokenize(word_array)

        for singleSentence in sent_token:
            word_tok = word_tokenize(singleSentence)
            temparr = []
            temparr.append("<s>")

            for word in word_tok:
                if word not in self.punc_word:
                    temparr.append(word)
            temparr.append("</s>")
            sen_array.append(temparr)

        return sen_array
