grammar Baseball2020;

POINT : '.';
COMA: ',';
GET: 'recibe';
SE: 'se';
KEEP: 'continua';
GO: 'avanza a';
GOTO: 'llega a';
ES: 'es';
OUT: 'Out';
AND: 'y';
CHANGE: 'Cambio de';
OCHANGE: 'Cambio a la Ofensiva en el Turno';
CLOSEACT: 'Cierre de actuacion del Lanzador #';
IN: 'Entra';
SALE: 'Sale';
GUION: '-';
OBRACKET: '[';
CBRACKET: ']';
COLON: ':';
GETFIRST: 'y llega a 1B';
BB : 'Base por Bolas';
BI : 'Base por Bolas Intencional';
DB: 'Pelotazo';

SO: 'Poncha';
ONBASE: 'embasa por';
STEAL: 'roba';
CS: 'cogido robando';
BAT: 'bateando';
SCORE: 'anota'|'Anota';
HIT: 'batea';
CONECTA: 'conecta';

PRIMERA: 'Primera Base';
SEGUNDA: 'Segunda Base';
TERCERA: 'Tercera Base';
HOME: 'Home';

SINGLE: 'Sencillo';
DOBLE: 'Doble';
TRIPLE: 'Triple';
SACRIFLY: 'un Fly de sacrificio';
SACRIHIT: 'sacrificio de Hit';
HOMERUN: 'Jonron';
DP: 'para Doble Play';


FLY: 'de fly';
LINE: 'de linea';
ROLL: 'de rolling';

LEFT: 'al jardin izquierdo';
CENTER: 'al jardin central';
RIGHT: 'al jardin derecho';

ERROR: 'Error probabilidad de Out';
EE: 'por error';
FCH: 'FCH'|'por FCH';
XERROR: 'por error no probabilidad de Out'|'por error no  probabilidad de Out';
YERROR: 'por un error probabilidad de Out'|'por un error no probabilidad de Out o PB';
OTROERROR: 'error no probabilidad de Out o PB'|'por un error no probabilidad de Out';

P: 'Lanzador';
R: 'Receptor';
BASE1: '1B';
BASE2: '2B';
BASE3: '3B';
SHORT: 'SS';
LFILD: 'LF';
CFILD: 'CF';
RFILD: 'RF';

STRING :	('a'..'z'|'A'..'Z')+
    ;

INT :   [0-9]+;
FLOAT: INT POINT INT;

WS : [ \t\r\n]+ -> channel(HIDDEN);

name: STRING POINT STRING STRING*;
stat: STRING COLON (FLOAT|INT) COMA*;
act: stat+;
plays	:	play+;
play	:	name GET recibeType POINT
    |   name GET recibeType 'de error' POINT
    |   name SE SO POINT
    |   name SE SO 'de error' endlineType*
    |   name SE SO GETFIRST 'por WP o FCH' POINT
    |   name SE SO GETFIRST 'por Pass Ball o Error probabilidad de Out' POINT
    |   name KEEP BAT 'de error'* POINT
    |   name SE STEAL baseType ((AND GO bases errorType)|(AND SCORE errorType)|(errorType)|(AND ES OUT ('tratando de anotar'|'tratando de llegar a' bases)))* COMA+
    |   name GO baseType ((AND GOTO baseType errorType)|(AND SCORE errorType)|(errorType)|(AND ES OUT ('tratando de anotar'|'tratando de llegar a' bases))|(AND 'se mantiene con vida' errorType))* COMA+
    |   name SCORE ('por WP, BK o BDP')* COMA*
    |   name SCORE FCH endlineType*
    |   name HIT hitType ((GOTO bases)|(AND SE ONBASE onbaseType)|(AND 'avanza hasta' bases))* connectionType direction* INT* POINT
    |   name CONECTA hitType connectionType direction* POINT
    |   name ES OUT (outType INT* direction*)* endlineType*
    |   name SE ONBASE onbaseType (AND (GOTO|GO) bases)* connectionType* direction* INT* POINT
    |   name SACRIHIT connectionType* INT* POINT
    |   CHANGE bases IN name (GUION SALE name)* endlineType*
    |   OCHANGE INT IN name (GUION SALE name)* endlineType*
    |   CLOSEACT INT+ GUION name OBRACKET act CBRACKET
    |   'sorprendido' endlineType*
    |   name CS AND SCORE errorType endlineType*
    |   name CS AND 'es quieto en' bases EE endlineType*;


recibeType:
    DB
	|BB
	|BI;

baseType:
    PRIMERA
    |SEGUNDA
    |TERCERA
    |HOME
    |BASE1
    |BASE2
    |BASE3;

hitType:
    SINGLE
    |DOBLE
    |TRIPLE
    |HOMERUN
    |SACRIFLY
    |DP;

bases:
    P
    |R
    |BASE1
    |BASE2
    |BASE3
    |SHORT
    |LFILD
    |CFILD
    |RFILD;

connectionType:
    FLY
    |ROLL
    |LINE;

direction:
    LEFT
    |CENTER
    |RIGHT;

outType:
    CS
    |FLY
    |ROLL
    |LINE;

endlineType:
    POINT
    |COMA;

errorType:
    ERROR
    |XERROR
    |YERROR
    |OTROERROR
    |FCH
    |EE;

onbaseType:
    ERROR
    |FCH;
