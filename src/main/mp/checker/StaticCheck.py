
"""
 * @author nhphung
"""
from AST import * 
from Visitor import *
from Utils import Utils
from StaticError import *

class MType:
    def __init__(self,partype,rettype):
        self.partype = partype
        self.rettype = rettype

class Symbol:
    def __init__(self,name,mtype,value = None):
        self.name = name
        self.mtype = mtype
        self.value = value
def check_redeclared(has_decl, decl):
    temp_name = ""
    if type(decl) is VarDecl:
        temp_name = decl.variable.name
        #if Utils.lookup(temp_name, has_decl,lambda x: x.name):
        if any((temp_name != hde.name ) for hde in has_decl):
            raise Redeclared(Variable(), temp_name)
        else: return Symbol(temp_name,decl.varType)
    else: 
        temp_name = decl.name.name
        #if Utils.lookup(temp_name, has_decl,lambda x: x.name):
        if any((temp_name != hde.name ) for hde in has_decl):
            if type(decl.returnType) is VoidType:
                raise Redeclared(Procedure(), temp_name)
            else: raise Redeclared(Function(), temp_name)
        else: return Symbol(temp_name,MType([x.varType for x in decl.param],decl.returnType))
            

    
    
    

class StaticChecker(BaseVisitor,Utils):

    global_envi = [Symbol("getInt",MType([],IntType())),
    			   Symbol("putIntLn",MType([IntType()],VoidType())),
                   Symbol("putInt",MType([IntType()],VoidType())),
                   Symbol("getFloat",MType([],FloatType())),
                   Symbol("putFloat",MType([FloatType()],VoidType())),
                   Symbol("putFloatLn",MType([FloatType()],VoidType())),
                   Symbol("putBool",MType([BoolType()],VoidType())),
                   Symbol("putBoolLn",MType([BoolType()],VoidType())),
                   Symbol("putString",MType([StringType()],VoidType())),
                   Symbol("putStringLn",MType([StringType()],VoidType())),
                   Symbol("putLn",MType([],VoidType()))
                   ]
            
    
    def __init__(self,ast):
        self.ast = ast
   
    def check(self):
        return self.visit(self.ast,StaticChecker.global_envi)

    def visitProgram(self,ast, c): 
        has_decl = c.copy()
        for decl in ast.decl:
            has_decl.append(check_redeclared(has_decl,decl))
        #return [self.visit(x,c) for x in ast.decl]
        for decl in ast.decl:
            self.visit(decl, has_decl)
        return None

    def visitFuncDecl(self,ast, c): 
        return list(map(lambda x: self.visit(x,(c,True)),ast.body)) 
    

    def visitCallStmt(self, ast, c): 
        at = [self.visit(x,(c[0],False)) for x in ast.param]
        
        res = self.lookup(ast.method.name,c[0],lambda x: x.name)
        if res is None or not type(res.mtype) is MType or not type(res.mtype.rettype) is VoidType:
            raise Undeclared(Procedure(),ast.method.name)
        elif len(res.mtype.partype) != len(at):
            raise TypeMismatchInStatement(ast)            
        else:
            return res.mtype.rettype

    def visitIntLiteral(self,ast, c): 
        return IntType()

