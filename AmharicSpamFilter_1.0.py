import l3
import sys
import codecs
import nltk
from l3.morpho.geez import *



print('\n'+ ">>> Amharic Spam Filter 1.0 <<<" + '\n'+ "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~" + '\n')


# -------------------------------------------------------------------------------------------------------------------
# Implementation of Morphological Anayzer Functions (Using our set of rules)

#function to transliterate a word from geez characters to latin characters
def geezsera(word):
	transtext=geez2sera (GEEZ_SERA ['am'][0],word)
	return transtext

#function to transliterate a word from latin to geez characters
def serageez(word):
	transtext=sera2geez (GEEZ_SERA ['am'][1],word)
	return transtext

#Morphological Analyzer to stem amharic words
def wordAnalyzer(word):
        #print(word+">>")
        word=geezsera(word)
        for rule in rules:
                mor=geezsera(rule[0])
                rplcd=geezsera(rule[1][0])
                rplcr=geezsera(rule[1][1])
                position=rule[2]

                if(position=='post'):
                        if(mor[0]=="'"):
                                mor=mor[1:]
                        if(word[-len(mor):]==mor):
                                word=word[:len(word)-len(mor)]
                elif(position=='pre'):
                        if (word[:len(mor)]==mor):
                                word=word[len(mor):]
        word=serageez(word)
        #print(word)
        return word
        
	






# --------------------------------------------------------------------------------------------
# Rule definitions for the "Analyzer" function. Includes affices and location of the affix(prefix or postfix)

rules = []

#Prefix Rules
rules.append(['ለ',['ለ',''],'pre'])
rules.append(['ተ',['ተ',''],'pre'])   
rules.append(['የ',['የ',''],'pre'])
rules.append(['ከ',['ከ',''],'pre'])
rules.append(['በ',['በ',''],'pre'])
rules.append(['አለ',['አለ',''],'pre'])
rules.append(['አል',['አል',''],'pre'])
rules.append(['ስለ',['ስለ',''],'pre'])
rules.append(['እየ',['እየ',''],'pre'])
rules.append(['ስለሚ',['ስለሚ',''],'pre'])
rules.append(['እንዳ',['እንዳ',''],'pre'])
rules.append(['እንዲ',['እንዲ',''],'pre'])
rules.append(['እስክ',['እስክ',''],'pre'])
rules.append(['ከነ',['ከነ',''],'pre'])
rules.append(['እንደ',['እንደ',''],'pre'])
rules.append(['እያ',['እያ',''],'pre'])





#Postfix Rules
rules.append(['ችን', ['ችን', ''], 'post'])
rules.append(['ኝ', ['ኝ', ''], 'post'])
rules.append(['ቸው',[' ቸው',''], 'post'])
rules.append(['ዊት', ['ዊት', ''], 'post'])
rules.append(['ና', ['ና', ''], 'post'])
rules.append(['ዎች', ['ዎች', ''], 'post'])
rules.append(['ኛ',['ኛ',''], 'post'])
rules.append(['የሚ',['የሚ',''],'pre'])
rules.append(['ዎቻቸው', ['ዎቻቸው', ''], 'post'])
rules.append(['ውም',[' ውም',''], 'post'])
rules.append(['ው', ['ው', ''], 'post'])
rules.append(['ውያን', ['ውያን', ''], 'post'])
rules.append(['ዎቹ', ['ዎቹ', ''], 'post'])
rules.append(['ኦች', ['ኦች', ''], 'post'])
rules.append(['ኦቹ', ['ኦቹ', ''], 'post'])
rules.append(['ናቸው', ['ናቸው', ''], 'post'])
rules.append(['ባቸው', ['ባቸው', ''], 'post'])
rules.append(['ዊያን', ['ዊያን', ''], 'post'])
rules.append(['ነት', ['ነት', ''], 'post'])
rules.append(['ያዊ', ['ያዊ', ''], 'post'])
rules.append(['እነ',['እነ',''],'pre'])
rules.append(['ኝ', ['ኝ', ''], 'post'])
rules.append(['ኛ',['ኛ',''], 'post'])
rules.append(['ሉ', ['ሉ', ''], 'post'])
rules.append(['ችው', ['ችው', ''], 'post'])
rules.append(['ዊ', ['ዊ', ''], 'post'])
rules.append(['ዊቷ', ['ዊቷ', ''], 'post'])
rules.append(['ቹን', ['ቹን', ''], 'post'])
rules.append(['ዬ', ['ዬ', ''], 'post'])
rules.append(['ዎ', ['ዎ', ''], 'post'])
rules.append(['ህ', ['ህ', ''], 'post'])
rules.append(['ዋ', ['ዋ', ''], 'post'])






# --------------------------------------------------------------------------------------------
# Reading and Preprocessing Data

# Spam Emails
spam_emails = ""
for i in range(1,51):
    num = str(i)
    file = "spam"+num+".txt"
    with codecs.open(file, 'r', 'utf-8') as myfile:
        data = myfile.read()
        data = data.replace('?', ' ')
        data = data.replace('\n', ' ')
        data = data.replace('.', ' ')
        data = data.replace('!', ' ')
        data = data.replace('፦', ' ')
        data = data.replace('•', ' ')
        data = data.replace('*', ' ')
        spam_emails = spam_emails + data
spam_words_list = spam_emails.split()
stemmed_spam_words = ""
for word in spam_words_list:
    stemmed_word = wordAnalyzer(word)
    stemmed_spam_words = stemmed_spam_words + " " + stemmed_word
stemmed_spam_words_list = stemmed_spam_words.split()

#Ham Emails
ham_emails = ""
for i in range(1,51):
    num = str(i)
    file = "ham"+num+".txt"
    with codecs.open(file, 'r', 'utf-8') as myfile:
        data = myfile.read()
        data = data.replace('?', ' ')
        data = data.replace('\n', ' ')
        data = data.replace('.', ' ')
        data = data.replace('!', ' ')
        data = data.replace('•', ' ')
        data = data.replace('፦', ' ')
        data = data.replace('*', ' ')
        ham_emails = ham_emails + data
ham_words_list = ham_emails.split()
stemmed_ham_words = ""
for word in ham_words_list:
    stemmed_word = wordAnalyzer(word)
    stemmed_ham_words = stemmed_ham_words + " " + stemmed_word
stemmed_ham_words_list = stemmed_ham_words.split()




# --------------------------------------------------------------------------------------------
# Extracting Features. Implementing the Classifier

all_words_list = stemmed_spam_words_list + stemmed_ham_words_list
unique_words = []
frequency_ratios = []
spam_words = ""

for word in all_words_list:
    if word not in unique_words:
        unique_words += [word]

print(">>>" + str(len(unique_words)) + " UNIQUE WORDS DETECTED.")

spam_frequencies = []
for word in unique_words:
    spam_frequencies += [int(stemmed_spam_words.count(word))]

ham_frequencies = []
for word in unique_words:
    ham_frequencies += [int(stemmed_ham_words.count(word))]
    frequency_ratios += [float(stemmed_ham_words.count(word))] #just initializing

for i in range(len(unique_words)):
    if (int(ham_frequencies[i]) != 0):
        frequency_ratios[i] = float(int(spam_frequencies[i]) / int(ham_frequencies[i]))
    else:
        frequency_ratios[i] = float(int(spam_frequencies[i]) / 1)


print('\n' + "SPAM WORDS" + '\n' + "---------") 
for i in range(len(unique_words)):
    if (float(frequency_ratios[i]) > 15):
        spam_words = spam_words + " " + unique_words[i]
        print(unique_words[i] + " = " + str(frequency_ratios[i]))
spam_triggers_list = spam_words.split()



# --------------------------------------------------------------------------------------------
# Main




#Function to find spam words in the incoming email
def find_spam_words(text):
        result = "NOT SPAM"
        print('\n'+'\n'+"------------------------------------------"+'\n'+"Spam Filter Result"+'\n'+"-------------------")
        for word in text.split():
                for i in range(len(spam_triggers_list)):
                        if (wordAnalyzer(word) == spam_triggers_list[i]):
                                result = "THIS IS A SPAM."
                                print("Spam Word: "+word+" >> "+wordAnalyzer(word))
        print ('\n'+"RESULT: "+result+'\n'+"------------------------------------------")



# Function to read email from file and call find_spam_words function
def emailResult(filename):
    with codecs.open(filename, 'r', 'utf-8') as myfile:
        data = myfile.read()
        print('\n'+data+'\n')
        find_spam_words(data)


#User input (Email filename) >> email1 and email2 for demonstration.
text = input('\n' + '\n' +"Enter Email: ")
while (text == "email1" or text == "email2" or text == "email3" or text == "email4" or text == "email5"):
    emailResult(text + ".txt")
    text = input('\n' + '\n' +"Enter Another Email: ")
else:
    print('\n'+"Email not found."+'\n'+"Good Bye."+'\n')
    exit


