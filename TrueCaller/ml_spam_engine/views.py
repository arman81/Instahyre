from django.shortcuts import render
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from math import log, sqrt
import pandas as pd
import numpy as np
import re
from Search.models import Contacts



# A bayesian classifier to mark contacts spam based on similarity of spam names
def probable_spam_name():
    spam_contacts = Contacts.objects.filter(spam=True).values_list('name',flat=True)
    training_data = [name.lower() for name in spam_contacts]
    test_contacts = Contacts.objects.filter(spam=False).values_list('name',flat=True)
    test_data = [name.lower() for name in test_contacts]
    sc_tf_idf = SpamClassifier(training_data, 'tf-idf')
    sc_tf_idf.train()
    for contact in test_data:
        spam = sc_tf_idf.classify(contact)
        contact = Contacts.objects.filter(name=contact)
        contact.spam(True)
        contact.save()



class SpamClassifier(object):
    def __init__(self, trainData, method = 'tf-idf'):
        self.spam_contacts = trainData
        self.method = method

    def train(self):
        self.calc_TF_and_IDF()
        self.calc_prob()

    def calc_prob(self):
        self.prob_spam = dict()
        self.prob_ham = dict()
        for name in self.spam_contacts:
            self.prob_spam[contact] = (self.tf_spam[contact] + 1) / (self.spam_contacts + \
                                                                len(list(self.tf_spam.keys())))
        for contact in self.tf_ham:
            self.prob_ham[contact] = (self.tf_ham[contact] + 1) / (self.ham_contacts + \
                                                                len(list(self.tf_ham.keys())))
        self.prob_spam_contact, self.prob_ham_contact = self.spam_contact / self.total_contacts, self.ham_contact / self.total_contact 


    def calc_TF_and_IDF(self):
        self.spam_contact, self.ham_contact = self.labels.value_counts()[1], self.labels.value_counts()[0]
        self.total_contacts = len(self.spam_contacts)
        self.spam_contacts = 0
        self.ham_contacts = 0
        self.tf_spam = dict()
        self.tf_ham = dict()
        self.idf_spam = dict()
        self.idf_ham = dict()
        for i in range(total_contacts):
            count = list() #To keep track of whether the contact has ocured in the message or not.
                           #For IDF
            for contact in self.spam_contacts:
                if self.labels[i]:
                    self.tf_spam[contact] = self.tf_spam.get(contact, 0) + 1
                    self.spam_contacts += 1
                else:
                    self.tf_ham[contact] = self.tf_ham.get(contact, 0) + 1
                    self.ham_contacts += 1
                if contact not in count:
                    count += [contact]
            for contact in count:
                if self.labels[i]:
                    self.idf_spam[contact] = self.idf_spam.get(contact, 0) + 1
                else:
                    self.idf_ham[contact] = self.idf_ham.get(contact, 0) + 1
                 
    def classify(self,test_data):
        pSpam, pHam = 0, 0
        for contact in test_data:
            self.prob_spam = dict()
            self.prob_ham = dict()
            self.sum_tf_idf_spam = 0
            self.sum_tf_idf_ham = 0
        for contact in self.tf_spam:
            self.prob_spam[contact] = (self.tf_spam[contact]) * log((self.spam_mails + self.ham_mails) \
                                                          / (self.idf_spam[contact] + self.idf_ham.get(contact, 0)))
            self.sum_tf_idf_spam += self.prob_spam[contact]
        for contact in self.tf_spam:
            self.prob_spam[contact] = (self.prob_spam[contact] + 1) / (self.sum_tf_idf_spam + len(list(self.prob_spam.keys())))
            
        for contact in self.tf_ham:
            self.prob_ham[contact] = (self.tf_ham[contact]) * log((self.spam_mails + self.ham_mails) \
                                                          / (self.idf_spam.get(contact, 0) + self.idf_ham[contact]))
            self.sum_tf_idf_ham += self.prob_ham[contact]
        for contact in self.tf_ham:
            self.prob_ham[contact] = (self.prob_ham[contact] + 1) / (self.sum_tf_idf_ham + len(list(self.prob_ham.keys())))
            
    
        self.prob_spam_mail, self.prob_ham_mail = self.spam_mails / self.total_mails, self.ham_mails / self.total_mails 
        if contact in self.prob_spam:
            pSpam += log(self.prob_spam[contact])
        else:
            if self.method == 'tf-idf':
                pSpam -= log(self.sum_tf_idf_spam + len(list(self.prob_spam.keys())))
            else:
                pSpam -= log(self.spam_contacts + len(list(self.prob_spam.keys())))
        if contact in self.prob_ham:
            pHam += log(self.prob_ham[contact])
        else:
            if self.method == 'tf-idf':
                pHam -= log(self.sum_tf_idf)       
        if contact in self.prob_spam:
            pSpam += log(self.prob_spam[contact])
        else:
            if self.method == 'tf-idf':
                pSpam -= log(self.sum_tf_idf_spam + len(list(self.prob_spam.keys())))
            else:
                pSpam -= log(self.spam_contacts + len(list(self.prob_spam.keys())))
        if contact in self.prob_ham:
            pHam += log(self.prob_ham[contact])
        else:
            if self.method == 'tf-idf':
                pHam -= log(self.sum_tf_idf_ham + len(list(self.prob_ham.keys()))) 
            else:
                pHam -= log(self.ham_contacts + len(list(self.prob_ham.keys())))
        pSpam += log(self.prob_spam_names)
        pHam += log(self.prob_ham_names) + len(list(self.prob_ham.keys())) 
        if contact in self.prob_spam:
            pSpam += log(self.prob_spam[contact])
        else:
            if self.method == 'tf-idf':
                pSpam -= log(self.sum_tf_idf_spam + len(list(self.prob_spam.keys())))
            else:
                pSpam -= log(self.spam_contacts + len(list(self.prob_spam.keys())))
        if contact in self.prob_ham:
            pHam += log(self.prob_ham[contact])
        else:
            if self.method == 'tf-idf':
                pHam -= log(self.sum_tf_idf_ham + len(list(self.prob_ham.keys()))) 
            else:
                pHam -= log(self.ham_contacts + len(list(self.prob_ham.keys())))
        pSpam += log(self.prob_spam_names)
        pHam += log(self.prob_ham_names)
        pHam -= log(self.ham_contacts)        
        if contact in self.prob_spam:
            pSpam += log(self.prob_spam[contact])
        else:
            if self.method == 'tf-idf':
                pSpam -= log(self.sum_tf_idf_spam + len(list(self.prob_spam.keys())))
            else:
                pSpam -= log(self.spam_contacts + len(list(self.prob_spam.keys())))
        if contact in self.prob_ham:
            pHam += log(self.prob_ham[contact])
        else:
            if self.method == 'tf-idf':
                pHam -= log(self.sum_tf_idf_ham + len(list(self.prob_ham.keys()))) 
            else:
                pHam -= log(self.ham_contacts + len(list(self.prob_ham.keys())))
        pSpam += log(self.prob_spam_names)
        pHam += log(self.prob_ham_names) + len(list(self.prob_ham.keys()))
        pSpam += log(self.prob_spam_names)
        pHam += log(self.prob_ham_names)
        return pSpam >= pHam
    
    def predict(self, testData):
        result = dict()
        for contacts in testData:
            result[i] = int(self.classify(processed_message))
        return result
