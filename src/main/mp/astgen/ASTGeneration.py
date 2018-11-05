from MPVisitor import MPVisitor
from MPParser import MPParser
from AST import *

class ASTGeneration(MPVisitor):
    def visitProgram(self,ctx:MPParser.ProgramContext):
        templist = []
        for decl in ctx.declaration():
            templist += self.visit(decl)
        return Program(templist)


    def visitDeclaration(self, ctx:MPParser.DeclarationContext):
        if ctx.varDec():
            return self.visit(ctx.varDec())
        else:
            if ctx.funcDec():
                return self.visit(ctx.funcDec())
            else: return self.visit(ctx.procDec())

    def visitVarDec(self, ctx:MPParser.VarDecContext):
        listOfType = ctx.listOfType()
        listOfVarDecl = []
        for x in listOfType:
            listid, types = self.visit(x)
            for id in listid:
                listOfVarDecl.append(VarDecl(Id(id),types))       
        return (listOfVarDecl)
    def visitListOfType(self, ctx:MPParser.ListOfTypeContext):
        listid = []
        if type(ctx.ID()) is list:
            for listlistid in ctx.ID():
                listid.append(listlistid.getText())
        else: listid.append(ctx.ID().getText())
        
        
        return listid,self.visit(ctx.types())

    def visitTypes(self, ctx:MPParser.TypesContext):
        if ctx.BOOLEAN(): return BoolType()
        elif ctx.INTEGER(): return IntType()
        elif ctx.REAL(): return FloatType()
        elif ctx.STRING(): return StringType()
        else: return self.visit(ctx.arraycp())

    def visitArraycp(self, ctx:MPParser.ArraycpContext):
        temp = ""
        if ctx.BOOLEAN(): temp = BoolType()
        elif ctx.INTEGER(): temp = IntType()
        elif ctx.REAL(): temp = FloatType()
        else: temp = StringType()
        
        return ArrayType(int(self.visit(ctx.arrayindex(0))),
                        int(self.visit(ctx.arrayindex(1))),
                        temp
                                                        )
    def visitArrayindex(self, ctx:MPParser.ArrayindexContext):
        if ctx.SUBOP():
            return str(ctx.SUBOP().getText()) + str(ctx.INTLIT().getText())
        else: return str(ctx.INTLIT().getText())
    def visitFuncDec(self, ctx:MPParser.FuncDecContext):
        name = Id(ctx.ID().getText())
        param = self.visit(ctx.paramList())
        returnType = self.visit(ctx.types())
        if ctx.varDec():
            local = self.visit(ctx.varDec())
        else: local = []
        body = self.visit(ctx.compound_st())
        return [FuncDecl(name,param,local,body,returnType)]

    def visitProcDec(self, ctx:MPParser.ProcDecContext):
        name = Id(ctx.ID().getText())
        param = self.visit(ctx.paramList())
        if ctx.varDec():
            local = self.visit(ctx.varDec())
        else: local = []
        if ctx.compound_st():
            body = self.visit(ctx.compound_st())
        else: body = []
        return [FuncDecl(name,param,local,body)]
    def visitParamList(self, ctx:MPParser.ParamListContext):
        listOfVarDecl = []
        listOfType = ctx.listOfType()
        if not listOfType:
            return []
        else:
            for x in listOfType:
                listid, types = self.visit(x)
                for id in listid:
                    listOfVarDecl.append(VarDecl(Id(id),types))
            return listOfVarDecl
    def visitCompound_st(self, ctx:MPParser.Compound_stContext):
        statements = ctx.statement()
        statementsList = []
        if not statements:
            return []
        else:
            for statement in statements:
                statementsList += self.visit(statement)
            
        return statementsList

    def visitStatement(self, ctx:MPParser.StatementContext):
        if ctx.assign_st():
            return self.visit(ctx.assign_st())
        elif ctx.if_st():
            return self.visit(ctx.if_st())
        elif ctx.for_st():
            return self.visit(ctx.for_st())
        elif ctx.while_st():
            return self.visit(ctx.while_st())
        elif ctx.break_st():
            return self.visit(ctx.break_st())
        elif ctx.continue_st():
            return self.visit(ctx.continue_st())
        elif ctx.return_st():
            return self.visit(ctx.return_st())
        elif ctx.full_call_st():
            return self.visit(ctx.full_call_st())
        elif ctx.compound_st():
            return self.visit(ctx.compound_st())
        else: 
            return self.visit(ctx.with_st())

    def visitAssign_st(self, ctx:MPParser.Assign_stContext):
        assignList = []
        lhs = ctx.lhs()
        #print(lhs)
        exp = ctx.expression()
        
        if type(lhs) is list:
            for i in reversed(lhs):
                assignList.append(Assign(self.visit(i),self.visit(exp)))
                exp = i
        else: assignList.append(Assign(self.visit(lhs),self.visit(exp)))
        return assignList

    def visitLhs(self, ctx:MPParser.LhsContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        else: return self.visit(ctx.indexEx())
    def visitIndexEx(self, ctx:MPParser.IndexExContext):
        return ArrayCell(self.visit(ctx.exp5()),self.visit(ctx.expression()))
    def visitExpression(self, ctx:MPParser.ExpressionContext):
        if (ctx.THEN()):
            return BinaryOp('andthen',self.visit(ctx.expression()),self.visit(ctx.exp1()))
        elif (ctx.ELSE()):
            return BinaryOp('orelse',self.visit(ctx.expression()), self.visit(ctx.exp1()))
        else: return self.visit(ctx.exp1())
    def visitExp1(self, ctx:MPParser.Exp1Context):
        op = ""
        if ctx.EQOP(): op = ctx.EQOP().getText()
        elif ctx.NEQOP(): op = ctx.NEQOP().getText()
        elif ctx.LTOP(): op = ctx.LTOP().getText()
        elif ctx.LTEOP(): op = ctx.LTEOP().getText()
        elif ctx.GTOP(): op = ctx.GTOP().getText()
        elif ctx.GTEOP(): op = ctx.GTEOP().getText()
        else: return self.visit(ctx.exp2(0))
        
        return BinaryOp(op,self.visit(ctx.exp2(0)),self.visit(ctx.exp2(1)))

    def visitExp2(self, ctx:MPParser.Exp2Context):
        op = ""
        if ctx.ADDOP(): op = ctx.ADDOP().getText()
        elif ctx.SUBOP(): op = ctx.SUBOP().getText()
        elif ctx.OR(): op = ctx.OR().getText()
        else: return self.visit(ctx.exp3())

        return BinaryOp(op, self.visit(ctx.exp2()), self.visit(ctx.exp3()))

    def visitExp3(self, ctx:MPParser.Exp3Context):
        op = ""
        if ctx.DIVOP(): op = ctx.DIVOP().getText()
        elif ctx.MULOP(): op = ctx.MULOP().getText()
        elif ctx.DIV(): op = ctx.DIV().getText()
        elif ctx.MOD(): op = ctx.MOD().getText()
        elif ctx.AND(): op = ctx.AND().getText()
        else: return self.visit(ctx.exp4())

        return BinaryOp(op, self.visit(ctx.exp3()), self.visit(ctx.exp4()))

    def visitExp4(self, ctx:MPParser.Exp4Context):
        op = ""
        if ctx.SUBOP(): op = ctx.SUBOP().getText()
        elif ctx.NOT(): op = ctx.NOT().getText()
        else: return self.visit(ctx.exp5())

        return UnaryOp(op, self.visit(ctx.exp4()))
    
    def visitExp5(self, ctx:MPParser.Exp5Context):
        if ctx.LSB():
            return ArrayCell(self.visit(ctx.exp5()), self.visit(ctx.expression()))
        else: return self.visit(ctx.exp6())
    def visitExp6(self, ctx:MPParser.Exp6Context):
        if ctx.LB():
            return self.visit(ctx.expression())
        else: return self.visit(ctx.exp7())
    def visitExp7(self, ctx:MPParser.Exp7Context):
        if ctx.operand():
            return self.visit(ctx.operand())
        else: return self.visit(ctx.call_st())
    ####visitOperand problem: FloatLiteral
    def visitOperand(self, ctx:MPParser.OperandContext):
        if ctx.INTLIT(): return IntLiteral(int(ctx.INTLIT().getText()))
        elif ctx.REALIT(): return FloatLiteral(float(ctx.REALIT().getText()))
        elif ctx.STRLIT(): return StringLiteral(ctx.STRLIT().getText())
        elif ctx.BOOLIT(): return BooleanLiteral(True if (ctx.BOOLIT().getText().lower()) == 'true' else False)
        else: return Id(ctx.ID().getText())

    #def visitIndexEx(self, ctx:MPParser.IndexExContext):
    #    return ArrayCell(self.visit(ctx.exp5()), self.visit(ctx.expression()))
    
    def visitWhile_st(self, ctx:MPParser.While_stContext): 
        return [While(self.visit(ctx.expression()),self.visit(ctx.statement()))]

    def visitBreak_st(self, ctx:MPParser.Break_stContext):
        return [Break()]
    def visitContinue_st(self, ctx:MPParser.Continue_stContext):
        return [Continue()]
    def visitReturn_st(self, ctx:MPParser.Return_stContext):
        if ctx.expression():
            return [Return(self.visit(ctx.expression()))]
        else: return [Return()]
    
    def visitCall_st(self, ctx:MPParser.Call_stContext):
        return CallExpr(Id(ctx.ID().getText()),self.visit(ctx.listOfExp()))
    def visitWith_st(self, ctx:MPParser.With_stContext):
        listOfType = ctx.listOfType()
        if type(listOfType) is not list:
            listOfType = list(listOfType)
        listOfVarDecl = []
        for x in listOfType:
            listid, types = self.visit(x)
            for id in listid:
                listOfVarDecl.append(VarDecl(Id(id),types))
           
        return [With(listOfVarDecl,self.visit(ctx.statement()))]
    #################################
    def visitFull_call_st(self, ctx:MPParser.Full_call_stContext):
        temp = self.visit(ctx.call_st())
        return [CallStmt(temp.method,temp.param)]
    def visitListOfExp(self, ctx:MPParser.ListOfExpContext):
        listOfExp = []
        if not ctx.expression():
            return []
        elif type(ctx.expression()) is list:
            for expr in ctx.expression():
                listOfExp.append(self.visit(expr))
        else: listOfExp.append(self.visit(ctx.expression()))
        return listOfExp
    
    def visitIf_st(self, ctx:MPParser.If_stContext):
        return [If(self.visit(ctx.expression())
            ,self.visit(ctx.statement(0)) 
            ,self.visit(ctx.statement(1)) if ctx.ELSE() else [])]
        
    def visitFor_st(self, ctx:MPParser.For_stContext):
        id = Id(ctx.ID().getText())
        expr1 = self.visit(ctx.expression(0))
        expr2 = self.visit(ctx.expression(1))
        loop = self.visit(ctx.statement())
        up = True if ctx.TO() else False 
        return [For(id,expr1,expr2,up,loop)]
    
    # def visitProgram(self,ctx:MPParser.ProgramContext):
    #     listDec = []
    #     for dec in ctx.declaration():
    #         listDec += self.visit(dec)
    #     return Program(listDec)
    # def visitDeclaration(self,ctx:MPParser.DeclarationContext):
    #     if ctx.varDec(): return self.visit(ctx.varDec())
    #     elif ctx.funcDec(): return self.visit(ctx.funcDec())
    #     else: return self.visit(ctx.procDec())
    # def visitVarDec(self,ctx:MPParser.VarDecContext):
    #     listVarDec = []
    #     for listoftype in ctx.listOfType():
    #         listID, types = self.visit(listoftype)
    #         for id in listID:
    #             listVarDec += [VarDecl(id,types)]
    #     return listVarDec
    # def visitListOfType(self,ctx:MPParser.ListOfTypeContext):
    #     listID = []
    #     if type(ctx.ID()) is list:
    #         for id in ctx.ID():
    #             listID += [id.getText()]
    #     else: listID += [ctx.ID().getText()]
    #     return listID, self.visit(ctx.types())

    # def visitTypes(self,ctx:MPParser.TypesContext):
    #     if ctx.BOOLEAN(): return BoolType()
    #     elif ctx.INTEGER(): return IntType()
    #     elif ctx.REAL(): return FloatType()
    #     elif ctx.STRING(): return StringType()
    #     else: return self.visit(ctx.arraycp())
    # def visitArraycp(self,ctx:MPParser.ArraycpContext):
    #     temp = ""
    #     if ctx.BOOLEAN(): temp = BoolType()
    #     elif ctx.INTEGER(): temp = IntType()
    #     elif ctx.REAL(): temp = FloatType()
    #     else: temp = StringType()
        
    #     return ArrayType(self.visit(ctx.arrayindex(0)), self.visit(ctx.arrayindex(1)), temp)
    # def visitArrayindex(self,ctx:MPParser.ArrayindexContext):
    #     if ctx.SUBOP(): return int(ctx.SUBOP().getText() + ctx.INTLIT().getText())
    #     else: return int(ctx.INTLIT().getText())
    # def visitFuncDec(self,ctx:MPParser.FuncDecContext):
    #     name = ctx.ID().getText()
    #     param = self.visit(ctx.paramList())
    #     returntype = self.visit(ctx.types())
    #     local = self.visit(ctx.varDec()) if ctx.varDec() else []
    #     body = self.visit(ctx.compound_st())
    #     return FuncDecl(name,param,local,body,returntype)
    # def visitParamList(self,ctx:MPParser.ParamListContext):
    #     if not ctx.listOfType(): return []
    #     else:
    #         listVarDec = []
    #         for listoftype in ctx.listOfType():
    #             listID, types = self.visit(listoftype)
    #             for id in listID:
    #                 listVarDec += [VarDecl(id,types)]
    #         return listVarDec
    # def visitCompound_st(self,ctx:MPParser.Compound_stContext):
    #     if not ctx.statement(): return []
    #     else:
    #         liststmt = []
    #         for stmt in ctx.statement():
    #             liststmt += self.visit(stmt)
                
    #         return liststmt
    # def visitStatement(self,ctx:MPParser.StatementContext):
    #     if ctx.assign_st(): return self.visit(ctx.assign_st()) 
    #     elif ctx.if_st(): return self.visit(ctx.if_st())
    #     elif ctx.for_st(): return self.visit(ctx.for_st())
    #     elif ctx.while_st(): return self.visit(ctx.while_st())
    #     elif ctx.break_st(): return self.visit(ctx.break_st())
    #     elif ctx.continue_st(): return self.visit(ctx.continue_st())
    #     elif ctx.return_st(): return self.visit(ctx.return_st())
    #     elif ctx.full_call_st(): return self.visit(ctx.full_call_st())
    #     elif ctx.compound_st(): return self.visit(ctx.compound_st())
    #     else: return self.visit(ctx.with_st())
    # def visitExpression(self,ctx:MPParser.ExpressionContext):
    #     if ctx.AND(): return BinaryOp('andthen',self.visit(ctx.expression()),self.visit(ctx.exp1()))
    #     elif ctx.OR(): return BinaryOp('orelse',self.visit(ctx.expression()),self.visit(ctx.exp1()))
    #     else: return self.visit(ctx.exp1())
    # def visitExp1(self,ctx:MPParser.Exp1Context):
    #     op = ""
    #     if ctx.EQOP(): op = ctx.EQOP().getText()
    #     elif ctx.NEQOP(): op = ctx.NEQOP().getText()
    #     elif ctx.LTOP(): op = ctx.LTOP().getText()
    #     elif ctx.LTEOP(): op = ctx.LTEOP().getText()
    #     elif ctx.GTOP(): op = ctx.GTOP().getText()
    #     elif ctx.GTEOP(): op = ctx.GTEOP().getText()
    #     else: return self.visit(ctx.exp2())
    #     return BinaryOp(op,self.visit(ctx.exp2(0)),self.visit(ctx.exp2(1)))
    # def visitExp2(self,ctx:MPParser.Exp2Context):
    #     op = ""
    #     if ctx.ADDOP(): op = ctx.ADDOP().getText()
    #     elif ctx.SUBOP(): op = ctx.SUBOP().getText()
    #     elif ctx.OR(): op = ctx.OR().getText()
    #     else: return self.visit(ctx.exp3())
    #     return BinaryOp(op,self.visit(ctx.exp2()),self.visit(ctx.exp3()))
    # def visitExp3(self,ctx:MPParser.Exp3Context):
    #     op = ""
    #     if ctx.DIVOP(): op = ctx.DIVOP().getText()
    #     elif ctx.MULOP(): op = ctx.MULOP().getText()
    #     elif ctx.DIV(): op = ctx.DIV().getText()
    #     elif ctx.MOD(): op = ctx.MOD().getText()
    #     elif ctx.AND(): op = ctx.AND().getText()
    #     else: return self.visit(ctx.exp4())
    #     return BinaryOp(op,self.visit(ctx.exp3()),self.visit(ctx.exp4()))
    # def visitExp4(self,ctx:MPParser.Exp4Context):
    #     op = ""
    #     if ctx.SUBOP(): op = ctx.SUBOP().getText()
    #     elif ctx.NOT(): op = ctx.NOT().getText()
    #     else: return self.visit(ctx.exp5())
    #     return UnaryOp(op,self.visit(ctx.exp4()))
    # def visitExp5(self,ctx:MPParser.Exp5Context):
    #     if ctx.expression():
    #         return ArrayCell(self.visit(ctx.exp5()), self.visit(ctx.expression()))
    #     else: return self.visit(ctx.exp6())
    # def visitExp6(self,ctx:MPParser.Exp6Context):
    #     if ctx.expression(): return self.visit(ctx.expression())
    #     else: return self.visit(ctx.exp7())
    # def visitExp7(self,ctx:MPParser.Exp7Context):
    #     if ctx.operand(): return self.visit(ctx.operand())
    #     else: return self.visit(ctx.call_st())
    # def visitOperand(self,ctx:MPParser.OperandContext):
    #     if ctx.INTLIT(): return IntLiteral(int(ctx.INTLIT().getText()))
    #     elif ctx.REALIT(): return FloatLiteral(float(ctx.REALIT().getText()))
    #     elif ctx.STRLIT(): return StringLiteral(ctx.STRLIT().getText())
    #     elif ctx.ID(): return Id(ctx.ID().getText())
    #     else: return BooleanLiteral(ctx.BOOLIT().getText().lower() == 'true')
            
    