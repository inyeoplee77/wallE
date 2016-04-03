from konlpy.tag import Twitter
from konlpy.tag import Komoran
twitter = Komoran()

text = open('190747347803005_191149761096097','r').read().decode('utf8')
print text
print '---------------'
sentence = []
for i in twitter.pos(text):
    #if i[1] == 'Unknown' or i[1] == 'Punctuation':
    #    continue
    if i[1] == 'SF' or i[1] == 'SE' or i[1] == 'SP' or i[1] == 'SS':
        continue
    sentence.append(i[0])
    if i[1] == 'EF' :
        print ''.join(sentence)
        sentence = []
    
    