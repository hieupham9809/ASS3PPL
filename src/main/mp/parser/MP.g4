/* 
    ID: 1611046 
    NAME: Pham Minh Hieu
*/

grammar MP;

@lexer::header {
from lexererr import *
}

options{
	language=Python3;
}

program  : declaration+ EOF;
declaration     : varDec | funcDec | procDec;

varDec            : VAR listOfType (SEMI listOfType)* SEMI;

listOfType      : ID (COMMA ID)* COLON types ;

// type

types           : BOOLEAN | INTEGER | REAL | STRING | arraycp;
arraycp         : ARRAY LSB arrayindex DDOT arrayindex RSB OF (BOOLEAN | INTEGER | REAL | STRING);

// funcDec
funcDec         : FUNCTION ID LB paramList RB COLON types SEMI varDec? compound_st;
paramList       : listOfType (SEMI listOfType)* | ;

compound_st     : BEGIN statement* END;

// procDec
procDec         : PROCEDURE ID LB paramList RB SEMI varDec? compound_st;

// expression


expression  : expression (AND THEN) exp1
            | expression (OR ELSE) exp1 | exp1;
exp1        : exp2 (EQOP | NEQOP | LTOP | LTEOP | GTOP | GTEOP) exp2 | exp2;
exp2        : exp2 (ADDOP | SUBOP | OR) exp3 | exp3;
exp3        : exp3 (DIVOP | MULOP | DIV | MOD | AND) exp4 | exp4;
exp4        : (SUBOP | NOT) exp4 | exp5;
exp5        : exp5 LSB expression RSB | exp6;
exp6        : LB expression RB | exp7;
exp7        : operand | call_st ;
operand     : INTLIT | REALIT | STRLIT | ID | BOOLIT;


indexEx : exp5 LSB expression RSB;

// statements
statement       : assign_st SEMI
                | if_st 
                | for_st 
                | while_st 
                | break_st SEMI
                | continue_st SEMI
                | return_st SEMI
                | full_call_st
                | compound_st 
                | with_st;

assign_st       : (lhs ASSIGOP)+ expression;
             
lhs             : ID | indexEx ;

while_st        : WHILE expression DO statement;
for_st          : FOR ID ASSIGOP expression (TO | DOWNTO) expression DO statement; 
break_st        : BREAK;
continue_st     : CONTINUE;
return_st       : RETURNS expression? ;
with_st         : WITH listOfType (SEMI listOfType)* SEMI DO statement;
full_call_st    : call_st SEMI;
call_st         : ID LB listOfExp RB;
listOfExp       : expression (COMMA expression)* | ;
//listOfExp1      : COMMA expression listOfExp1 | ;

if_st           : IF expression THEN statement (ELSE statement)?;
arrayindex      : SUBOP? INTLIT;
//key insensitive
fragment A: [aA];
fragment B: [bB];
fragment C: [cC];
fragment D: [dD];
fragment E: [eE];
fragment F: [fF];
fragment G: [gG];
fragment H: [hH];
fragment I: [iI];
fragment J: [jJ];
fragment K: [kK];
fragment L: [lL];
fragment M: [mM];
fragment N: [nN];
fragment O: [oO];
fragment P: [pP];
fragment Q: [qQ];
fragment R: [rR];
fragment S: [sS];
fragment T: [tT];
fragment U: [uU];
fragment V: [vV];
fragment W: [wW];
fragment X: [xX];
fragment Y: [yY];
fragment Z: [zZ];

// keyword
BREAK       : B R E A K;
CONTINUE    : C O N T I N U E;
FOR         : F O R;
TO          : T O;
DOWNTO      : D O W N T O;
DO          : D O;
IF          : I F;
THEN        : T H E N;
ELSE        : E L S E;
RETURNS     : R E T U R N;
WHILE       : W H I L E;
BEGIN       : B E G I N;
END         : E N D;
FUNCTION    : F U N C T I O N;
PROCEDURE   : P R O C E D U R E;
VAR         : V A R;
fragment TRUE        : T R U E;
fragment FALSE       : F A L S E;
ARRAY       : A R R A Y;
OF          : O F;
REAL        : R E A L;
BOOLEAN     : B O O L E A N;
INTEGER     : I N T E G E R;
STRING      : S T R I N G;
NOT         : N O T;
AND         : A N D;
OR          : O R;
DIV         : D I V;
MOD         : M O D;
WITH        : W I T H;




fragment IDCHAR: (A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z);

// Operators
ASSIGOP : ':=';
ADDOP   : '+';
MULOP   : '*';
NEQOP   : '<>';
LTOP    : '<';
LTEOP   : '<=';
SUBOP   : '-';
DIVOP   : '/';
EQOP    : '=';
GTOP    : '>';
GTEOP   : '>=';



// Literals
fragment DIGIT:  [0-9];
INTLIT  : DIGIT+;
//REALIT  : ((NUM_HAS_P | DIGIT+) EXPN) | NUM_HAS_P;
REALIT  : DIGIT+ '.'? | DIGIT* '.'? DIGIT+ ([eE]'-'? DIGIT+)?;
BOOLIT  : TRUE | FALSE;

ID  : (IDCHAR | '_')(IDCHAR | '_' | '0'..'9')*;


UNCLOSE_STRING: '"' (~["'\n\r\\] | ('\\' ["'nbftr\\]))*              
            {
                self.text = self.text[1:]    
                raise UncloseString(self.text)    
            };
STRLIT      : UNCLOSE_STRING '"'
                        {
                            self.text = self.text[1:-1]
                        };

ILLEGAL_ESCAPE: UNCLOSE_STRING ('\\' ~[bfntr"'])
                                            {
                                                raise IllegalEscape(self.text[1:])
                                            }; 







fragment NUM_HAS_P   :   DIGIT* '.' DIGIT+ | DIGIT+ '.' DIGIT*;   
fragment EXPN        :   (E '-'?) DIGIT+;




// Separators
LB      : '(' ;

RB      : ')' ;

SEMI    : ';' ;

COMMA   : ',';

LSB     : '[';

RSB     : ']';

COLON   : ':';

DDOT    : '..';

WS : [ \t\r\n]+ -> skip ; // skip spaces, tabs, newlines

// Comments
BLOCKCOM_B: '(*'.*?'*)' ->skip;
BLOCKCOM_P: '{'.*?'}' -> skip;
LINECOM: '//'~[\r\n]* ->skip;

ERROR_TOKEN: .
            {
                raise ErrorToken(self.text)    
            };





