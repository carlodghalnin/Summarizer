import sys
import fileinput

def add_kw(kw_file,kw,wt):
    '''Add specified keyword and weight to kw_file. Arguments kw_file and kw are
    strs, while wt is an int. Not used for updating weight.
    '''

    kw_add = 0
    with open(kw_file) as f:
        for line in f:
            if kw in line:
                raise Exception("Keyword already present.") from None
    with fileinput.input(files=(kw_file),inplace=1) as f:
        for line in f:
            if int(line.split(':')[-1]) > (wt - 1) and not kw_add:
                sys.stdout.write(line)
            elif int(line.split(':')[-1]) == (wt - 1) and not kw_add:
                sys.stdout.write(kw + ':' + str(wt) + '\n' + line)
                kw_add = 1
            elif kw_add:
                sys.stdout.write(line)
    print(f"Keyword {kw!r} added.")
    return None

def kw_syn(kw_file,kw,syn):
    '''Updates kw_file with synonym of specified keyword. String arguments.
    '''

    kw_update = 0
    with fileinput.input(files=(kw_file),inplace=1) as f:
        for line in f:
            if kw in line and syn not in line:
                sys.stdout.write(line.replace(':', ',' + syn + ':'))
                kw_update = 2
            elif kw in line and syn in line:
                sys.stdout.write(line)
                kw_update = 1
            else:
                sys.stdout.write(line)
    if kw_update == 2:
            print(f"Keyword {kw!r} updated with synonym {syn!r}.")
    elif kw_update == 1:
            print(f"Keyword {kw!r} already has synonym {syn!r}.")
    else:
            print(f"Keyword {kw!r} not present in {kw_file!r}.")
    return None

def del_kw(kw_file,kw):
    '''Remove specified keyword from kw_file. String arguments.
    '''

    kw_del = 0
    with fileinput.input(files=(kw_file),inplace=1) as f:
        for line in f:
            if kw in line:
                kw_del = 1
                continue
            else:
                sys.stdout.write(line)
    if kw_del:
        print(f"Keyword {kw!r} deleted.")
    else:
        print(f"Keyword {kw!r} not present in {kw_file!r}.")
    return None

def del_syn(kw_file,kw,syn):
    '''Removes synonym of specified keyword. String arguments.
    '''

    syn_del = 0
    with fileinput.input(files=(kw_file),inplace=1) as f:
        for line in f:
            if kw in line and syn in line:
                sys.stdout.write(line.replace(',' + syn + ':',':'))
                syn_del = 2
            elif kw in line and syn not in line:
                sys.stdout.write(line)
                syn_del = 1
            else:
                sys.stdout.write(line)
    if syn_del == 2:
            print(f"Synonym {syn!r} of keyword {kw!r} deleted.")
    elif syn_del == 1:
            print(f"Keyword {kw!r} doesn't have synonym {syn!r}.")
    else:
            print(f"Keyword {kw!r} not present in {kw_file!r}.")
    return None


## To update weight, delete keyword and then add again.


##Testing file
##success:3
##fail:1
##none:0
##add_kw('kw_test.txt','temp',2)
##kw_syn('kw_test.txt','fail','lose')
##del_kw('kw_test.txt','none')
##del_syn('kw_test.txt','fail','lose')
