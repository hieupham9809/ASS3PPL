import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):

    # test redeclare 
    def test_redeclare_0(self):
        code = Program([
            VarDecl(Id("a"), IntType()),
            VarDecl(Id("a"), FloatType())
        ])
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(code,expect,400))

    def test_redeclare_1(self):
        code = Program([
            VarDecl(Id("a"), IntType()),
            FuncDecl(Id("a"),[],[],[Return(FloatLiteral(1.0))], FloatType())
        ])
        expect = "Redeclared Function: a"
        self.assertTrue(TestChecker.test(code,expect,401))

    def test_redeclare_2(self):
        code = Program([
            VarDecl(Id("a"), IntType()),
            FuncDecl(Id("a"),[],[],[], VoidType())
        ])
        expect = "Redeclared Procedure: a"
        self.assertTrue(TestChecker.test(code,expect,402))

    def test_redeclare_3(self):
        code = Program([
            FuncDecl(Id("a"),[],[],[], VoidType()),
            VarDecl(Id("a"), IntType())
        ])
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(code,expect,403))

    def test_redeclare_4(self):
        """ redeclare param """
        code = Program([
            VarDecl(Id("a"), IntType()),
            FuncDecl(
                Id("a"),
                [
                    VarDecl(Id("p1"), IntType()),
                    VarDecl(Id("p2"), IntType()),
                    VarDecl(Id("p1"), IntType())
                ],
                [],
                [], 
                VoidType())
        ])
        expect = "Redeclared Procedure: a"
        self.assertTrue(TestChecker.test(code,expect,404))

    def test_redeclare_5(self):
        """ redeclare local var """
        code = Program([
            VarDecl(Id("a"), IntType()),
            FuncDecl(
                Id("a"),
                [
                    VarDecl(Id("p1"), IntType()),
                    VarDecl(Id("p2"), IntType()),
                    VarDecl(Id("p3"), IntType())
                ],
                [
                    VarDecl(Id("p1"), IntType()),
                ],
                [], 
                VoidType())
        ])
        expect = "Redeclared Procedure: a"
        self.assertTrue(TestChecker.test(code,expect,405))
    

    def test_undeclare_1(self):
        code = """
            procedure main();
            begin
                foo();
            end
        """

        expect = "Undeclared Procedure: foo"
        self.assertTrue(TestChecker.test(code,expect,406))

    def test_undeclare_2(self):
        code = """
            procedure main();
            begin
                A := foo();
            end
        """

        expect = "Undeclared Identifier: A"
        self.assertTrue(TestChecker.test(code,expect,407))

    def test_undeclare_3(self):
        code = """
            var a: String;
            procedure main();
            var a: integer;
            begin
                A := foo();
            end
        """

        expect = "Undeclared Function: foo"
        self.assertTrue(TestChecker.test(code,expect,408))


    def test_typemissmatch_1(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure main();
                
            begin
                if a then a:=1;
            end
        """

        expect = "Type Mismatch In Statement: If(Id(a),[AssignStmt(Id(a),IntLiteral(1))],[])"
        self.assertTrue(TestChecker.test(code,expect,409))

    def test_typemissmatch_2(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure main();
                var i:integer;
                j:real;
            begin
                for j:=1 to 10 do a:=1;
            end
        """

        expect = "Type Mismatch In Statement: For(Id(j)IntLiteral(1),IntLiteral(10),True,[AssignStmt(Id(a),IntLiteral(1))])"
        self.assertTrue(TestChecker.test(code,expect,410))

    def test_typemissmatch_3(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure main();
                var i:integer;
                j:real;
            begin
                for i:=1.0 to 10 do a:=1;
            end
        """

        expect = "Type Mismatch In Statement: For(Id(i)FloatLiteral(1.0),IntLiteral(10),True,[AssignStmt(Id(a),IntLiteral(1))])"
        self.assertTrue(TestChecker.test(code,expect,411))

    def test_typemissmatch_4(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure main();
                var i:integer;
                j:real;
            begin
                for i:=1 to 10.0 do a:=1;
            end
        """

        expect = "Type Mismatch In Statement: For(Id(i)IntLiteral(1),FloatLiteral(10.0),True,[AssignStmt(Id(a),IntLiteral(1))])"
        self.assertTrue(TestChecker.test(code,expect,412))

    def test_typemissmatch_5(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure main();
                
            begin
                while (a) do a:=1;
            end
        """
        expect = "Type Mismatch In Statement: While(Id(a),[AssignStmt(Id(a),IntLiteral(1))])"
        self.assertTrue(TestChecker.test(code,expect,413))

    def test_typemissmatch_6(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure main();
                
            begin
                while d do while b do a:=1;
            end
        """
        expect = "Type Mismatch In Statement: While(Id(b),[AssignStmt(Id(a),IntLiteral(1))])"
        self.assertTrue(TestChecker.test(code,expect,414))
    
    def test_typemissmatch_7(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure main();
                
            begin
                a:=1;
                c:=1.0;
                d:=true;
                b:="asdf";
            end
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),StringLiteral(asdf))"
        self.assertTrue(TestChecker.test(code,expect,415))

    def test_typemissmatch_8(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure main();
                
            begin
                c := 10;
                e := 1;
            end
        """
        expect = "Type Mismatch In Statement: AssignStmt(Id(e),IntLiteral(1))"
        self.assertTrue(TestChecker.test(code,expect,416))

    def test_typemissmatch_9(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            begin
                return 1;
            end
            procedure main();
                
            begin
                foo();
            end
        """
        expect = "Type Mismatch In Statement: Return(Some(IntLiteral(1)))"
        self.assertTrue(TestChecker.test(code,expect,417))

    def test_typemissmatch_10(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            begin
                return;
            end
            procedure main();
                
            begin
                a := foo();
            end
        """
        expect = "Type Mismatch In Statement: Return(None)"
        self.assertTrue(TestChecker.test(code,expect,418))

    def test_typemissmatch_11(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function goo(): real;
            begin
                return 1;
            end
            function foo(): integer;
            begin
                return 1.0;
            end
            procedure main();
                
            begin
                a := foo();
                c := goo();
            end
        """
        expect = "Type Mismatch In Statement: Return(Some(FloatLiteral(1.0)))"
        self.assertTrue(TestChecker.test(code,expect,419))

    def test_typemissmatch_12(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function goo(): real;
            begin
                return true;
            end
            function foo(): integer;
            begin
                return 1.0;
            end
            procedure main();
                
            begin
                a := foo();
                c := goo();
            end
        """
        expect = "Type Mismatch In Statement: Return(Some(BooleanLiteral(True)))"
        self.assertTrue(TestChecker.test(code,expect,420))

    def test_typemissmatch_13(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function goo():  array[1 .. 3] of integer;
            begin
                return e;
            end
            function foo(): array[2 .. 3] of integer;
            begin
                return e;
            end
            procedure main();
                
            begin
                e := foo();
                e := goo();
            end
        """
        expect = "Type Mismatch In Statement: Return(Some(Id(e)))"
        self.assertTrue(TestChecker.test(code,expect,421))

    def test_typemissmatch_14(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function goo():  array[1 .. 3] of integer;
            begin
                return e;
            end
            function foo(): array[1 .. 3] of real;
            begin
                return e;
            end
            procedure main();
                
            begin
                e := foo();
                e := goo();
            end
        """
        expect = "Type Mismatch In Statement: Return(Some(Id(e)))"
        self.assertTrue(TestChecker.test(code,expect,422))

    def test_typemissmatch_15(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function goo():  array[1 .. 3] of integer;
            begin
                return e;
            end
            function foo(): array[1 .. 4] of integer;
            begin
                return e;
            end
            procedure main();
                
            begin
                e := foo();
                e := goo();
            end
        """
        expect = "Type Mismatch In Statement: Return(Some(Id(e)))"
        self.assertTrue(TestChecker.test(code,expect,423))


    def test_typemissmatch_16(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo(_a: integer; _b:string; _c:real; _d:boolean; _e:array[1 .. 3] of integer);
            begin

            end
            procedure main();
                
            begin
                foo();
            end
        """
        expect = "Type Mismatch In Statement: CallStmt(Id(foo),[])"
        self.assertTrue(TestChecker.test(code,expect,424))

    def test_typemissmatch_17(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo(_a: integer; _b:string; _c:real; _d:boolean; _e:array[1 .. 3] of integer);
            begin

            end
            procedure main();
                
            begin
                foo(1,"abd",1.0,true,e);
                foo(1.0,"abd",1.0,true,e);
                foo(1.0,"abd",1.0,true);
            end
        """
        expect = "Type Mismatch In Statement: CallStmt(Id(foo),[FloatLiteral(1.0),StringLiteral(abd),FloatLiteral(1.0),BooleanLiteral(True),Id(e)])"
        self.assertTrue(TestChecker.test(code,expect,425))


    def test_typemissmatch_18(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo(_e:array[2 .. 3] of integer);
            begin

            end
            procedure main();
                
            begin
                foo(e);
            end
        """
        expect = "Type Mismatch In Statement: CallStmt(Id(foo),[Id(e)])"
        self.assertTrue(TestChecker.test(code,expect,426))

    def test_typemissmatch_19(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo(_e:array[1 .. 4] of integer);
            begin

            end
            procedure main();
                
            begin
                foo(e);
            end
        """
        expect = "Type Mismatch In Statement: CallStmt(Id(foo),[Id(e)])"
        self.assertTrue(TestChecker.test(code,expect,427))

    def test_typemissmatch_20(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo(_e:array[1 .. 3] of real);
            begin

            end
            procedure main();
                
            begin
                foo(e);
            end
        """
        expect = "Type Mismatch In Statement: CallStmt(Id(foo),[Id(e)])"
        self.assertTrue(TestChecker.test(code,expect,428))


    def test_typemissmatch_exp_1(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): array[1 .. 3] of integer;
            begin
                return e;
            end
            procedure main();                
            begin
                a:=foo()[1];
                a:=foo()[1.2];
            end
        """
        expect = "Type Mismatch In Expression: ArrayCell(CallExpr(Id(foo),[]),FloatLiteral(1.2))"
        self.assertTrue(TestChecker.test(code,expect,429))

    def test_typemissmatch_exp_2(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): array[1 .. 3] of integer;
            begin
                return e;
            end
            procedure main();                
            begin
                a:=foo()[1];
                a:=foo()[1.2];
            end
        """
        expect =  "Type Mismatch In Expression: ArrayCell(CallExpr(Id(foo),[]),FloatLiteral(1.2))"
        self.assertTrue(TestChecker.test(code,expect,430))

    def test_typemissmatch_exp_3(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): array[1 .. 3] of integer;
            begin
                return e;
            end
            procedure main();                
            begin
                a:=e[1];
                a:=b[1];
            end
        """
        expect =  "Type Mismatch In Expression: ArrayCell(Id(b),IntLiteral(1))"
        self.assertTrue(TestChecker.test(code,expect,431))


    def test_typemissmatch_exp_4(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): array[1 .. 3] of integer;
            begin
                return e;
            end
            procedure main();                
            begin
                a:= -a;
                c:= -c;
                c:= -a;
                d:= not d;
                b:= -b;
            end
        """
        expect =  "Type Mismatch In Expression: UnaryOp(-,Id(b))"
        self.assertTrue(TestChecker.test(code,expect,432))


    def test_typemissmatch_exp_5(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): array[1 .. 3] of integer;
            begin
                return e;
            end
            procedure main();                
            begin
                a:= Not a;
            end
        """
        expect =  "Type Mismatch In Expression: UnaryOp(Not,Id(a))"
        self.assertTrue(TestChecker.test(code,expect,433))


    def test_typemissmatch_exp_6(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            begin
                return 1;
            end
            function goo(): real;
            begin
                return 1.0;
            end
            procedure main();                
            begin
                a:= foo();
                c:= goo();
                c:= goo();
                b:=foo();
            end
        """
        expect =  "Type Mismatch In Statement: AssignStmt(Id(b),CallExpr(Id(foo),[]))"
        self.assertTrue(TestChecker.test(code,expect,434))

    def test_funtion_not_return(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            begin
                a:= 1;
            end

            procedure main();                
            begin
                a:= foo();

            end
        """
        expect =  "Function fooNot Return "
        self.assertTrue(TestChecker.test(code,expect,435))

    def test_break_continue_not_in_loop_1(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            begin
                break;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Break Not In Loop"
        self.assertTrue(TestChecker.test(code,expect,436))

    def test_break_continue_not_in_loop_2(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            begin
                continue;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Continue Not In Loop"
        self.assertTrue(TestChecker.test(code,expect,437))

    def test_break_continue_not_in_loop_3(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            var i:integer;
            begin
                for i:=1 to 10 do
                    begin
                        a:=1;
                        break;
                    end
                while d do
                    begin
                        a:=1;
                        break;
                    end
                break;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Break Not In Loop"
        self.assertTrue(TestChecker.test(code,expect,438))


    def test_unreachable_stmt_1(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            var i:integer;
            begin
                a:=1;
                return;
                a:=2;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Unreachable statement: AssignStmt(Id(a),IntLiteral(2))"
        self.assertTrue(TestChecker.test(code,expect,439))


    def test_unreachable_stmt_2(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            var i:integer;
            begin
                if d then return;
                else return;
                a:=1;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Unreachable statement: AssignStmt(Id(a),IntLiteral(1))"
        self.assertTrue(TestChecker.test(code,expect,440))


    def test_unreachable_stmt_3(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            var i:integer;
            begin
                for i:=1 to 10 do
                    begin
                        return;
                    end
                while d do
                    begin
                        return;
                    end
                a:=2;
                return;
                a:=1;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Unreachable statement: AssignStmt(Id(a),IntLiteral(1))"
        self.assertTrue(TestChecker.test(code,expect,441))


    def test_unreachable_stmt_4(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            var i:integer;
            begin
                with x:integer; do
                    begin
                        return;
                    end
                a:=2;
                return;
                a:=1;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Unreachable statement: AssignStmt(Id(a),IntLiteral(2))"
        self.assertTrue(TestChecker.test(code,expect,442))


    def test_unreachable_stmt_5(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            var i:integer;
            begin
                if d then return;
                if d then return;
                if d then a:=1; else return;
                if d then return; else return;
                a:=2;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Unreachable statement: AssignStmt(Id(a),IntLiteral(2))"
        self.assertTrue(TestChecker.test(code,expect,443))


    def test_unreachable_stmt_6(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            var i:integer;
            begin
                if d then
                begin
                    a:=1;
                    return;
                    a:=2;
                end
                a:=3;
                return;
                a:=4;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Unreachable statement: AssignStmt(Id(a),IntLiteral(2))"
        self.assertTrue(TestChecker.test(code,expect,444))


    def test_unreachable_stmt_7(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            var i:integer;
            begin
                if d then
                    return;
                if d then
                    a:=1;
                else
                    return;
                a:=2;
                return;
                a:=3;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Unreachable statement: AssignStmt(Id(a),IntLiteral(3))"
        self.assertTrue(TestChecker.test(code,expect,445))


    def test_unreachable_stmt_8(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            var i:integer;
            begin
                return;
                if d then return; else return;
                return;
                a:=1;
                return;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Unreachable statement: If(Id(d),[Return(None)],[Return(None)])"
        self.assertTrue(TestChecker.test(code,expect,446))


    def test_unreachable_stmt_9(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            procedure foo();
            var i:integer;
            begin
                return;
                return;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Unreachable statement: Return(None)"
        self.assertTrue(TestChecker.test(code,expect,447))



    def test_unreachable_stmt_10(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            var i:integer;
            begin
                if d then return 1;
                a:=1;
                if d then return 1;
                else return 2;
                return 3;
                return 4;
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Unreachable statement: Return(Some(IntLiteral(3)))"
        self.assertTrue(TestChecker.test(code,expect,448))

 
    def test_unreachable_func_1(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            var i:integer;
            begin
                return 1;
            end
            procedure goo();
            begin
            end
            procedure main();                
            begin
                foo();
            end
        """
        expect =  "Undeclared Procedure: foo"
        self.assertTrue(TestChecker.test(code,expect,449))

    def test_unreachable_func_2(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            var i:integer;
            begin
                return 1;
            end
            procedure goo();
            begin
            end
            procedure main();                
            begin
                goo();
            end
        """
        expect =  "Unreachable Function: foo"
        self.assertTrue(TestChecker.test(code,expect,450))

    def test_unreachable_func(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            var i:integer;
            begin
                return 1;
            end
            procedure goo();
            begin
            end
            procedure main();                
            begin
                a:=foo();
            end
        """
        expect =  "Unreachable Procedure: goo"
        self.assertTrue(TestChecker.test(code,expect,451))


    def test_all_1(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            var i:integer;
            begin
                return 1;
            end
            procedure goo();
            begin
            end
            var MaIn: integer;
            procedure main();                
            begin
                a:=foo();
                goo();
            end
        """
        expect =  "Redeclared Procedure: main"
        self.assertTrue(TestChecker.test(code,expect,452))

    def test_all_2(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            var i:integer;
            begin
                return 1;
            end
            procedure goo();
            begin
                return 2;
            end
            procedure main();                
            begin
                a:=foo();
                goo();
            end
        """
        expect =  "Type Mismatch In Statement: Return(Some(IntLiteral(2)))"
        self.assertTrue(TestChecker.test(code,expect,453))

    def test_all_3(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            var i:integer;
            begin
                if d then
                    if d then
                        return 1;
                else
                    return 1;
            end
            procedure goo();
            begin
            end
            procedure main();                
            begin
                a:=foo();
                goo();
            end
        """
        expect =  "Function fooNot Return "
        self.assertTrue(TestChecker.test(code,expect,454))

    def test_all_4(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            var i:integer;
            begin
                if d then
                begin
                    while d do
                        return 2;
                    for i:=1 to 2 do
                        return 3;
                end
                else
                    return 1;
            end
            procedure goo();
            begin
            end
            procedure main();                
            begin
                a:=foo();
                goo();
            end
        """
        expect =  "Function fooNot Return "
        self.assertTrue(TestChecker.test(code,expect,455))

    def test_all_5(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            var i:integer;
            begin
                if d then
                begin
                    while d do
                        return 2.0;
                    for i:=1 to 2 do
                        return 3;
                end
                else
                    return 1;
            end
            procedure goo();
            begin
            end
            procedure main();                
            begin
                a:=foo();
                goo();
            end
        """
        expect =  "Type Mismatch In Statement: Return(Some(FloatLiteral(2.0)))"
        self.assertTrue(TestChecker.test(code,expect,456))

    def test_all_6(self):
        code = """
            var a: integer;
            var b: string;
            var c: real;
            var d: boolean;
            var e: array[1 .. 3] of integer;
            function foo(): integer;
            var i:integer;
            begin
                if d then
                begin
                    while d do
                        return 2;
                    for i:=1 to 2 do
                        return "hello";
                end
                else
                    return 1;
            end
            procedure goo();
            begin
            end
            procedure main();                
            begin
                a:=foo();
                goo();
            end
        """
        expect =  "Type Mismatch In Statement: Return(Some(StringLiteral(hello)))"
        self.assertTrue(TestChecker.test(code,expect,457))

