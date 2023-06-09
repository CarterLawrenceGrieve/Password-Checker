import requests
import hashlib
import sys

def RequestApiData(query_chars):
    url='https://api.pwnedpasswords.com/range/'+ query_chars
    res=requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}')
    return res

def get_leak_count(hashes,password_tail_hashed):
   hashes=(line.split(':') for line in hashes.text.splitlines())
   for h, count in hashes:
    if h == password_tail_hashed:
       return count
       break

def pwned_check(password):
    sha1password=hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char,tail=sha1password[0:5],sha1password[5:]
    response=RequestApiData(first5_char)
    return(get_leak_count(response,tail))

#in case you want to run it in file:
def check_my_passwords(*args):
    for password in args:
        count=pwned_check(password)
        if count:
            print(f'This password, "{password}", was found {count} times.')
        else:
            print("Carry on, my wayward password")
    return 'End of passwords checked'

#in case you want to run it from command line:
def main(args):
    for password in args:
        count=pwned_check(password)
        if count:
            print(f'This password, "{password}", was found {count} times.')
        else:
            print("Carry on, my wayward password")
    return 'End of passwords checked'

#in case you want to read passwords from a text file split by newlines:
def Check_my_passwords_from_text_file(filename):
    with open(str(filename)+'.txt') as file:
        lines=file.read().splitlines()
    for password in lines:
        count=pwned_check(password)
        if count:
            print(f'This password, "{password}", was found {count} times.')
        else:
            print("Carry on, my wayward password")
    return 'End of passwords checked'

if __name__=='__main__':
    sys.exit(main(sys.argv[1:]))