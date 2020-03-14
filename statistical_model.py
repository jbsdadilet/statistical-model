#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 17:24:50 2019

@author: adilet
"""
import math 

def clean_text(txt):
        """cleaning the text from punctuation symbols"""
       
        s = txt.lower()
        
        for symbol in """.,?'!$%/#§±&*:;""":
            s = s.replace(symbol, '')
            
        s = s.split()
        
        return s    


def stem(word):
    """this function remove endings of the words and return stem/root of the word """
    if word == '':
        return word
    if word[-4:] == 'ness':
        word =stem(word[:-4])
    elif word[-2:] == 'es':
        word = stem(word[:-2])
    elif word[-1] == 's':
        word = stem(word[:-1])
    elif word[-3:] == 'ing':
        if len(word) >= 5 and word[-4] == word[-5]:
            if len(word[:-3]) <= 3:
                word = word[:-3]
            else:
                word = word[:-4]
        else:
            word = stem(word[:-3])      
    elif word[-2:] == 'er':
        word = stem(word[:-2])
    elif word[-2:] == 'ed':
        word = stem(word[:-2])
    elif word[-2:] == 'ty':
        if word[-3:] == 'ity':
            word = word[:-2]
        else:
            word = word[:-1] + 'i'
    elif word[-2:] == 'al':
        word = stem(word[:-2])
    elif word[-3:] == 'dom':
        word = stem(word[:-3])
    
    elif word[-4:] == 'able':
        word = stem(word[:-4])
    
    return word
    
def compare_dictionaries(d1, d2):
    """this function counts total number of words in dictionary d1, and return probability scores  """
    score = 0
    
    num_words_dic1 = 0
    #num_words_dic2 = 0
    
    # to count the number of words in dictionary
    for key in d1:
        num_words_dic1 += d1[key] 

    for key in d2:
        if key in d1:
            score +=  d2[key] * math.log(d1[key] / num_words_dic1)
        else:
            score += d2[key] * math.log(0.5/num_words_dic1)
    
    return score
    
    
    
          
class TextModel:
    
    def __init__(self, model_name):
        """constructor of this class, accept model name from user  and has two empty dictionaries"""
        self.name = model_name
        self.words = {}
        self.word_lengths = {}
        
        self.stems = {}
        self.sentence_lengths = {}
        self.num_punctuation = {}
        
    
    def __repr__(self):
        """Return a string representation of the TextModel."""
        s = 'text model name: ' + self.name + '\n'
        s += '  number of words: ' + str(len(self.words)) + '\n'
        s += '  number of word lengths: ' + str(len(self.word_lengths)) +"\n"
        s += "  number of stems: " + str(len(self.stems)) +'\n'
        s += "  number of sentence lengths: " + str(len(self.sentence_lengths))+"\n"
        s += "  number of punctuation: " + str(len(self.num_punctuation)) 
        
        return s

    
    def add_string(self, s):
        """Analyzes the string txt and adds its pieces
           to all of the dictionaries in this text model."""
            
        splitted = s.split()
        #print(splitted)
        num_words = 0
        
        for word in splitted:
            num_words +=1
            if '.' in word or '?' in word or '!' in word or ';' in word:
                #print("I was here")
                self.sentence_lengths[num_words] = 1
                num_words = 0
                
        # to count the punctunation from string of text
        for symbol in """.,?'!$%/#§±&*:;_-*()+=\'"][""":
            for symbol2 in s:
                if symbol == symbol2 and symbol not in self.num_punctuation:
                    self.num_punctuation[symbol] = 1
                elif symbol == symbol2 and symbol in self.num_punctuation:
                    self.num_punctuation[symbol] +=1
        
        
        word_list = clean_text(s)
        
        for stemmed in word_list:
            stem2 = stem(stemmed)
            if stem2 not in self.stems:
                self.stems[stem2] = 1
            elif stem2 in self.stems:
                self.stems[stem2] +=1
        
        for w in word_list:
            if w not in self.words:
                self.words[w] = 1
            elif w in self.words:
                self.words[w] += 1
                   
         
        for w in word_list:
            if len(w) not in self.word_lengths:
                self.word_lengths[len(w)] = 1
            elif len(w) in self.word_lengths:
                self.word_lengths[len(w)] += 1
                
        
    
        
    def add_file(self, filename):
        """method open the file and add the file to model, creating words and word_lengths dictionaries"""
        
        # open and read the text file and send to helper function to add the strings 
        file = open(filename, 'r', encoding='utf8', errors='ignore')
        
        text = file.read()
        file.close()
        
        self.add_string(text)
        
        
    def save_model(self):
        """the method create five files and write the dictionary content into file """
        
        filename1 = str(self.name) + '_' + 'words'
        
        filename2 = str(self.name) + '_' + 'word_lengths'
        
        filename3 = str(self.name) + "_" + "stems"
        
        filename4 = str(self.name) + "_" + "sentence_lengths"
        
        filename5 = str(self.name) + "_" + "number of punctuation"
        
        file1 = open(filename1, 'w')
        file1.write(str(self.words))
        file1.close()
        
        file2 = open(filename2, 'w')
        file2.write(str(self.word_lengths))
        file2.close()
        
        file3 = open(filename3, 'w')
        file3.write(str(self.stems))
        file3.close()
        
        file4 = open(filename4, 'w')
        file4.write(str(self.sentence_lengths))
        file4.close()
        
        file5 = open(filename5, 'w')
        file5.write(str(self.num_punctuation))
        file5.close()
        
        
    def read_model(self):
        """reads the stored dictionaries saved into file and assign to model attrcibutes, like words and word_lengths dictionaries"""
        
        filename1 = str(self.name) + '_' + 'words'
        
        filename2 = str(self.name) + '_' + 'word_lengths'
        
        filename3 = str(self.name) + "_" + "stems"
        
        filename4 = str(self.name) + "_" + "sentence_lengths"
        
        filename5 = str(self.name) + "_" + "number of punctuation"
        
        file1 = open(filename1, 'r')
        dic_str1 = file1.read()
        file1.close()
    
        dict1 = dict(eval(dic_str1)) # in built function to convert str to dictionary 
        
        self.words = dict1
        
        file2 = open(filename2, 'r')
        dic_str2 = file2.read()
        file2.close()
    
        dict2 = dict(eval(dic_str2)) # in built function to convert str to dictionary 
        
        self.word_lengths = dict2
        
        file3 = open(filename3, 'r')
        dic_str3 = file3.read()
        file3.close()
        
        dict3 = dict(eval(dic_str3))
        self.stems = dict3
        
        file4 = open(filename4, 'r')
        dic_str4 = file4.read()
        file4.close()
        
        dict4 = dict(eval(dic_str4))
        self.sentence_lengths = dict4
        
        file5 = open(filename5, 'r')
        dic_str5 = file5.read()
        file5.close()
        
        dict5 = dict(eval(dic_str5))
        self.num_punctuation = dict5
        
        
        
        
    def similarity_scores(self, other):
        """ this method use helper function compare_dictionaries for (two dict) self and other dictinoaries"""
        
        word_score = compare_dictionaries(other.words, self.words)
        
        word_length_score = compare_dictionaries(other.word_lengths, self.word_lengths)
        
        stems_score = compare_dictionaries(other.stems, self.stems)
        
        sentence_lengths_score = compare_dictionaries(other.sentence_lengths, self.sentence_lengths)
        
        num_punctuation_score = compare_dictionaries(other.num_punctuation, self.num_punctuation)
        
        return_list = [word_score, word_length_score, stems_score, sentence_lengths_score, num_punctuation_score ]
    
        
        return return_list
            
            
        
    def classify(self, source1, source2):
        """this method calls other method(similarity_scores) and compare the numbers
        and find out which one more likely come from original text"""
        
        scores1 = self.similarity_scores(source1)
        scores2 = self.similarity_scores(source2)

        
        for i in range(len(scores1)):
            scores1[i] = round(scores1[i], 3)
            scores2[i] = round(scores2[i], 3)
        
        print(source1.name, ":" , scores1)
        print(source2.name, ":" , scores2)
        
        count1 = 0
        count2 = 0
        
        for i in range(len(scores1)):
            if scores1[i] > scores2[i]:
                count1 +=1
                
            elif scores1[i] < scores2[i]:
                count2 +=1
                
        if count1 > count2:
            print(self.name, "is more likely to have come from", source1.name, '\n')
        else:
            print(self.name, "is more likely to have come from", source2.name, '\n')
            
                
def run_tests():
    """ taking New York Times and Wall Street Journal texts to check with other articals which come from differnt sources """
    source1 = TextModel('New York Times')
    source1.add_file('The Perfect Weapon(NYT).txt')
    source1.add_file('Perils of Climate Change(NYT).txt')
    source1.add_file('SoftBank Takes Loss(NYT).txt')
    source1.add_file('Wonder and Worry(NYT).txt')

    source2 = TextModel('Wall Street Journal')
    source2.add_file('The Best Apps for Reading(WSJ).txt')
    source2.add_file('TV Maker Vizio(WSJ).txt')
    source2.add_file('Korea’s Giant Shipyard(WSJ).txt')
    print(source1.num_punctuation, source1.stems)
                     
                     
    new1 = TextModel('National Geographic')
    new1.add_file('New kind of alien(NG).txt')
    new1.classify(source1, source2) 
    
    new2 = TextModel('Smithsonian')
    new2.add_file('Scientists Pumped Ovarian(smith).txt')
    new2.classify(source1, source2) 
    
    new3 = TextModel('Cosmopolitan')
    new3.add_file('Bernie Sanders(Cos).txt')
    new3.classify(source1, source2) 
    
    new4 = TextModel('Cosmopolitan')
    new4.add_file('Cosmo Asks Bernie Sanders the Questions(Cos).txt')
    new4.classify(source1, source2) 
    
    # below optional model comparison 
    new5 = TextModel('Essay')
    new5.add_file('What Makes a Good Teacher.txt')
    new5.classify(source1, source2)
    
    new6 = TextModel('NYT')
    new6.add_file('SoftBank Takes Loss(NYT).txt')
    new6.classify(source1, source2) 
    
    new7 = TextModel('WSJ')
    new7.add_file('The Best Apps for Reading(WSJ).txt')
    new7.classify(source1, source2) 

    

def test():
    """ this function short test from source1 and source2, to find mystery text has more likely to be close """
    source1 = TextModel('source1')
    source1.add_string('It is interesting that she is interested.')

    source2 = TextModel('source2')
    source2.add_string('I am very, very excited about this!')

    mystery = TextModel('mystery')
    mystery.add_string('Is he interested? No, but I am.')
    mystery.classify(source1, source2)
    
    
     
       
        
        
        
        
        
        
        