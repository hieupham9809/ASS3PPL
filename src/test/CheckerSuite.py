import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    def test_redeclared_builtin_procedure(self):
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

    def test_diff_numofparam_stmt(self):
        """More complex program"""
        input = """procedure main (); begin
            putIntLn();
        end"""
        expect = "Type Mismatch In Statement: CallStmt(Id(putIntLn),[])"
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_undeclared_function_use_ast(self):
        """Simple program: int main() {} """
        input = Program([FuncDecl(Id("main"),[],[],[
            CallStmt(Id("foo"),[])])])
        expect = "Undeclared Procedure: foo"
        self.assertTrue(TestChecker.test(input,expect,420))

    def test_diff_numofparam_expr_use_ast(self):
        """More complex program"""
        input = Program([
                FuncDecl(Id("main"),[],[],[
                    CallStmt(Id("putIntLn"),[])])])
                        
        expect = "Type Mismatch In Statement: CallStmt(Id(putIntLn),[])"
        self.assertTrue(TestChecker.test(input,expect,421))

    
    