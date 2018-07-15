'''check if there is another file in folder with the same name
list: new file----> number?
'''
class File(object):
    def __init__(self,name,content,path):
        self.name=name
        self.content=content
        self.path=path
        self.isNew=True
        self.modified=False
        

