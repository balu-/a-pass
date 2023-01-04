# a-pass
a password store based on age-encryption


## Run commands
    source venv/bin/activate
    python3 -m apass --help

<code>
usage: apass [-h] {init,show,insert,generate,update,delete,shell} ...

apass is a tool to store and access your password in a crypted wallet.

positional arguments:
  {init,show,insert,generate,update,delete,shell}
                        Sub-commands help
    init                init password vault
    show                show content
    insert              insert content
    generate            generate content
    update              update content
    delete              delete content
    shell               get a shell

options:
  -h, --help            show this help message and exit
</code>


## Run Tests
    source venv/bin/activate
    python3 -m unittest