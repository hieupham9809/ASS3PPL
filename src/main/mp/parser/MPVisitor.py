# Generated from main/mp/parser/MP.g4 by ANTLR 4.7.1
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MPParser import MPParser
else:
    from MPParser import MPParser

# This class defines a complete generic visitor for a parse tree produced by MPParser.

class MPVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MPParser#program.
    def visitProgram(self, ctx:MPParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#declaration.
    def visitDeclaration(self, ctx:MPParser.DeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#varDec.
    def visitVarDec(self, ctx:MPParser.VarDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#listOfType.
    def visitListOfType(self, ctx:MPParser.ListOfTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#types.
    def visitTypes(self, ctx:MPParser.TypesContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#arraycp.
    def visitArraycp(self, ctx:MPParser.ArraycpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#funcDec.
    def visitFuncDec(self, ctx:MPParser.FuncDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#paramList.
    def visitParamList(self, ctx:MPParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#compound_st.
    def visitCompound_st(self, ctx:MPParser.Compound_stContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#procDec.
    def visitProcDec(self, ctx:MPParser.ProcDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#expression.
    def visitExpression(self, ctx:MPParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp1.
    def visitExp1(self, ctx:MPParser.Exp1Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp2.
    def visitExp2(self, ctx:MPParser.Exp2Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp3.
    def visitExp3(self, ctx:MPParser.Exp3Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp4.
    def visitExp4(self, ctx:MPParser.Exp4Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp5.
    def visitExp5(self, ctx:MPParser.Exp5Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp6.
    def visitExp6(self, ctx:MPParser.Exp6Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#exp7.
    def visitExp7(self, ctx:MPParser.Exp7Context):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#operand.
    def visitOperand(self, ctx:MPParser.OperandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#indexEx.
    def visitIndexEx(self, ctx:MPParser.IndexExContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#statement.
    def visitStatement(self, ctx:MPParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#assign_st.
    def visitAssign_st(self, ctx:MPParser.Assign_stContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#lhs.
    def visitLhs(self, ctx:MPParser.LhsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#while_st.
    def visitWhile_st(self, ctx:MPParser.While_stContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#for_st.
    def visitFor_st(self, ctx:MPParser.For_stContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#break_st.
    def visitBreak_st(self, ctx:MPParser.Break_stContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#continue_st.
    def visitContinue_st(self, ctx:MPParser.Continue_stContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#return_st.
    def visitReturn_st(self, ctx:MPParser.Return_stContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#with_st.
    def visitWith_st(self, ctx:MPParser.With_stContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#full_call_st.
    def visitFull_call_st(self, ctx:MPParser.Full_call_stContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#call_st.
    def visitCall_st(self, ctx:MPParser.Call_stContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#listOfExp.
    def visitListOfExp(self, ctx:MPParser.ListOfExpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#if_st.
    def visitIf_st(self, ctx:MPParser.If_stContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MPParser#arrayindex.
    def visitArrayindex(self, ctx:MPParser.ArrayindexContext):
        return self.visitChildren(ctx)



del MPParser