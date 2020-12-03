import sys
from antlr4 import *
from antlr4.error.ErrorListener import ErrorListener
from Baseball2020Lexer import Baseball2020Lexer
from Baseball2020Parser import Baseball2020Parser
from Baseball2020Listener import Baseball2020Listener
import pandas as pd

class NamePrinter(Baseball2020Listener):     
    def exitName(self, ctx):         
        print(ctx.getRuleIndex())

class MyErrorListener(ErrorListener):
    csvline = 0
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        print("ERROR: when parsing line %d column %d: %s\n" % \
                        (self.csvline, column, msg))
        return 

class BaseballListener(Baseball2020Listener) :
    nombre = ""
    outs = 0
    manonFirst = ""
    manonSecond = ""
    manonThird = ""
    base = ""
    runs = 0
    valid = True
    sacrihit = False
    aux_name = ""
    error = False
    def __init__(self, nombre="", outs=0, first="", second="", third="", runs=0):        
        self.nombre = nombre
        self.outs = outs
        self.manonFirst = first
        self.manonSecond = second
        self.manonThird = third
        self.base = ""
        self.runs = runs
        self.valid = True
        self.sacrihit = False
        self.aux_name = ""
        self.error = False

    def enterName(self, ctx:Baseball2020Parser.NameContext):
        self.nombre = ""
        for palabra in ctx.STRING():
            self.nombre += (palabra.getText() + " ")

    def enterBaseType(self, ctx:Baseball2020Parser.BaseTypeContext):
        if ( ctx.BASE1() or ctx.PRIMERA()):
            self.base = "1B"
        elif ( ctx.BASE2() or ctx.SEGUNDA()):
            self.base = "2B"
        elif ( ctx.BASE3() or ctx.TERCERA()):
            self.base = "3B"
        else:
            pass
    
    def enterHitType(self, ctx:Baseball2020Parser.HitTypeContext):
        if(ctx.DP()):
            self.outs+=1
        elif(ctx.SACRIFLY()):
            self.outs+=1
        elif(ctx.SINGLE()):
            self.base = "1B"
            self.manonFirst = self.nombre
        elif(ctx.DOBLE()):
            self.base = "2B"
            self.manonSecond = self.nombre
        elif(ctx.TRIPLE()):
            self.base = "3B"
            self.manonThird = self.nombre
        elif(ctx.HOMERUN()):
            self.runs+=1
    
    def enterBases(self, ctx:Baseball2020Parser.BasesContext):
        self.base = ctx.getText()
    
    def enterErrorType(self, ctx:Baseball2020Parser.ErrorTypeContext):
        self.error = True

    def exitPlay(self, ctx:Baseball2020Parser.PlayContext):
        if( ctx.GET() ):
            self.manonFirst = self.nombre
        elif( len(ctx.SE())>0 and ctx.GETFIRST() and ctx.SO()):
            self.manonFirst = self.nombre
        elif( len(ctx.SE())>0 and ctx.SO() ):
            self.esOut(self.nombre)
        elif( len(ctx.SE())>0 and ctx.STEAL() ):
            if( len(ctx.OUT()) > 0 ):
                self.esOut(self.nombre)
            elif(len(ctx.AND()) > 0 and len(ctx.SCORE()) > 0):
                self.quitarDelaBase(self.nombre)
                self.runs+=1
            else:
                self.moveRunner(self.nombre)
        elif( len(ctx.GO()) > 0 ):
            if( len(ctx.OUT()) > 0 ):
                self.esOut(self.nombre)
            elif(len(ctx.AND()) > 0 and len(ctx.SCORE()) > 0):
                self.quitarDelaBase(self.nombre)
                self.runs+=1
            else:
                self.moveRunner(self.nombre)
        elif( len(ctx.OUT()) > 0 and len(ctx.ES()) > 0):
            self.esOut(self.nombre)
        elif( len(ctx.SCORE()) > 0 ):
            self.quitarDelaBase(self.nombre)
            self.runs+=1
        elif( ctx.HIT() ):
            if( len(ctx.GOTO()) > 0 ):
                self.moveRunner(self.nombre)
            elif( len(ctx.ONBASE()) > 0 ):
                self.manonFirst = self.nombre
                self.outs-=1
            else:
                self.moveRunner(self.nombre)
        elif( len(ctx.SE()) > 0 and len(ctx.ONBASE()) > 0 ):
            if( len(ctx.GOTO()) > 0 or len(ctx.GO()) > 0 ):
                self.moveRunner(self.nombre)
            else:
                self.manonFirst = self.nombre
        elif( ctx.SACRIHIT() ):
            self.sacrihit = True
            self.aux_name = self.nombre
            self.outs+=1
        elif( ctx.CS() ):
            if(len(ctx.AND()) > 0 and len(ctx.SCORE()) > 0):
                self.quitarDelaBase(self.nombre)
                self.runs+=1
            elif(len(ctx.AND()) > 0 and ctx.EE()):
                self.moveRunner(self.nombre)
        elif( ctx.CONECTA() ):
            pass
        else:
            self.valid = False
   
    def exitPlays(self, ctx:Baseball2020Parser.PlaysContext):
        if(self.sacrihit and self.error):
            self.manonFirst = self.aux_name
            self.outs-=1

    def quitarDelaBase(self, name):
        if(name == self.manonFirst): self.manonFirst = ""
        elif(name == self.manonSecond): self.manonSecond = ""
        elif(name == self.manonThird): self.manonThird = ""
        else: pass

    def moveRunner(self, name):
        self.quitarDelaBase(name)
        if(self.base == "1B"): self.manonFirst = name
        elif (self.base == "2B"): self.manonSecond = name
        elif (self.base == "3B"): self.manonThird = name
        else: pass

    def esOut(self, name):
        self.outs+=1
        self.quitarDelaBase(name)

def writeRunners(first,second,third):
    if(first!="" and second!="" and third!=""):
        return "123"
    elif(first!="" and second!="" and third==""):
        return "12-"
    elif(first!="" and second=="" and third==""):
        return "1--"
    elif(first!="" and second=="" and third!=""):
        return "1-3"
    elif(first=="" and second=="" and third!=""):
        return "--3"
    elif(first=="" and second!="" and third!=""):
        return "-23"
    elif(first=="" and second!="" and third==""):
        return "-2-"
    else:
        return "---"
    
def main(argv):
    df = pd.read_csv("data.csv")
    data = pd.DataFrame(columns=[
        'Liga', 'Inning', 'Mitad Del Inning', 'Evento'
        , 'Outs Antes De Jugada', 'Corredores Inicio De Jugada'
        , 'Carreras Antes De Jugada', 'Carreras Anotadas En Jugada'
        , 'Outs En Juego', 'Outs Despues De Jugada', 'Corredores Despues De Jugada'
        , 'Carreras Despues De Jugada', 'Carreras Final Inning'
    ])
    outs = 0
    manonFirst = ""
    manonSecond = ""
    manonThird = ""
    runs = 0
    parte_del_inning = ""
    inning=""
    runners = "---"
    count = 0
    begin = 0
    #print(df.head(1))
    for index, play in df.iterrows():      
        error_listener = MyErrorListener()  
        error_listener.csvline = index
        lexer = Baseball2020Lexer(InputStream(play["evento"]))
        stream = CommonTokenStream(lexer)
        parser = Baseball2020Parser(stream)
        parser.removeErrorListeners()
        parser.addErrorListener(error_listener)
        tree = parser.plays()

        if( play["parte_del_inning"] != parte_del_inning or play["inning"] != inning):
            if(parte_del_inning!=""):
                data["Carreras Final Inning"][begin:count] = runs
                begin = count
            parte_del_inning = play["parte_del_inning"]
            inning = play["inning"]
            outs = 0
            runs = 0
            manonFirst = ""
            manonSecond = ""
            manonThird = ""
            runners = "---"
        
        jugada = pd.Series(index=data.columns, name=count)

        jugada["Liga"]="SNB60"
        jugada["Inning"]=play["inning"]
        jugada["Mitad Del Inning"]=play["parte_del_inning"]
        jugada["Evento"]=play["evento"]
        jugada["Outs Antes De Jugada"]=outs
        jugada["Corredores Inicio De Jugada"]=runners
        jugada["Carreras Antes De Jugada"]=runs
        
        bl = BaseballListener(outs=outs,first=manonFirst, second=manonSecond, third=manonThird,runs=runs)
        walker = ParseTreeWalker()
        walker.walk(bl, tree)
        outs = bl.outs
        runs = bl.runs
        manonFirst = bl.manonFirst
        manonSecond = bl.manonSecond
        manonThird = bl.manonThird
        runners = writeRunners(manonFirst,manonSecond,manonThird)

        jugada["Carreras Anotadas En Jugada"] = runs - jugada["Carreras Antes De Jugada"]
        jugada["Outs En Juego"] = outs - jugada["Outs Antes De Jugada"]
        jugada["Outs Despues De Jugada"] = outs
        jugada["Corredores Despues De Jugada"] = runners
        jugada["Carreras Despues De Jugada"] = runs
        if(jugada["Outs Antes De Jugada"] > 2):
            print(index)
            print(jugada["Evento"])
        if(bl.valid):
            data = data.append(jugada)
            count+=1
        #inning["Carreras Final Inning"] = runs
        
        #jugada["Carreras Final Inning"] 
        #print(tree.toStringTree(recog=parser))
    data["Carreras Final Inning"][begin:count] = runs
    data.to_csv('plays_data.csv', index=False)
    #print(data[:count])
    # lexer = Baseball2020Lexer(InputStream("Y. Urgelles  continua bateando de error. Y. Penalver  se roba 2B y avanza a 3B por error no probabilidad de Out, "))
    # stream = CommonTokenStream(lexer)
    # parser = Baseball2020Parser(stream)
    # tree = parser.plays()
    # bl = BaseballListener()
    # walker = ParseTreeWalker()
    # walker.walk(bl, tree)
if __name__ == '__main__':
    main(sys.argv)