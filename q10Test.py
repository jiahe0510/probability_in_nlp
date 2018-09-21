import Readfile
import ProbCalculate

path_en = 'EN.txt'
lang_en = 'English'
path_fr = 'FR.txt'
lang_fr = 'French'
path_gr = 'GR.txt'
lang_gr = 'German'
path_test = 'LangID.test.txt'
lang_test = 'English'
path_res = 'LangID.gold.txt'

english_file = Readfile.Readfile(path_en, 'English')
english_file.change_str2word()
# print(english_file.word_file)
english_file.build_word_dic()
print(english_file.word_index_dic)
print(english_file.index_word_dic)
english_file.build_probability()
english_file.test_word_dictionary()
english_file.build_trigram_dic()
english_file.build_trigram_probability()

french_file = Readfile.Readfile(path_fr, 'French')
french_file.change_str2word()
# print(french_file.word_file)
french_file.build_word_dic()
french_file.build_probability()
french_file.test_word_dictionary()
french_file.build_trigram_dic()
french_file.build_trigram_probability()

german_file = Readfile.Readfile(path_gr, 'German')
german_file.change_str2word()
# print(german_file.word_file)
german_file.build_word_dic()
german_file.build_probability()
german_file.test_word_dictionary()
german_file.build_trigram_dic()
german_file.build_trigram_probability()

test_file = Readfile.Readfile(path_test, 'English')

result_file = Readfile.Readfile(path_res, 'English')

write_file_path = 'q10.txt'

newf = open(write_file_path, 'w')
p = ProbCalculate.ProbCalculate()
index = 1
accuate = 0
total = 0
alpha1 = 0.5
alpha2 = 0.05
for line in test_file.sentence_file:

    total += 1
    prob_en = p.katz_trigram(english_file.word_dictionary, english_file.trigram_dic,english_file.word_unigram,
                             english_file.word_index_dic, english_file.index_word_dic,
                             english_file.totalword, line, alpha1, alpha2)
    prob_fr = p.turing_prob(french_file.word_dictionary, french_file.trigram_dic, french_file.word_unigram,
                            french_file.word_index_dic, french_file.index_word_dic,
                            french_file.totalword, line, alpha1, alpha2)
    prob_gr = p.turing_prob(german_file.word_dictionary, german_file.trigram_dic, german_file.word_unigram,
                            german_file.word_index_dic, german_file.index_word_dic,
                            german_file.totalword, line, alpha1, alpha2)
    # prob_final = float(max(prob_en, prob_gr, prob_fr))
    print(prob_en, prob_fr, prob_gr)
    if prob_en > prob_fr and prob_en > prob_gr:
        res_str = "EN"
    elif prob_fr > prob_gr:
        res_str = "FR"
    else:
        res_str = "GR"

    test_str = str(result_file.sentence_file[total])
    print(res_str, test_str)
    newf.write(str(index) + ". " + res_str + "\n")
    if test_str.count(str(res_str)) > 0:
        accuate += 1
    index += 1
print(accuate, ",", total)
print("Accuracy is: ", float(accuate) / float(total) * 100, "%")
newf.write("Accuracy is: " + str(float(accuate) / float(total) * 100) + "%")