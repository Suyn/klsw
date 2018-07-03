# -*- coding: utf-8 -*-
from module.files.files_module import Base
from dbsession import engine
def run():
    print('---------creating tables---------')
    Base.metadata.create_all(engine)
    print('---------create over---------')

if __name__ == "__main__":
    run()
