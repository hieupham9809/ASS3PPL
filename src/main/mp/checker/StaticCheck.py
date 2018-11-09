
"""
 * @author 
    Pham Minh Hieu - 1611046 - MT16TN
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
    
    if k == "variable":
        temp_name = decl.variable.name
        if any((temp_name.lower() == hde.name.lower() ) for hde in has_decl):
            raise Redeclared(Variable(), temp_name)
        else: return Symbol(temp_name,decl.varType)   
    elif k == "procedure": 
        temp_name = decl.name.name
        if any((temp_name.lower() == hde.name.lower() ) for hde in has_decl):
            if type(decl.returnType) is VoidType:
                raise Redeclared(Procedure(), temp_name)
            else: raise Redeclared(Function(), temp_name)
        else: return Symbol(temp_name,MType([x.varType for x in decl.param],decl.returnType))
    else:
        temp_name = decl.variable.name
        if any((temp_name.lower() == hde.name.lower() ) for hde in has_decl):
            raise Redeclared(Parameter(), temp_name)
        else: return Symbol(temp_name,decl.varType)    

    
def check_operator(left, right):
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
    
        func_decl = []
        
        for decl in ast.decl:
            if type(decl) is FuncDecl:
                func_decl.append(check_redeclared(func_decl,decl,"procedure"))
        
        find_entry = func_decl.copy()
        for decl in ast.decl:
            self.visit(decl, (has_decl,func_decl))
        
        res = self.lookup("main",find_entry,lambda x: x.name.lower())
        if res is None or not type(res.mtype) is MType or not type(res.mtype.rettype) is VoidType or not len(res.mtype.partype) == 0:
            raise NoEntryPoint()
        self.reach(func_decl,"main")
        if not func_decl:
            pass
        else: raise Unreachable(Procedure() if type(func_decl[0].mtype.rettype) is VoidType else Function(),func_decl[0].name)
        return []
    def check_inside(self,listStmt, c, k):
        
        has_ = False
        stmt_flag = 100
        
        for i in range(len(listStmt)):
            stmt_flag = self.visit(listStmt[i],c)
            if type(stmt_flag) is int:
                
                if stmt_flag == k:
                    if i != len(listStmt) - 1:
                        raise UnreachableStatement(listStmt[i+1])
                    else: 
                        has_ = True
            if type(listStmt[i]) is If and stmt_flag is True:
                if i != len(listStmt) - 1:
                    raise UnreachableStatement(listStmt[i+1])
                else: has_ = True
            if type(listStmt[i]) is With and stmt_flag is True:
                if i != len(listStmt) - 1:
                    raise UnreachableStatement(listStmt[i+1])
                else: has_ = True
        return has_
    def visitFuncDecl(self,ast, c):
        globaldecl = c[0].copy()
        returnType = ast.returnType
        listStmt = ast.body
        has_return = False
        isInLoop = False
        param_sub_scope = []
        local_sub_scope = []
        
        for vardecl in ast.param:
            param_sub_scope.append(check_redeclared(param_sub_scope, vardecl,"parameter"))
        local_sub_scope += param_sub_scope
        
        for vardecl in ast.local:
            local_sub_scope.append(check_redeclared(local_sub_scope, vardecl,"variable"))

        has_return = self.check_inside(listStmt, (local_sub_scope+globaldecl,returnType,isInLoop,c[1],ast.name.name),1) 
        
        if has_return == False and not type(returnType) is VoidType:
            raise FunctionNotReturn(ast.name.name)
         
    def arrayTypeCompare(self,funcReturnType, exprType):
        lower = funcReturnType.lower == exprType.lower
        upper = funcReturnType.upper == exprType.upper
        eleType = type(funcReturnType.eleType) == type(exprType.eleType)
        
        return lower and upper and eleType
    def visitReturn(self, ast, c):
        returnExp = ast.expr
          
        if type(c[1]) != VoidType:
            
            if returnExp is None:
                raise TypeMismatchInStatement(ast)
            else: 
                
                typeExp = self.visit(returnExp,c)
                if type(c[1]) is ArrayType:
                    if not type(typeExp) is ArrayType:
                        raise TypeMismatchInStatement(ast)
                    else:
                        if not self.arrayTypeCompare(c[1], typeExp):
                            raise TypeMismatchInStatement(ast)
                
                if type(typeExp) != type(c[1]):
                    if not type(typeExp) is IntType or not type(c[1]) is FloatType:
                        raise TypeMismatchInStatement(ast)
        else:
            if not returnExp is None:
                raise TypeMismatchInStatement(ast)
        
        return 1
    def visitIf(self,ast,c):
        expr = ast.expr
        thenStmt = ast.thenStmt
        elseStmt = ast.elseStmt
        
        typeOfExpr = self.visit(expr,c)
        if not type(typeOfExpr) is BoolType:
            raise TypeMismatchInStatement(ast)
        
        thenCheck = self.check_inside(thenStmt,c,1)
        elseCheck = self.check_inside(elseStmt,c,1)
        return (thenCheck and elseCheck)
    def visitWith(self,ast,c):
        globalList = c[0].copy()
        localList = []
        for decl in ast.decl:
            localList.append(check_redeclared(localList,decl,"variable"))
        return self.check_inside(ast.stmt,(localList + globalList,c[1],c[2],c[3],c[4]),1)

    def visitWhile(self,ast,c):
        expr = ast.exp
        listStmt = ast.sl
        isInLoop = True

        typeOfExpr = self.visit(expr,c)
        
        if not type(typeOfExpr) is BoolType:
            raise TypeMismatchInStatement(ast)
        
        return self.check_inside(listStmt,(c[0],c[1],isInLoop,c[3],c[4]),1)
    def visitFor(self,ast,c):
        id = self.visit(ast.id,c)
        expr1 = self.visit(ast.expr1,c)
        expr2 = self.visit(ast.expr2,c)
        listStmt = ast.loop
        isInLoop = True
        
        if not type(id) is IntType or not type(expr1) is IntType or not type(expr2) is IntType:
            raise TypeMismatchInStatement(ast)
        return self.check_inside(listStmt,(c[0],c[1],isInLoop,c[3],c[4]),1)
    def visitContinue(self, ast, c):
        if c[2] == False:
            raise ContinueNotInLoop()
        else:
            return 1
    def visitBreak(self,ast,c):
        if c[2] == False:
            raise BreakNotInLoop()
        else:
            return 1

    def reach(self, func_decl_list, func_decl_name):
        
        for i in range(len(func_decl_list)):
            if func_decl_list[i].name.lower() == func_decl_name.lower():
                del func_decl_list[i]
                break
        

    def visitCallStmt(self, ast, c): 
        if ast.method.name != c[4]:
            self.reach(c[3], ast.method.name)
        
        at = [self.visit(x,c) for x in ast.param]
        res = self.lookup(ast.method.name.lower(),c[0],lambda x: x.name.lower()) 
        
        if res is None or not type(res.mtype) is MType or not type(res.mtype.rettype) is VoidType:
            raise Undeclared(Procedure(),ast.method.name)
        elif len(res.mtype.partype) != len(at):
            raise TypeMismatchInStatement(ast)            
        else:
            match_type = zip(res.mtype.partype, at)
            for mt0,mt1 in match_type:
                
                if type(mt0) != type(mt1):
                    if not type(mt0) is FloatType or not type(mt1) is IntType:
                        raise TypeMismatchInStatement(ast)
                    else: pass
                else:
                    if type(mt0) is ArrayType:
                        if not self.arrayTypeCompare(mt0,mt1):
                            raise TypeMismatchInStatement(ast)
                    
            return res.mtype.rettype

    def visitBinaryOp(self, ast, c):
        
        left = self.visit(ast.left, c)
        right = self.visit(ast.right, c)
        
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
        if ast.method.name != c[4]:
            self.reach(c[3], ast.method.name)
        at = [self.visit(x,c) for x in ast.param]
        
        res = self.lookup(ast.method.name.lower(),c[0],lambda x: x.name.lower())
        if res is None or not type(res.mtype) is MType or type(res.mtype.rettype) is VoidType:
            raise Undeclared(Function(),ast.method.name)
        elif len(res.mtype.partype) != len(at):
            raise TypeMismatchInExpression(ast)            
        else:
            match_type = zip(res.mtype.partype, at)
            for mt0,mt1 in match_type:
                
                if type(mt0) != type(mt1):
                    if not(type(mt0), type(mt1)) == (FloatType, IntType):
                        raise TypeMismatchInExpression(ast)
                    else: pass
                else:
                    if type(mt0) is ArrayType:
                        if not self.arrayTypeCompare(mt0,mt1):
                            raise TypeMismatchInExpression(ast)
                    
            return res.mtype.rettype
    def visitUnaryOp(self, ast, c):
        expr = self.visit(ast.body, c)
        if ast.op == '-':
            if type(expr) == IntType:
                return IntType()
            elif type(expr) == FloatType:
                return FloatType()
            else: raise TypeMismatchInExpression(ast)
        else:           
            if type(expr) == BoolType:
                return BoolType()
            else: raise TypeMismatchInExpression(ast)
    def visitId(self, ast, c):
        declared_id = self.lookup(ast.name.lower(), c[0], lambda x: x.name.lower())
        if declared_id is None or type(declared_id.mtype) is MType :
            raise Undeclared(Identifier(),ast.name)
        else:
            return declared_id.mtype

    def visitArrayCell(self,ast,c):
        
        idxType = self.visit(ast.idx, c)
        idType = self.visit(ast.arr, c)
        
        if type(idType) != ArrayType or type(idxType) != IntType:
            raise TypeMismatchInExpression(ast) 
        else: return idType.eleType

    def visitAssign(self,ast,c):
        lhs = self.visit(ast.lhs, c)
        exp = self.visit(ast.exp, c)

        if type(lhs) in [StringType, ArrayType]:
            
            raise TypeMismatchInStatement(ast)
        else:
            
            if type(lhs) != type(exp):
                if not (type(lhs),type(exp)) == (FloatType, IntType):
                    raise TypeMismatchInStatement(ast)

    def visitIntLiteral(self,ast, c): 
        return IntType()
    def visitFloatLiteral(self,ast,c):
        return FloatType()
    def visitBooleanLiteral(self,ast,c):
        return BoolType()
    def visitStringLiteral(self,ast,c):
        return StringType()

