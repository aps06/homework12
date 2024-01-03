import re
import main as ma
import os
import pickle
def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError:
            result = 'Wrong comand'
        except ValueError:
            result = "Wrong value"
        except IndexError:
            result = "Give me name and phone please"
        return result
    return inner


@input_error
def hello():
    return "How can I help you?"


@input_error
def add_rec(contacts, inputs):
    name = inputs.split()[0]
    if len(inputs.split()) == 2:
        birthday = inputs.split()[1]
        y = ma.Record(name, birthday)
    else:
        y = ma.Record(name)
    if name not in contacts.data:
        contacts.add_record(y)
    else:
        raise ValueError

@input_error
def add_phon(contacts, inputs):
    name = inputs.split()[0]
    phone = inputs.split()[1]
    contacts.data[name].add_phone(phone)


@input_error
def to_birthday(contacts, name):
    if name in contacts.data:
        return contacts.data[name].days_to_birthday()


@input_error
def change(contacts, inputs):
    name, phone1, phone2 = inputs.split()[0], inputs.split()[1], inputs.split([2])
    contacts.data[name].edit_phone(phone1, phone2)


@input_error
def find(contacts, inputs):
    return contacts.find_all(inputs)


@input_error
def del_contact(contacts, name):
    contacts.delete(name)


@input_error
def del_phone(contacts, inputs):
    name, phone = inputs.split()[0], inputs.split()[1]
    contacts.data[name].remove_phone(phone)


@input_error
def show(contacts, inputs):
    if len(inputs.split()) == 3:
        for k in contacts.iterator(int(inputs.split()[1]), int(inputs.split()[2])):
            return k
    for k in contacts.iterator():
        return k

def save(contacts):
    with open('contacts.bin', 'wb') as fh:
        pickle.dump(contacts.data, fh)

def loads(contacts):
    if 'contacts.bin' in os.listdir():
        with open('contacts.bin', 'rb') as fh:
            contacts.data = pickle.load(fh)


@input_error
def good_bye():
    return 'Good bye'


COMANDS = {'add rec': add_rec, "add phon": add_phon, 'hello': hello, 'change': change, 'find': find, 'show': show,
           'good bye': good_bye, 'close': good_bye, 'exit': good_bye, 'to birthday': to_birthday,
           'del contact': del_contact, 'del phone': del_phone}


def main():
    contacts = ma.AddressBook()
    loads(contacts)
    while True:
        inputs = input()
        c = ''
        for i in ['hello', 'change ', 'find ', 'show', 'add rec ', 'add phon ',
                  'good bye', 'close', 'exit', 'to birthday ', 'del contact ', 'del phone ']:
            if len(c) != 0:
                break
            c = re.findall(fr'^{i}', inputs)
            c = ''.join(c).strip()
        if c in ['add rec', 'add phon', 'change', 'show', 'find', 'del contact', 'del phone', 'to birthday'] and len(inputs[len(c)::].split()) <= 3:
            b = COMANDS[c](contacts, inputs[len(c)+1::])
            if b.__class__ is str:
                print(b)
        elif c in ['hello',  'good bye', 'close', 'exit'] and len(inputs[len(c)::].split()) == 0:
            a = COMANDS[c]()
            print(a)
            if a == 'Good bye':
                save(contacts)
                break
        else:
            print('wrong comand')


if __name__ == '__main__':
    main()
