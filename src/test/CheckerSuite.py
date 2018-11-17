import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    
    def test_super_unreachable_stmt_1(self):
        input = '''
            function foo():integer;
            var abc, def: integer;
            begin
                if true then 
                    begin
                    while true do
                    begin
                        if true 
                        then
                            continue;
                        else
                            break;  
                    end
                    return 1;
                    end
                    
                else return 2;
                a:=1;
            end

            procedure main();
            var x:real;
            begin
                x := foo();
            end
        '''
        expect = "Unreachable statement: AssignStmt(Id(a),IntLiteral(1))"
        self.assertTrue(TestChecker.test(input,expect,492))

    def test_super_unreachable_stmt_2(self):
        input = '''
            function foo():integer;
            var abc, def: integer;
            begin
                if true then 
                    if true then
                        if true then
                            if true then
                                return 1;
                            else return 1;
                        else return 1;
                    else return 1;
                else return 1;
                a:=1;
            end

            procedure main();
            var x:real;
            begin
                x := foo();
            end
        '''
        expect = "Unreachable statement: AssignStmt(Id(a),IntLiteral(1))"
        self.assertTrue(TestChecker.test(input,expect,493))

    def test_super_unreachable_stmt_3(self):
        input = '''
            function foo():integer;
            var abc, def: integer;
            begin
                if true then 
                    begin
                    while true do
                    begin
                        if true then
                            begin
                            continue;
                            a:=2;
                            end
                        else
                            break;
                    end
                    return 1;
                    end
                else return 2;
            end

            procedure main();
            var x:real;
            begin
                x := foo();
            end
        '''
        expect = "Unreachable statement: AssignStmt(Id(a),IntLiteral(2))"
        self.assertTrue(TestChecker.test(input,expect,494))
    
    def test_super_unreachable_stmt_4(self):
        input = '''
            function foo():integer;
            var abc, def: integer;
            begin
                if true then 
                    begin
                        with a:integer; do
                            begin
                                return def;
                            end
                    end
                else 
                    begin
                        if true then
                            begin
                                abc:=abc+1;
                                return abc;
                            end
                        else
                            return 3;
                    end
                a:=1;
            end

            procedure main();
            var x:real;
            begin
                x := foo();
            end
        '''
        expect = "Unreachable statement: AssignStmt(Id(a),IntLiteral(1))"
        self.assertTrue(TestChecker.test(input,expect,495))

    def test_super_unreachable_stmt_5(self):
        input = '''
            function foo():integer;
            var abc, i: integer;
                flag: boolean;
            begin
                flag := true;
                while flag do
                    begin
                        for i := 1 to 10 do
                            begin
                                while flag do
                                    begin
                                        if true then break;
                                        else
                                            begin
                                                continue;
                                                a:=a+1;
                                            end
                                    end
                            end
                    end
                return 1;
            end

            procedure main();
            var x:real;
            begin
                x := foo();
            end
        '''
        expect = "Unreachable statement: AssignStmt(Id(a),BinaryOp(+,Id(a),IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input,expect,496))

    def test_super_unreachable_stmt_6(self):
        input = '''
            function foo():integer;
            var abc, i: integer;
                flag: boolean;
            begin
                flag := true;
                if true then
                begin
                    while flag do
                        begin
                            for i := 1 to 10 do
                                begin
                                    while flag do
                                        begin
                                            if true then break;
                                            else
                                                begin
                                                    continue;
                                                end
                                        end
                                end
                        end
                    return 5;
                end
                else
                    return 1;
                a:=a+1;
            end

            procedure main();
            var x:real;
            begin
                x := foo();
            end
        '''
        expect = "Unreachable statement: AssignStmt(Id(a),BinaryOp(+,Id(a),IntLiteral(1)))"
        self.assertTrue(TestChecker.test(input,expect,497))

    def test_super_unreachable_stmt_7(self):
        input = '''
            function foo():integer;
            var abc, def: integer;
            begin
                with a:integer; do
                    begin
                        while true do
                        begin
                            if true then return 1;
                            else return 2;
                        end
                    end
                if true then a:=a+1;
                        else a:=a-1;
                begin
                    return 3;
                end
                return "la hoang duc dep trai vo doi";
            end

            procedure main();
            var x:real;
            begin
                x := foo();
            end
        '''
        expect = "Unreachable statement: Return(Some(StringLiteral(la hoang duc dep trai vo doi)))"
        self.assertTrue(TestChecker.test(input,expect,498))

    def test_super_unreachable_stmt_8(self):
        input = '''
            function foo():string;
            var b, def: integer;
            begin
                with a:string; do
                    begin
                        b:=b+2;
                    end
                while true do
                    begin
                        if true then return "swhite-chan is super perfect";
                        else return "Swhite sister is so cute <3 ~~~~~!!!!!";
                    end
                if true then return "la duc is so handsome";
                        else
                            begin
                                with a:string; do
                                begin
                                    return "no nut november !";
                                end
                            end
                return "???????";
            end

            procedure main();
            var x:real;
            begin
                x := foo();
            end
        '''
        expect = "Unreachable statement: Return(Some(StringLiteral(???????)))"
        self.assertTrue(TestChecker.test(input,expect,499))