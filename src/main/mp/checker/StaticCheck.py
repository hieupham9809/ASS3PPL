
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
def check_redeclared(has_decl, decl, k):
    temp_name = ""
    #if type(decl) is VarDecl:
    if k == "variable":
        
        temp_name = decl.variable.name
        
        #if Utils.lookup(temp_name, has_decl,lambda x: x.name):
        if any((temp_name == hde.name ) for hde in has_decl):
            raise Redeclared(Variable(), temp_name)
        else: return Symbol(temp_name,decl.varType)
        #return StaticChecker.visit(decl,has_decl)
    elif k == "procedure": 
        temp_name = decl.name.name
        #if Utils.lookup(temp_name, has_decl,lambda x: x.name):
        if any((temp_name == hde.name ) for hde in has_decl):
            if type(decl.returnType) is VoidType:
                raise Redeclared(Procedure(), temp_name)
            else: raise Redeclared(Function(), temp_name)
        else: return Symbol(temp_name,MType([x.varType for x in decl.param],decl.returnType))
    else:
        temp_name = decl.variable.name
        #if Utils.lookup(temp_name, has_decl,lambda x: x.name):
        if any((temp_name == hde.name ) for hde in has_decl):
            raise Redeclared(Parameter(), temp_name)
        else: return Symbol(temp_name,decl.varType)    

    
def check_operator(left, right):
    #print(left)
    #print(right)
    if (type(left), type(right)) == (IntType, IntType):
        return IntType()
    elif (type(left),type(right)) in [(IntType, FloatType), (FloatType, IntType), (FloatType, FloatType)]:
        return FloatType()
    else: return None

    
    

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
            has_decl.append(check_redeclared(has_decl,decl, "variable" if type(decl) is VarDecl else "procedure"))
        #return [self.visit(x,c) for x in ast.decl]
        for decl in ast.decl:
            self.visit(decl, has_decl)
        return None

    def visitFuncDecl(self,ast, c):
        globaldecl = c.copy()
        param_sub_scope = []
        local_sub_scope = []
        flag = False
        for vardecl in ast.param:
            param_sub_scope.append(check_redeclared(param_sub_scope, vardecl,"parameter"))
        local_sub_scope += param_sub_scope
        
        for vardecl in ast.local:
            local_sub_scope.append(check_redeclared(local_sub_scope, vardecl,"variable"))
        
        for i in range(len(local_sub_scope)):
            flag = False
            for j in range(len(globaldecl)):
                if globaldecl[j].name == local_sub_scope[i].name:
                    globaldecl[j] = local_sub_scope[i]
                    flag = True
                    break 
            if not flag:
                globaldecl.append(local_sub_scope[i])

        #return list(map(lambda x: self.visit(x,c),ast.body)) 
        
        return [self.visit(x, globaldecl) for x in ast.body]
    '''def visitVarDecl(self,ast,c):
        if any((ast.variable.name == hde.name ) for hde in c):
            raise Redeclared(Variable(), ast.variable.name)
        else: #return Symbol(ast.variable.name,self.visit(ast.varType,c))
            return Symbol(ast.variable.name,ast.varType)'''

    def visitCallStmt(self, ast, c): 
        at = [self.visit(x,c) for x in ast.param]
        
        res = self.lookup(ast.method.name,c,lambda x: x.name)
        if res is None or not type(res.mtype) is MType or not type(res.mtype.rettype) is VoidType:
            raise Undeclared(Procedure(),ast.method.name)
        elif len(res.mtype.partype) != len(at):
            raise TypeMismatchInStatement(ast)            
        else:
            match_type = zip(res.mtype.partype, at)
            for mt0,mt1 in match_type:
                
                if type(mt0) != type(mt1):
                    
                    if not(type(mt0), type(mt1)) == (FloatType, IntType):
                    #if type(mt0) != FloatType or type(mt1) != IntType:  
                    #if not isinstance(mt0,FloatType) or not isinstance(mt1,IntType):
                        raise TypeMismatchInStatement(ast)
                    else: pass
                    
            return res.mtype.rettype

    def visitBinaryOp(self, ast, c):
        
        left = self.visit(ast.left, c)
        #print(left)
        
        right = self.visit(ast.right, c)
        #print(right)
        check = check_operator(left, right)
        if ast.op in ['+','-','*']:
            if check:
                return check
            else: raise TypeMismatchInExpression(ast)
        elif ast.op == '/':
            if check:
                return FloatType()
            else: raise TypeMismatchInExpression(ast)
        elif ast.op.lower() in ['div','mod']:
            if type(check) is IntType:
                return check 
            else: raise TypeMismatchInExpression(ast)  
        elif ast.op.lower() in ['or','and','andthen','orelse']:
            if (type(left), type(right)) == (BoolType, BoolType):
                return BoolType()
            else: raise TypeMismatchInExpression(ast)
        else:
            if check:
                return BoolType()
            else: raise TypeMismatchInExpression(ast)
    
    def visitCallExpr(self,ast,c):
        at = [self.visit(x,c) for x in ast.param]
        
        res = self.lookup(ast.method.name,c,lambda x: x.name)
        if res is None or not type(res.mtype) is MType or type(res.mtype.rettype) is VoidType:
            raise Undeclared(Function(),ast.method.name)
        elif len(res.mtype.partype) != len(at):
            raise TypeMismatchInStatement(ast)            
        else:
            match_type = zip(res.mtype.partype, at)
            for mt0,mt1 in match_type:
                
                if type(mt0) != type(mt1):
                    
                    if not(type(mt0), type(mt1)) == (FloatType, IntType):
                    #if type(mt0) != FloatType or type(mt1) != IntType:  
                    #if not isinstance(mt0,FloatType) or not isinstance(mt1,IntType):
                    
                        raise TypeMismatchInStatement(ast)
                    else: pass
                    
            return res.mtype.rettype
    def visitUnaryOp(self, ast, c):
        expr = self.visit(ast.body, c)
        if ast.op == '-':
            if type(expr) == IntType:
                return IntType()
            elif type(expr) == FloatType:
                return FloatType()
            else: raise TypeMismatchInExpression(ast)
        else:           # ast.op == 'not':
            if type(expr) == BoolType:
                return BoolType()
            else: raise TypeMismatchInExpression(ast)
    def visitId(self, ast, c):
        declared_id = self.lookup(ast.name, c, lambda x: x.name)
        if declared_id is None or declared_id.mtype is MType :
            raise Undeclared(Identifier(),ast.name)
        else:
            if type(declared_id.mtype) == ArrayType:
                return declared_id.mtype
            else: return declared_id.mtype()
    

    '''def visitArrayType(self,ast,c):
        return ArrayType(ast.lower, ast.upper, ast.eleType)'''
    def visitArrayCell(self,ast,c):
        
        idxType = self.visit(ast.idx, c)
        idType = self.visit(ast.arr, c)
        
        if type(idType) != ArrayType or type(idxType) != IntType:
            raise TypeMismatchInExpression(ast) 
        else: return idType.eleType
    def visitIntLiteral(self,ast, c): 
        return IntType()
    def visitFloatLiteral(self,ast,c):
        return FloatType()
    def visitBooleanLiteral(self,ast,c):
        return BoolType()

