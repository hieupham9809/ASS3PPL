import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    '''def test_redeclared_builtin_procedure(self):
        """Simple program: int main() {} """
        input = Program([
                FuncDecl(Id("putIntLn"),[],[],[])])
        expect = "Redeclared Procedure: putIntLn"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_redeclared_builtin_function(self):
        """Simple program: int main() {} """
        input = Program([
                FuncDecl(Id("getInt"),[],[],[],IntType)])
        expect = "Redeclared Function: getInt"
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_redeclared_procedure(self):
        """Simple program: int main() {} """
        input = Program([
                FuncDecl(Id("foo"),[],[],[]),
                FuncDecl(Id("foo"),[],[],[])])
        expect = "Redeclared Procedure: foo"
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_redeclared_param_vs_local(self):
        """Simple program: int main() {} """
        input = Program([
                FuncDecl(Id("foo"),[VarDecl(Id("a"),IntType)],[VarDecl(Id("a"),IntType)],[])])
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_redeclared_param(self):
        """Simple program: int main() {} """
        input = Program([
                VarDecl(Id("name"),FloatType),
                FuncDecl(Id("foo2"),[VarDecl(Id("name"),IntType)],[],[]),
                FuncDecl(Id("foo"),[VarDecl(Id("a"),IntType),VarDecl(Id("a"),IntType)],[],[])])
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_type_not_coerc_int_float(self):
        """Simple program: int main() {} """
        input = Program([
                FuncDecl(Id("foo"),[],[],[CallStmt(Id("putInt"),[BinaryOp('+',IntLiteral(1), FloatLiteral(2.1))])])])
        expect = "Type Mismatch In Statement: CallStmt(Id(putInt),[BinaryOp(+,IntLiteral(1),FloatLiteral(2.1))])"
        self.assertTrue(TestChecker.test(input,expect,405))
    
    def test_type_coerc_int_float(self):
        """Simple program: int main() {} """
        input = Program([
                FuncDecl(Id("foo"),[],[],[CallStmt(Id("putFloat"),[BinaryOp('+',IntLiteral(1), IntLiteral(2))]),
                                        CallStmt(Id("putInt"),[BinaryOp('+',FloatLiteral(1.3), IntLiteral(2))])])])
        expect = "Type Mismatch In Statement: CallStmt(Id(putInt),[BinaryOp(+,FloatLiteral(1.3),IntLiteral(2))])"
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_and_or_boolean(self):
        """Simple program: int main() {} """
        input = Program([
                FuncDecl(Id("foo"),[],[],[CallStmt(Id("putBoolLn"),[BinaryOp('and',BooleanLiteral(True), BooleanLiteral(False))]),
                                        CallStmt(Id("putBool"),[BinaryOp('or',IntLiteral(1), FloatLiteral(2.1))])])])
        expect = "Type Mismatch In Expression: BinaryOp(or,IntLiteral(1),FloatLiteral(2.1))"
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_andthen_orelse_boolean(self):
        """Simple program: int main() {} """
        input = Program([
                FuncDecl(Id("foo"),[],[],[CallStmt(Id("putBoolLn"),[BinaryOp('andthen',BooleanLiteral(True), BooleanLiteral(False))]),
                                        CallStmt(Id("putBool"),[BinaryOp('orelse',IntLiteral(1), FloatLiteral(2.1))])])])
        expect = "Type Mismatch In Expression: BinaryOp(orelse,IntLiteral(1),FloatLiteral(2.1))"
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_Unary_Type_sub(self):
        """Simple program: int main() {} """
        input = Program([
                FuncDecl(Id("foo"),[],[],[CallStmt(Id("putIntLn"),[UnaryOp('-', IntLiteral(1))]),
                                        CallStmt(Id("putInt"),[UnaryOp('-',StringLiteral("string in unaryop"))])])])
        expect = "Type Mismatch In Expression: UnaryOp(-,StringLiteral(string in unaryop))"
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_Unary_Type_Not(self):
        """Simple program: int main() {} """
        input = Program([
                FuncDecl(Id("foo"),[],[],[CallStmt(Id("putBoolLn"),[UnaryOp('not', BooleanLiteral(True))]),
                                        CallStmt(Id("putBool"),[UnaryOp('not',StringLiteral("string in unaryop"))])])])
        expect = "Type Mismatch In Expression: UnaryOp(not,StringLiteral(string in unaryop))"
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_Unary_Type_Not(self):
        """Simple program: int main() {} """
        input = Program([
                FuncDecl(Id("foo"),[],[],[CallStmt(Id("putBoolLn"),[UnaryOp('not', BinaryOp('>',IntLiteral(1),IntLiteral(2)))]),
                                        CallStmt(Id("putBool"),[UnaryOp('not',BinaryOp('+', IntLiteral(10000), IntLiteral(0)))])])])
        expect = "Type Mismatch In Expression: UnaryOp(not,BinaryOp(+,IntLiteral(10000),IntLiteral(0)))"
        self.assertTrue(TestChecker.test(input,expect,411))
    def test_Undeclared_id(self):
        """Simple program: int main() {} """
        input = Program([
                VarDecl(Id("a"),IntType),
                FuncDecl(Id("foo"),[],[],[CallStmt(Id("putBoolLn"),[BinaryOp('>',Id("a"),IntLiteral(2))]),
                                        CallStmt(Id("putBool"),[BinaryOp('>',Id("b"),IntLiteral(2))])])])
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_Declared_id_in_local(self):
        """More complex program"""
        input = Program([
                
                FuncDecl(Id("foo"),[],[VarDecl(Id("a"),IntType)],[CallStmt(Id("putBoolLn"),[BinaryOp('>',Id("a"),IntLiteral(2))]),
                                        CallStmt(Id("putBool"),[BinaryOp('>',Id("b"),IntLiteral(2))])])])
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input,expect,413))
    
    def test_Declared_id_in_param(self):
        """More complex program"""
        input = Program([
                
                FuncDecl(Id("foo"),[VarDecl(Id("a"),IntType)],[],[CallStmt(Id("putBoolLn"),[BinaryOp('>',Id("a"),IntLiteral(2))]),
                                        CallStmt(Id("putBool"),[BinaryOp('>',Id("b"),IntLiteral(2))])])])
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input,expect,414))'''
    
    def test_Declared_inside_hidden_outside(self):
        """More complex program"""
        input = Program([
                VarDecl(Id("a"),FloatType),
                FuncDecl(Id("foo"),[VarDecl(Id("a"),StringType)],[],[CallStmt(Id("putFloatLn"),[Id("a")])
                                        ])])
        expect = "Type Mismatch In Statement: CallStmt(Id(putFloatLn),[Id(a)])"
        self.assertTrue(TestChecker.test(input,expect,415))

    def Atest_undeclared_function_use_ast(self):
        """Simple program: int main() {} """
        input = Program([FuncDecl(Id("main"),[],[],[
            CallStmt(Id("foo"),[])])])
        expect = "Undeclared Procedure: foo"
        self.assertTrue(TestChecker.test(input,expect,420))

    def Atest_diff_numofparam_expr_use_ast(self):
        """More complex program"""
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[])])])
                        
        expect = "Type Mismatch In Statement: CallStmt(Id(putIntLn),[])"
        self.assertTrue(TestChecker.test(input,expect,421))

    
    