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
