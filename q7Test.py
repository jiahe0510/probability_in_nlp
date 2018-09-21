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

english_file = Readfile.Readfile(path_en, 'English')
english_file.change_str2word()
# print(english_file.word_file)
english_file.build_word_dic()
english_file.build_probability()
english_file.test_word_dictionary()
english_file.build_letter_dic()
english_file.build_letter_probability()

french_file = Readfile.Readfile(path_fr, 'French')
french_file.change_str2word()
# print(french_file.word_file)
french_file.build_word_dic()
french_file.build_probability()
french_file.test_word_dictionary()
french_file.build_letter_dic()
french_file.build_letter_probability()

german_file = Readfile.Readfile(path_gr, 'German')
german_file.change_str2word()
# print(german_file.word_file)
german_file.build_word_dic()
german_file.build_probability()
german_file.test_word_dictionary()
german_file.build_letter_dic()
german_file.build_letter_probability()

test_file = Readfile.Readfile(path_test, 'English')

result_file = Readfile.Readfile(path_res, 'English')


def test(model1dic, model1uni, model1total, model2dic, model2uni, model2total, model3dic, model3uni, model3total,
         test_file, test_result, write_file_path):

    newf = open(write_file_path, 'w')
    p = ProbCalculate.ProbCalculate()
    index = 1
    accuate = 0
    total = 0
    for line in test_file:

        total += 1
        prob_en = p.regular_prob_cal(model1dic, model1uni, model1total, line)
        prob_fr = p.regular_prob_cal(model2dic, model2uni, model2total, line)
        prob_gr = p.regular_prob_cal(model3dic, model3uni, model3total, line)
        prob_final = float(max(prob_en, prob_gr, prob_fr))

        print(prob_en, prob_fr, prob_gr)
        if prob_en > prob_fr and prob_en > prob_gr:
            res_str = "EN"
        elif prob_fr > prob_gr:
            res_str = "FR"
        else:
            res_str = "GR"

        test_str = str(test_result[total])
        print(res_str, test_str)
        newf.write(str(index)+". "+res_str+"\n")
        if test_str.count(str(res_str)) > 0:
            accuate += 1
            if prob_final == 0:
                accuate -= 1
        index += 1
    print(accuate, ",", total)
    print("Accuracy is: ", float(accuate) / float(total)*100, "%")
    newf.write("Accuracy is: " + str(float(accuate) / float(total)*100)+"%")

# print(german_file.letter_unigram)
test(english_file.letter_dictionary, english_file.letter_unigram, english_file.totalletter,
     french_file.letter_dictionary, french_file.letter_unigram, french_file.totalletter,
     german_file.letter_dictionary, german_file.letter_unigram, german_file.totalletter,
     test_file.sentence_file, result_file.sentence_file, '/Users/jiahezhao/Desktop/GWU/NLP/Homework1/q7.txt')



