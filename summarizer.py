file_length = 0
irr_lines = []

def dict_gen(keyword_file):
    '''Returns dictionary with keys the keywords and synonyms in keyword_file
    and values the specified weights. Ignores keywords weighted 0.
    '''

    a = {}
    with open(keyword_file) as f:
        for line in f:
            b = line.split(':')
            if not int(b[-1]):
                break
            c = tuple(b[0].split(','))
            a[c] = b[1].rstrip()
    if a == {}:
        raise Exception('No keywords found.') from None
    return a

def blk_gen(keyword_file):
    '''Returns list with keywords and synonyms in keyword_file with weight 0.
    '''

    a = []
    with open(keyword_file) as f:
        for line in f:
            b = line.split(':')
            if not int(b[-1]):
                c = tuple(b[0].split(','))
                a.append(c)
    if a == []:
        raise Exception('No blacklisted keywords found.') from None
    return a

def doc_segmenter(text_file, separator):
    '''Returns list of strs created from text_file. Str separator specifies
    splitting of lines.
    '''

    a = []
    global file_length
    with open(text_file) as f:
        for line in f:
            file_length = file_length + 1
            for i in line.split(separator):
                a.append(i.rstrip())
    if a == []:
        raise Exception('No lines segmented.') from None
    print(str(file_length) + ' lines segmented.')
    return a

def weight_search(segmented_doc, keyword_dict):
    '''Return list of tuples: weights, keywords, and strings from list
    segmented_doc that have a keyword found in ordered keyword_dict.
    '''
    
    a = []
    n = 0
    global irr_lines
    for i in segmented_doc:
        b = 1
        for j in list(keyword_dict):
            for k in j:
                if k in i:
                    b = 0
                    n = n + 1
                    k = (keyword_dict.get(j), j[0], i)
                    a.append(k) 
                    break
            else:
                continue
            break
        if b:
            irr_lines.append(i)
    p = int((n/file_length)*100)
    if p <= 100:
        print(str(p) + '% of lines relevant.')
    else:
        raise Exception('Cannot have relevancy of over 100%') from None
    if a == []:
        raise Exception('No keyword matches found') from None
    a.sort(reverse = True)
    return a

def blk_search(segmented_doc, blk_list):
    '''Return list of strings from list segmented_doc that have a keyword found
    in blk_list.
    '''
    
    a = []
    n = 0
    for i in segmented_doc:
        for j in blk_list:
            for k in j:
                if k in i:
                    n = n + 1
                    a.append(i) 
                    break
            else:
                continue
            break
    p = int((n/file_length)*100)
    if p <= 100:
        print(str(p) + '% of lines with blacklisted terms.')
    else:
        raise Exception('Cannot have blacklist % of over 100%') from None
    if a == []:
        raise Exception('No blacklist matches found') from None
    return a

def keyword_texts(weighted_texts):
    '''Returns dictionary with keys the keywords from tuples weighted_texts
    and values a list of strs associated with the keyword.
    '''

    a = {}
    for i in weighted_texts:
        if i[1] in a:
            a[i[1]].append(i[2])
        else:
            a[i[1]] = [i[2]]
    return a

def keyword_summary(keyword_strs, filename):
    '''Creates text file with name from str filename containing keywords from
    keyword_strs (output of keyword_texts) followed by associated strs.
    '''

    f = open(filename, 'w')
    for i in list(keyword_strs):
        f.write(i + '(' + str(int((len(keyword_strs[i])/file_length)*100)) + '%)\n')
        for j in keyword_strs.get(i):
            f.write(j + '\n')
        f.write(' \n')
    f.close()
    print(f'{filename!r} updated with summary.')
    return None

##Test docs and functions:
a = dict_gen('resume.txt')
##print(a)
b = doc_segmenter('posting.txt','[')
##print(b)
c = weight_search(b,a)
##print(c)
print(irr_lines)
d = keyword_texts(c)
##print(d)
keyword_summary(d,'summary.txt')
##e = blk_gen('resume.txt')
##print(e)
##f = blk_search(b,e)
##print(f)
