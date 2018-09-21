import Readfile
import ProbCalculate

path_en = '/Users/jiahezhao/Desktop/GWU/NLP/Homework1/EN.txt'
lang_en = 'English'
path_fr = '/Users/jiahezhao/Desktop/GWU/NLP/Homework1/FR.txt'
lang_fr = 'French'
path_gr = '/Users/jiahezhao/Desktop/GWU/NLP/Homework1/GR.txt'
lang_gr = 'German'
path_test = '/Users/jiahezhao/Desktop/GWU/NLP/Homework1/LangID.test.txt'
lang_test = 'English'
path_res = '/Users/jiahezhao/Desktop/GWU/NLP/Homework1/LangID.gold.txt'
k = 20

english_file = Readfile.Readfile(path_en, 'English')
english_file.change_str2word()
# print(english_file.word_file)
english_file.build_word_dic()
english_file.build_probability()
english_file.test_word_dictionary()
english_file.turing_count(k)

french_file = Readfile.Readfile(path_fr, 'French')
french_file.change_str2word()
# print(french_file.word_file)
french_file.build_word_dic()
french_file.build_probability()
french_file.test_word_dictionary()
french_file.turing_count(k)

german_file = Readfile.Readfile(path_gr, 'German')
german_file.change_str2word()
# print(german_file.word_file)
german_file.build_word_dic()
german_file.build_probability()
german_file.test_word_dictionary()
german_file.turing_count(k)

test_file = Readfile.Readfile(path_test, 'English')

result_file = Readfile.Readfile(path_res, 'English')

write_file_path = '/Users/jiahezhao/Desktop/GWU/NLP/Homework1/q9.txt'

newf = open(write_file_path, 'w')
p = ProbCalculate.ProbCalculate()
index = 1
accuate = 0
total = 0
for line in test_file.sentence_file:

    total += 1
    prob_en = p.turing_prob(english_file.word_dictionary, english_file.word_unigram, english_file.totalword,
                            line, english_file.turing_prob, k)
    prob_fr = p.turing_prob(french_file.word_dictionary, french_file.word_unigram, french_file.totalword,
                            line, french_file.turing_prob, k)
    prob_gr = p.turing_prob(german_file.word_dictionary, german_file.word_unigram, german_file.totalword,
                            line, german_file.turing_prob, k)
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