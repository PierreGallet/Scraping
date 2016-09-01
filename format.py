# coding: utf-8
import re, os, urllib2
from six.moves.html_parser import HTMLParser
import json

# text = u"hello, j'ai une couille\u2014"
# print(text.encode('utf-8'))
# text = u'Comment modifier vos coordonn\xe9es en ligne ?'
# print(text.encode('utf-8'))

def remove_tabs(text):
    text = text.replace('\t', '')
    return text

def remove_returns(text):
    # text = text.replace('\n\n', ' ')
    # text = text.replace('\r', ' ')
    # text = text.replace('\n', ' ')
    text = text.strip()
    return text

def format_faq():
    if os.path.exists('link2answer.json'):
        os.remove('link2answer.json')
    result = {}
    with open('sfr.json', 'r+') as f:
        data = json.load(f)
        for i in range(len(data)):
            result[urllib2.unquote(data[i][u'url'].encode('utf-8'))] = []
            result[urllib2.unquote(data[i][u'url'].encode('utf-8'))].append({"text":data[i]['title']})
            # we remove html special chars
            html = HTMLParser()
            text = html.unescape(' '.join(data[i][u'answer']))
            # we replace image blocks with *i*
            text = re.sub(r'<img.*?>', '*i*', text)
            # get the text inside the <a></a> for use in the button
            button = re.findall(r'<a.*?</a>', text)
            for n in range(len(button)):
                button[n] = re.sub(r'<.*?>', '', button[n]).strip()
            # we replace link block by *l* (the text inside will be used for the button)
            text = re.sub(r'<a.*?</a>', '*l*', text)

            # go to line when <br>
            text = text.replace('<br>', '\n')
            text = text.replace('</br>', '\n')
            text = text.replace('<br/>', '\n')
            # we remove all blocks
            clean_answer = re.sub(r'<.*?>', ' ',text)
            # print(clean_answer.encode('utf-8'))
            # print('-'*50)
            # we split by \n

            clean_answer = clean_answer.encode('utf-8').split('\n')
            # print(clean_answer)
            for k in range(len(clean_answer)):
                clean_answer[k] = clean_answer[k].strip()
            # clean_answer_2 = [elem + '\n' for elem in clean_answer if elem != '']
            clean_answer_2 = []
            for elem in clean_answer:
                if elem != '':
                    if elem != '*l*' and elem != '*i*' and len(elem) > 7:
                        clean_answer_2.append((elem+'\\n'))
                    else:
                        clean_answer_2.append(elem)
            # print clean_answer_2[0].split()
            # print('='*50)

            for m in range(len(clean_answer_2)):
                if (len(clean_answer_2[m]) > 320 or m == len(clean_answer_2)-1):
                    while(len(clean_answer_2[m]) > 320):
                        output = {}
                        count = 0
                        j = 0
                        for word in clean_answer_2[m].split():
                            if (count + len(word) + 1 > 318):
                                break;
                            else:
                                count += len(word) + 1
                                j += 1
                        output['text'] = ' '.join(clean_answer_2[m].split()[:j])
                        output['text'] += '...'
                        if len(output['text']) > 320:
                            raise ValueError('text > 320 character')
                        clean_answer_2[m] = ' '.join(clean_answer_2[m].split()[j:])
                        if (output['text'].count('*i*') > 0):
                            output['img'] = data[i][u'image'][:output['text'].count('*i*')]
                            data[i][u'image'] = data[i][u'image'][output['text'].count('*i*'):]
                            output['text'] = output['text'].replace('*i*', '').strip()
                        if (output['text'].count('*l*') > 0):
                            output['link'] = data[i][u'link'][:output['text'].count('*l*')]
                            output['button'] = button[:output['text'].count('*l*')]
                            data[i][u'image'] = data[i][u'link'][output['text'].count('*l*'):]
                            output['text'] = output['text'].replace('*l*', '').strip()
                        result[urllib2.unquote(data[i][u'url'].encode('utf-8'))].append(output)
                        # print ('aaaah', output['text'])
                        # print ('_'*50)
                    if (len(clean_answer_2[m]) > 300 or m == len(clean_answer_2)-1):
                        output = {}
                        output['text'] = clean_answer_2[m].strip()
                        if (output['text'].count('*i*') > 0):
                            output['img'] = data[i][u'image'][:output['text'].count('*i*')]
                            data[i][u'image'] = data[i][u'image'][output['text'].count('*i*'):]
                            output['text'] = output['text'].replace('*i*', '').strip()
                        if (output['text'].count('*l*') > 0):
                            output['link'] = data[i][u'link'][:output['text'].count('*l*')]
                            output['button'] = button[:output['text'].count('*l*')]
                            data[i][u'image'] = data[i][u'link'][output['text'].count('*l*'):]
                            output['text'] = output['text'].replace('*l*', '').strip()
                        result[urllib2.unquote(data[i][u'url'].encode('utf-8'))].append(output)
                        # print ('hey', output['text'])
                        # print ('_'*50)
                    else:
                        clean_answer_2[m+1] = clean_answer_2[m] + clean_answer_2[m+1]

                else:
                    clean_answer_2[m+1] = clean_answer_2[m] + clean_answer_2[m+1]


            # while(len(clean_answer) > 320):
            #     output = {}
            #     count = 0
            #     j = 0
            #     for word in clean_answer.split():
            #         if (count + len(word) + 1 > 318):
            #             break;
            #         else:
            #             count += len(word) + 1
            #             j += 1
            #     output['text'] = ' '.join(clean_answer.split()[:j])
            #     output['text'] += '...'
            #     if len(output['text']) > 320:
            #         raise ValueError('text > 320 character')
            #     clean_answer = ' '.join(clean_answer.split()[j:])


    if os.path.exists('link2answer.json'):
        os.remove('link2answer.json')
    with open('link2answer.json', 'w+') as output_file:
        json.dump(result, output_file, indent=4)

if __name__ == '__main__':

    format_faq()
