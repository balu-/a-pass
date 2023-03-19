import logging
#logging.basicConfig(level=logging.DEBUG)

import argparse
parser = argparse.ArgumentParser(description='apass is a tool to store and access your password in a crypted wallet.')

subparsers = parser.add_subparsers(help="Sub-commands help", dest="command")
parser_init = subparsers.add_parser("init", help="init password vault")
parser_show = subparsers.add_parser("show", help="show content")
parser_insert = subparsers.add_parser("insert", help="insert content")
parser_generate = subparsers.add_parser("generate", help="generate content")
parser_update = subparsers.add_parser("update", help="update content")
parser_delete = subparsers.add_parser("delete", help="delete content")
parser_shell = subparsers.add_parser("shell", help="get a shell")


parser_show.add_argument("-c", "--clipboard", action="store_true",
    help="Copy selected password to clipboard")

parser_show.add_argument("--showPassword", action="store_true",
    help="print passwort in cleartext output")

group = parser_show.add_mutually_exclusive_group()
group.add_argument("-t","--title",  nargs='?', help="select entry by title",type=str)
group.add_argument("-u", "--uuid", nargs='?', help="select entry by uuid",type=str)
group.add_argument("-a","--attribute",  nargs='?', action='append', help="select entry by attribute value (format key=value)",type=str)
#parser_show.add_argument("descriptor",    nargs='?', default='', help="Descriptor of PW to select",type=str)

parser_insert.add_argument("descriptor",  help="Descriptor of PW to insert",type=str)
parser_generate.add_argument("descriptor",help="Descriptor of PW to generate",type=str)
parser_update.add_argument("descriptor",  help="Descriptor of PW to update",type=str)
parser_delete.add_argument("descriptor",  help="Descriptor of PW to delete",type=str)

args = parser.parse_args()

logging.debug(vars(args))

from getpass import getpass

from .repo import Repo
from .entry import Entry
from .util import totp


def getPassword(prompt:str="Enter the password to open the vault:")->str:
    """ Ask user for a password """
    try:
        return getpass(prompt)
    except KeyboardInterrupt as e:
        print("Abort")
        exit(0)

def stringifyEntry(e:Entry, printPassword:bool=False) -> str:
    """ generate a cli printable string representation of Entry e """
    t = e.title
    v = e.getValues()
    v_str = {}
    
    for key, value in v.items():
        attr = value.getAttribute()
        if not printPassword and value.getType() == Entry.Value.TYPE_PASSWORD:
            v_str[key] = "***"
        elif not printPassword and value.getType() == Entry.Value.TYPE_TOTP:
            #genrate totp value
            v_str[key] = totp.fromUrl(str(value))[2]
            #pass
        else:
            v_str[key] = str(value)
        #if hasattr(v[key],"type")
    return f"[{t}] -> {v_str}" 

def shellFunc_init() -> None:
    """ Function to init a new Password store"""
    password = getPassword("Enter a password for the new vault")
    try:
        e = Repo(password, createRepo=True)
        if type(e) != Repo:
            print("Error")
            raise Exception("Unknown error creatting password vault")
        else:
            print("Created vault successfully")
            exit(0)
    except Exception as e:
        print(e)

def shellFunc_insert(title) -> None:
    """ Function to insert entry in the Password store """
    password = getPassword()
    try:
        r = Repo(password)
        if type(r) != Repo:
            raise Exception("Unknown error opening password vault")
        else:
            #repo open successfully
            attr = {}
            while(input("Add attribute?[y/N]").lower() == "y"):
                typeOfAttr = -1
                typeArray = Entry.Value.LIST_OF_TYPE
                while typeOfAttr < 0 or typeOfAttr > len(typeArray)-1:
                    for key, value in enumerate(typeArray):
                        print(f"{key}-{value}")
                    typeOfAttr = int(input(f"Select typ of attribut (0-{len(typeArray)-1}):"))
                name = input("Enter name of attribute:")
                if typeArray[typeOfAttr] != "password":
                    value = input(f"Enter value for {name}:")
                else:
                    value = getPassword(f"Enter password value for {name}:")
                attr[name]=Entry.Value(value, typeOfValue=typeArray[typeOfAttr])
            #attr['password'] = pw
            e = Entry(title, attr)
            r.saveEntry(e)
            print("Saved entry")
    except Exception as e:
        print(e)

def shellFunc_show(title=None, attribute=None, uuid=None, showPassword=False) -> None:
    password = getPassword()
    try:
        r = Repo(password)
        if type(r) != Repo:
            raise Exception("Unknown error creatting password vault")
        else:
            #list repo content
            res = []
            if (title == None and uuid == None and attribute == None):
                entries = r.ls()
                for key,e in entries.items():
                    res.append(e)
            else:
                #show single entry
                entries = r.ls()
                #suchen 
                if attribute != None:
                    search_attr = {} #search key value
                    for attr in attribute:
                        s_attr = attr.split("=")
                        if len(s_attr) != 2:
                            raise Exception("Attribute should have the format <key>=<value>")
                        else:
                            search_attr[s_attr[0]]=s_attr[1]
                    #search
                    class forLoopBreakException(Exception):
                        pass

                    for key, e in entries.items():
                        try:
                            for skey, sval in search_attr.items():
                                if not (sval in e[skey]):
                                    raise forLoopBreakException("key value missmatch - loop breaker")
                            res.append(e)
                        except forLoopBreakException as e:
                            pass
                else:
                    for key, e in entries.items():
                        if title and e.title == title:
                            res.append(e)
                        elif uuid and e.uuid == uuid:
                            res.append(e)
            for e in res:
                print(f"{stringifyEntry(e, printPassword=showPassword)}")
            print("-----------------")
            print(f"{len(res)} entries")
    except Exception as e:
        print(e)

def do_command(args):
    if args.command == "show":
        logging.debug("Show")
        shellFunc_show(title=args.title, attribute=args.attribute, uuid=args.uuid, showPassword=args.showPassword)
    elif args.command == "insert":
        logging.info("insert")
        shellFunc_insert(args.descriptor)
    elif args.command == "generate":
        logging.info("generate")
    elif args.command == "update":
        logging.info("update")
    elif args.command == "delete":
        logging.info("delete")
    elif args.command == "init":
        logging.info("init")
        shellFunc_init()
    else:
        parser.print_help()

def main():
    # main function
    if args.command == "shell": 
        logging.info("shell")
        #prepare shell mode
        parser.exit_on_error=False
        parser_exit = subparsers.add_parser("exit", help="exit shell")
        try:
            while True:
                inp = input(">")
                try:
                    
                    shell_args = parser.parse_args(inp.split(' '))
                    if shell_args.command == "exit":
                        exit(0)
                    else:
                        do_command(shell_args)
                except argparse.ArgumentError as e:
                    print(f"Unknown Comand {inp}")
                    parser.print_help()
        except KeyboardInterrupt as i:
            print("exit on KeyboardInterrupt")
            exit(0)
    else:
        do_command(args)


#main programm
try:
    main()
except Exception as e:
    print("Unknown error")
    raise e