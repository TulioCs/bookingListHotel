
class Hotel(object):
   
    def __init__(self, name, score ):
        self.__name = name
        self.__score = score
     
    def __repr__(self):
        return "\n %s = %.1f" % (self.__name, self.__score)
  
    def get_name(self):
        return self.__name
 
    def get_score(self):
        return self.__score
