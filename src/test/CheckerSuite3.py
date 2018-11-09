import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    def test_redeclared_builtin_procedure(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                
                end
                procedure putIntLn();
                beGin
                
                eND
                """
        expect = "Redeclared Procedure: putIntLn"
        self.assertTrue(TestChecker.test(input,expect,400))
    
    def test_redeclared_builtin_function(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                end
                function getInt():Integer;
                beGin
                return 3;
                eND
                """
        expect = "Redeclared Function: getInt"
        self.assertTrue(TestChecker.test(input,expect,401))

    def test_redeclared_procedure(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                end
                procedure foo();
                beGin
                
                eND
                procedure foo();
                beGin
                
                eND
                """
        expect = "Redeclared Procedure: foo"
        self.assertTrue(TestChecker.test(input,expect,402))

    def test_redeclared_param_vs_local(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                end
                procedure foo(a: integer);
                var a:integer;
                beGin
                
                eND
                """
        expect = "Redeclared Variable: a"
        self.assertTrue(TestChecker.test(input,expect,403))

    def test_redeclared_param(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                end
                var name: real;
                procedure foo2(name: integer);
                beGin
                eND
                procedure foo(a: integer;a: integer);
                begin
                end
                """
        expect = "Redeclared Parameter: a"
        self.assertTrue(TestChecker.test(input,expect,404))

    def test_type_not_coerc_int_float(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                end
                procedure foo();
                beGin
                putInt(1+2.1);
                eND
                
                """
        expect = "Type Mismatch In Statement: CallStmt(Id(putInt),[BinaryOp(+,IntLiteral(1),FloatLiteral(2.1))])"
        self.assertTrue(TestChecker.test(input,expect,405))
    
    def test_type_coerc_int_float(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                end
                procedure foo();
                beGin
                putFloat(1+2);
                putInt(1.3+2);
                eND
                
                """
        expect = "Type Mismatch In Statement: CallStmt(Id(putInt),[BinaryOp(+,FloatLiteral(1.3),IntLiteral(2))])"
        self.assertTrue(TestChecker.test(input,expect,406))

    def test_and_or_boolean(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                end
                procedure foo();
                beGin
                    putBoolLn(trUe and false);
                    putBool(1 or 2.1);
                eND
                
                """
        expect = "Type Mismatch In Expression: BinaryOp(or,IntLiteral(1),FloatLiteral(2.1))"
        self.assertTrue(TestChecker.test(input,expect,407))

    def test_andthen_orelse_boolean(self):
        """Simple program: int main() {} """
        
        input = r"""
                procedure main();
                begin
                end
                procedure foo();
                beGin
                    putBoolLn(true and then false);
                    putBool(1 or else 2.1);
                eND
                
                """
        expect = "Type Mismatch In Expression: BinaryOp(orelse,IntLiteral(1),FloatLiteral(2.1))"
        self.assertTrue(TestChecker.test(input,expect,408))

    def test_Unary_Type_sub(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                end
                procedure foo();
                beGin
                    putIntLn(-1);
                    putInt(- "string in unaryop");
                eND
                
                """
        expect = "Type Mismatch In Expression: UnaryOp(-,StringLiteral(string in unaryop))"
        self.assertTrue(TestChecker.test(input,expect,409))

    def test_Unary_Type_Not(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                end
                procedure foo();
                beGin
                    putBoolLn(not true);
                    putBool(1 or else 2.1);
                eND
                
                """
        expect = "Type Mismatch In Expression: BinaryOp(orelse,IntLiteral(1),FloatLiteral(2.1))"
        self.assertTrue(TestChecker.test(input,expect,410))

    def test_Unary_Type_Not_more(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                end
                procedure foo();
                beGin
                    putBoolLn(not (1>2));
                    putBool(not (10000 + 0));
                eND
                
                """
        expect = "Type Mismatch In Expression: UnaryOp(not,BinaryOp(+,IntLiteral(10000),IntLiteral(0)))"
        self.assertTrue(TestChecker.test(input,expect,411))
    def test_Undeclared_id(self):
        """Simple program: int main() {} """
        input = r"""
                procedure main();
                begin
                end
                var a: integer;
                procedure foo();
                beGin
                    putBoolLn(a>2);
                    putBool(b>2);
                eND
                
                """
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input,expect,412))

    def test_Declared_id_in_local(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                
                procedure foo();
                var a: integer;
                beGin
                    putBoolLn(a>2);
                    putBool(b>2);
                eND
                
                """
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input,expect,413))
    
    def test_Declared_id_in_param(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                
                procedure foo(a: integer);
                
                beGin
                    putBoolLn(a>2);
                    putBool(b>2);
                eND
                
                """
        expect = "Undeclared Identifier: b"
        self.assertTrue(TestChecker.test(input,expect,414))
    
    def test_Declared_inside_hidden_outside(self):
        """More complex program"""
        
        input = r"""
                procedure main();
                begin
                end
                var a: real;
                procedure foo(a:string);
                beGin
                    putFloatLn(a);
                eND
                
                """
        expect = "Type Mismatch In Statement: CallStmt(Id(putFloatLn),[Id(a)])"
        self.assertTrue(TestChecker.test(input,expect,415))
    def test_undeclared_procedure(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                procedure swap() ;
                var a: array[0 .. 1] of integer;
                 {i,j,temp: integer;}
                beGin
                    print(a);
                eND
                """
        expect = "Undeclared Procedure: print"
        self.assertTrue(TestChecker.test(input,expect,416))

    def test_array_type_mismatch_with_int(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                procedure swap() ;
                var a: array[0 .. 1] of integer;
                 {i,j,temp: integer;}
                beGin
                    putIntLn(a[0]);
                    putStringLn(a[0]);
                eND
                """
        expect = "Type Mismatch In Statement: CallStmt(Id(putStringLn),[ArrayCell(Id(a),IntLiteral(0))])"
        self.assertTrue(TestChecker.test(input,expect,417))

    def test_array_type_mismatch_with_float(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                procedure swap() ;
                var a: array[0 .. 1] of real;
                 {i,j,temp: integer;}
                beGin
                    putFloatLn(a[0]);
                    putStringLn(a[0]);
                eND
                """
        expect = "Type Mismatch In Statement: CallStmt(Id(putStringLn),[ArrayCell(Id(a),IntLiteral(0))])"
        self.assertTrue(TestChecker.test(input,expect,418))

    def test_assign_type_mismatch_with_arraytype(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                procedure swap() ;
                var a: array[0 .. 1] of real;
                 i: integer;
                beGin
                    i := 5;
                    a := i;
                eND
                """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),Id(i))"
        self.assertTrue(TestChecker.test(input,expect,419))
    
    def test_assign_type_mismatch_with_stringtype(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                procedure swap() ;
                var a: string;
                 i: integer;
                beGin
                    i := 5;
                    a := i;
                eND
                """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),Id(i))"
        self.assertTrue(TestChecker.test(input,expect,420))
    def test_complex_assign_type_mismatch_with_stringtype(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                procedure swap() ;
                var a: string;
                 i,k: integer;
                beGin
                    i := k := 5;
                    a := i;
                eND
                """
        expect = "Type Mismatch In Statement: AssignStmt(Id(a),Id(i))"
        self.assertTrue(TestChecker.test(input,expect,421))
    def test_complex_assign_type_mismatch_with_intlit(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                procedure swap() ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                beGin
                    i := k := m[2];
                    i := a;
                    
                eND
                """
        expect = "Type Mismatch In Statement: AssignStmt(Id(i),Id(a))"
        self.assertTrue(TestChecker.test(input,expect,422))
    def test_function_not_return(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    i := k := m[2];
                    putInt(3);
                    
                end
                """
        expect = "Function swapNot Return "
        self.assertTrue(TestChecker.test(input,expect,423))
    def test_procedure_return_expr(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                procedure swap() ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    i := k := m[2];
                    putInt(3);
                    return 3;
                end
                """
        expect = "Type Mismatch In Statement: Return(Some(IntLiteral(3)))"
        self.assertTrue(TestChecker.test(input,expect,424))
    def test_procedure_return_without_expr(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                procedure swap() ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    i := k := m[2];
                    putInt(3);
                    return;
                end
                procedure swap2() ;
                begin
                    return 3;
                end
                """
        expect = "Type Mismatch In Statement: Return(Some(IntLiteral(3)))"
        self.assertTrue(TestChecker.test(input,expect,425))
    def test_function_return_mismatch_expr(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap(): integer;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    i := k := m[2];
                    putInt(3);
                    return a;
                end
                """
        expect = "Type Mismatch In Statement: Return(Some(Id(a)))"
        self.assertTrue(TestChecker.test(input,expect,426))
    def test_function_return_int_float_coerc_expr(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap(): real;
                var a: integer;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    i := k := m[2];
                    putInt(3);
                    return a;
                end
                function swap2(): integer;
                var b: real;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    i := k := m[2];
                    putInt(3);
                    return b;
                end
                """
        expect = "Type Mismatch In Statement: Return(Some(Id(b)))"
        self.assertTrue(TestChecker.test(input,expect,427))
    def test_unreachable_stmt(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    i := k := m[2];
                    return 3;
                    putInt(3);
                    
                end
                """
        expect = "Unreachable statement: CallStmt(Id(putInt),[IntLiteral(3)])"
        self.assertTrue(TestChecker.test(input,expect,428))
    def test_if_stmt(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    if (i>1) then k:=1;
                    else if ("true") then i:=0;
                    return 1;
                end
                """
        expect = "Type Mismatch In Statement: If(StringLiteral(true),[AssignStmt(Id(i),IntLiteral(0))],[])"
        self.assertTrue(TestChecker.test(input,expect,429))
    def test_if_stmt_with_return(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    if (i>1) then 
                        begin 
                            k:=1; 
                            retUrn 1.2;
                        end
                    else if (true) then i:=0;
                    return 1;
                end
                """
        expect = "Type Mismatch In Statement: Return(Some(FloatLiteral(1.2)))"
        self.assertTrue(TestChecker.test(input,expect,430))
    def test_if_stmt_with_not_return(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    if (i>1) then 
                        begin 
                            k:=1; 
                            retUrn 3;
                        end
                    else if (true) then i:=0;
                    {return 1;}
                end
                """
        expect = "Function swapNot Return "
        self.assertTrue(TestChecker.test(input,expect,431))
    def test_while_stmt_with_not_return(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    while (true) do return 3;
                    {return 1;}
                end
                """
        expect = "Function swapNot Return "
        self.assertTrue(TestChecker.test(input,expect,432))
    def test_while_stmt_with_return(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    while (5) do i:=1;
                    return 1;
                end
                """
        expect = "Type Mismatch In Statement: While(IntLiteral(5),[AssignStmt(Id(i),IntLiteral(1))])"
        self.assertTrue(TestChecker.test(input,expect,433))
    def test_while_stmt_with_continue(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    while (true) do
                        begin 
                            i:=2;
                            continue;
                        end
                    while (2>1) do
                        begin
                            continue;
                            i:=1;
                        end
                    return 1;
                end
                """
        expect = "Unreachable statement: AssignStmt(Id(i),IntLiteral(1))"
        self.assertTrue(TestChecker.test(input,expect,434))  
    def test_continue_not_in_loop(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    while (true) do
                        begin 
                            i:=2;
                            continue;
                        end
                    while (2>1) do
                        begin
                            i:=1;
                        end
                    continue;
                    return 1;
                end
                """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,435))
    def test_break_not_in_loop(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    while (true) do
                        begin 
                            i:=2;
                            continue;
                        end
                    while (2>1) do
                        begin
                            i:=1;
                        end
                    break;
                    return 1;
                end
                """
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,436))
    def test_inner_while(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    while (true) do
                        begin 
                            i:=2;
                            while (2>1) do
                                begin
                                    i:=1;
                                    break;
                                end
                            continue;
                        end
                    
                    return ;
                end
                """
        expect = "Type Mismatch In Statement: Return(None)"
        self.assertTrue(TestChecker.test(input,expect,437))  
    def test_return_in_if(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    if i > 10 then
                        begin
                            k := i;
                            return k;
                        end
                    else
                        begin
                            k := i + 1;
                            return 1.4;
                        end
                    
                end
                """
        expect = "Type Mismatch In Statement: Return(Some(FloatLiteral(1.4)))"
        self.assertTrue(TestChecker.test(input,expect,438))
    def test_return_in_if_then(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    if i > 10 then
                        begin
                            k := i;
                            return k;
                        end
                    else
                        begin
                            k := i + 1;
                            {return 1.4;}
                        end
                    
                end
                """
        expect = "Function swapNot Return "
        self.assertTrue(TestChecker.test(input,expect,439))
    def test_with_stmt(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    with  b : integer ; a: real; c : array [1 .. 2] of real ; do 
                    begin
                        a := c[1] + b ;
                        b := a;
                    end
                    
                end
                """
        expect = "Type Mismatch In Statement: AssignStmt(Id(b),Id(a))"
        self.assertTrue(TestChecker.test(input,expect,440))
    def test_with_stmt_with_return(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    with  b : integer ; a: real; c : array [1 .. 2] of real ; do 
                        begin
                            a := c[1] + b ;
                            {b := a;}
                            return b;
                        end
                    i := m[3];
                end
                """
        expect = "Unreachable statement: AssignStmt(Id(i),ArrayCell(Id(m),IntLiteral(3)))"
        self.assertTrue(TestChecker.test(input,expect,441))
    def test_for_stmt_with_return(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    for i:=1 to 10 do
                        begin
                            i := k;
                        end
                    for a:=1 to 10 do 
                        begin
                        end
                    return 1;
                end
                """
        expect = "Type Mismatch In Statement: For(Id(a)IntLiteral(1),IntLiteral(10),True,[])"
        self.assertTrue(TestChecker.test(input,expect,442))
    def test_for_stmt_with_not_return(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    for i:=1 to 10 do
                        begin
                            i := k;
                            return 1;
                        end
                    for k:=1 to 10 do 
                        begin
                            return 1;
                        end
                    
                end
                """
        expect = "Function swapNot Return "
        self.assertTrue(TestChecker.test(input,expect,443))
    def test_for_stmt_continue(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    for i:=1 to 10 do
                        begin
                            i := k;
                            return 1;
                        end
                    for k:=1 to 10 do 
                        begin
                            continue;
                        end
                    
                end
                """
        expect = "Function swapNot Return "
        self.assertTrue(TestChecker.test(input,expect,444))
    def test_for_stmt_continue_break(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap():integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 5] of integer;
                begin
                    for i:=1 to 10 do
                        begin
                            i := k;
                            for k:=1 to 10 do 
                                begin
                                    continue;
                                end
                            return 1;
                        end
                    
                    {return 1;}
                    
                end
                """
        expect = "Function swapNot Return "
        self.assertTrue(TestChecker.test(input,expect,445))
    
    def test_return_arraytype_type(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap(): array[2 .. 3] of integer ;
                var a: string;
                 i,k: integer;
                 m: array[2 .. 3] of real;
                begin
                    return m;
                end
                """
        expect = "Type Mismatch In Statement: Return(Some(Id(m)))"
        self.assertTrue(TestChecker.test(input,expect,446))
    def test_return_arraytype_lower_upper(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function swap(): array[2 .. 3] of integer ;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 3] of integer;
                begin
                    return m;
                end
                """
        expect = "Type Mismatch In Statement: Return(Some(Id(m)))"
        self.assertTrue(TestChecker.test(input,expect,447))
    def test_arraytype_as_parameter_wrong_returntype(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                procedure foo1(b: array[1 .. 2] of integer);
                var a: string;
                 i,k: integer;
                 m: array[1 .. 3] of integer;
                begin
                end
                procedure foo2();
                var n: array[1 .. 2] of real;
                begin
                    foo1(n);
                end
                """
        expect = "Type Mismatch In Statement: CallStmt(Id(foo1),[Id(n)])"
        self.assertTrue(TestChecker.test(input,expect,448))
    def test_arraytype_as_parameter_wrong_upper_procedure(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                procedure foo1(b: array[1 .. 2] of integer);
                var a: string;
                 i,k: integer;
                 m: array[1 .. 3] of integer;
                begin
                end
                procedure foo2();
                var n: array[1 .. 6] of integer;
                begin
                    foo1(n);
                end
                """
        expect = "Type Mismatch In Statement: CallStmt(Id(foo1),[Id(n)])"
        self.assertTrue(TestChecker.test(input,expect,449))
    def test_arraytype_as_parameter_wrong_upper_function(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                end
                function foo1(b: array[1 .. 2] of integer): integer;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 3] of integer;
                begin
                    return 1;
                end
                procedure foo2();
                var n: array[1 .. 2] of real;
                i: integer;
                begin
                    i:= foo1(n);
                end
                """
        expect = "Type Mismatch In Expression: CallExpr(Id(foo1),[Id(n)])"
        self.assertTrue(TestChecker.test(input,expect,450))
    def test_function_main_entrypoint(self):
        """More complex program"""
        input = r"""
                function main(): integer;
                begin
                    return 1;
                end
                function foo1(b: array[1 .. 2] of integer): integer;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 3] of integer;
                begin
                    return 1;
                end
                procedure foo2();
                var n: array[1 .. 2] of integer;
                i: integer;
                begin
                    i:= foo1(n);
                end
                """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,451))
    def test_no_entrypoint(self):
        """More complex program"""
        input = r"""
                function foo1(b: array[1 .. 2] of integer): integer;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 3] of integer;
                begin
                    return 1;
                end
                procedure foo2();
                var n: array[1 .. 2] of integer;
                i: integer;
                begin
                    i:= foo1(n);
                end
                """
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,452))
    def test_unreach_call_stmt(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                    {foo2();}
                end
                function foo1(b: array[1 .. 2] of integer): integer;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 3] of integer;
                begin
                    return 1;
                end
                procedure foo2();
                var n: array[1 .. 2] of integer;
                i: integer;
                begin
                    i:= foo1(n);
                end
                """
        expect = "Unreachable Procedure: foo2"
        self.assertTrue(TestChecker.test(input,expect,453))
    def test_unreach_call_expr(self):
        """More complex program"""
        input = r"""
                procedure main();
                begin
                    {foo2();}
                end
                function foo1(b: array[1 .. 2] of integer): integer;
                var a: string;
                 i,k: integer;
                 m: array[1 .. 3] of integer;
                begin
                    return 1;
                end
                function foo2(): integer;
                var n: array[1 .. 2] of integer;
                i: integer;
                begin
                    i:= foo1(n);
                    return 0;
                end
                """
        expect = "Unreachable Function: foo2"
        self.assertTrue(TestChecker.test(input,expect,454))
    def test_undeclared_identifier2(self):
        """test_undeclared_identifier2"""
        input = r"""
        var x:integer;
            
        function foo():real;
        begin
            return x;
        end

        procedure main();
        var x:real;
        begin
            x:=foo();
            x:= foo + 1; 
        end
        """
        expect = "Undeclared Identifier: foo"
        self.assertTrue(TestChecker.test(input,expect,455))
    def test_continue_not_in_loop2(self):
        """test_continue_not_in_loop2"""
        input = r"""
        procedure foo();
        var a:integer;
        begin
            while trUE do
                if (1=4) or (a>=0.0000000010001) then
                    Continue;
            
            for a:=a dOWNtO 1 do
                if true or FalSe then
                    Continue;
        end

        procedure MaIn();
        begin
            foo();
            if (0.6/5>7) or not false then
                Continue;  // error
        end
        """
        expect = "Continue Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,456))
    def test_unreachable_stmt_complex(self):
        """test_unreachable_stmt7"""
        input = r"""
        procedure MaIn();
        begin
            foo();
            foo7();
        end
                
        procedure foo();
        var a:real;
            i:integer;
        begin
            while true do  //# no return
                return;

            for i:=0 to 10 do
                begin
                    i:=-(-(i-1));
                    return;
                end
        end

        procedure foo7();
        var i:integer;
        begin
            while false do
                return ;
            return ;  //# return here

            for I:=0 to 10 do  // error
                begin
                    i:=-(-(i-1));
                    return ;
                end
        end
        """
        expect = "Unreachable statement: For(Id(I)IntLiteral(0),IntLiteral(10),True,[AssignStmt(Id(i),UnaryOp(-,UnaryOp(-,BinaryOp(-,Id(i),IntLiteral(1))))),Return(None)])"
        self.assertTrue(TestChecker.test(input,expect,457))
    def test_unreachable_stmt_more_complex(self):
        
        input = r"""
        procedure MaIn();
        begin
            foo();
            foo9();
        end

        procedure foo();
        var i:integer;
            f:real;
        begin
            for i:=0 downtO -100 do  //# no return
                return;

            if i=f then
                begin
                    f:=i+1;
                    return ;
                end
            else
                f:=i+12;
        end

        procedure foo9();
        var i:integer;
            f:real;
        begin
            for i:=0 downtO -100 do
                return;
            return;  //# return here

            if I=F then  // error
                begin
                    f:=i+1;
                    return;
                end
            else
                f:=i+12;
        end
        """
        expect = "Unreachable statement: If(BinaryOp(=,Id(I),Id(F)),[AssignStmt(Id(f),BinaryOp(+,Id(i),IntLiteral(1))),Return(None)],[AssignStmt(Id(f),BinaryOp(+,Id(i),IntLiteral(12)))])"
        self.assertTrue(TestChecker.test(input,expect,458)) 
    def test_func_not_return_complex(self):
        
        input = r"""
        procedure MaIn();
        var a:boolean;
        begin
            a:=foo();
            a:=foo12();
        end

        function foo():boolean;
        var a:integer;
        begin
            for a:=a to a do
                begin
                    a:=0;
                    if not (a=0) then
                        return falSE;
                    else
                        return false or false;
                end
            return foo();  //# return here
        end

        function foo12():boolean;  // error
        var a:integer;
        begin
            for a:=a to a do  //# no return
                begin
                    a:=0;
                    if not (a=0) then
                        return falSE;
                    else
                        return false or false;
                end
        end
        """
        expect = "Function foo12Not Return "
        self.assertTrue(TestChecker.test(input,expect,459))   
    def test_func_not_return_more_complex(self):
        
        input = r"""
        procedure MaIn();
        var a:boolean;
        begin
            a:=foo();
            a:=foo3();
        end
                
        function foo():boolean;
        begin
            if True then
                return falsE;  //# return here
            else
                return true;  //# return here
        end

        function foo3():boolean;  // error
        begin
            if True then  //# no return
                begin
                end
            else
                return True;
        end
        """
        expect = "Function foo3Not Return "
        self.assertTrue(TestChecker.test(input,expect,460))
    def test_redeclared_procedure_complex(self):
        input = r"""
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
        self.assertTrue(TestChecker.test(input,expect,461))
    def test_function_not_return_complex(self):
        input = r"""
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
        self.assertTrue(TestChecker.test(input,expect,462))
    def test_unreachable_func_complex(self):
        input = r"""
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
            procedure go();
            begin
            end
            procedure main();                
            begin
                a:=foo();
            end
        """
        expect =  "Unreachable Procedure: go"
        self.assertTrue(TestChecker.test(input,expect,463))
    def test_unreachable_stmt_more_complex2(self):
        input = r"""
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
        self.assertTrue(TestChecker.test(input,expect,464))
    def test_break_continue_not_in_loop_complex(self):
        input = r"""
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
        self.assertTrue(TestChecker.test(input,expect,465))
    def test_typemissmatch_exp_complex(self):
        input = r"""
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
        self.assertTrue(TestChecker.test(input,expect,466))
    def test_function_not_return_more_complex(self):
        input = r"""
        procedure MaIn();
        var a:boolean;
        begin
            a:=foo();
            a:=foo11();
        end

        function foo():boolean;
        var a:integer;
        begin
            while a = 1 do
                begin
                    a:=0;
                    if not (a=0) THEn
                        return falSE;
                    else
                        return false or false;
                end
            return foo();  
        end

        function foo11():boolean;  
        var a:integer;
        begin
            while a = 1 do  
                begin
                    a:=0;
                    if not (a=0) then
                        return falSE;
                    else
                        return false or false;
                end
        end
        """
        expect = "Function foo11Not Return "
        self.assertTrue(TestChecker.test(input,expect,467))
    def test_call_expr_param_len(self):
        input = r"""
        function foo():real;
        var a:integer;
        begin
            return a;
        end

        procedure MaIn();
        var a:real;
        begin
            a := foo();
            a := foo(1,2,3,4);  
        end
        """
        expect = "Type Mismatch In Expression: CallExpr(Id(foo),[IntLiteral(1),IntLiteral(2),IntLiteral(3),IntLiteral(4)])"
        self.assertTrue(TestChecker.test(input,expect,468))
    def test_type_binary_expr(self):
        input = r"""
        procedure foo(s:string);
        begin
            return ;
        end

        procedure MaIn();
        var a: integer;
        begin
            foo("ss");
            foo("s"*2);  
        end
        """
        expect = "Type Mismatch In Expression: BinaryOp(*,StringLiteral(s),IntLiteral(2))"
        self.assertTrue(TestChecker.test(input,expect,469))
    def test_expr1_arr_must_be_array_type(self):
        input = r"""
        procedure MaIn();
        var a:integer;
            arr:array[0 .. 4] of integer;
        begin
            arr[0]:=1;
            a[0]:=1;  
        end
        """
        expect = "Type Mismatch In Expression: ArrayCell(Id(a),IntLiteral(0))"
        self.assertTrue(TestChecker.test(input,expect,470))
    def test_unreachable_function_recursive1(self):
        
        input = r"""
        procedure main();
        begin
        end

        function recur(b:boolean):boolean;
        begin
            b:=recur(False);
            return false;
        end
        """
        expect = "Unreachable Function: recur"
        self.assertTrue(TestChecker.test(input,expect,471))
    def test_unreachable_procedure2(self):
        
        input = r"""
        procedure main();
        begin
        end

        procedure recur();
        begin
            recur();
        end
        """
        expect = "Unreachable Procedure: recur"
        self.assertTrue(TestChecker.test(input,expect,472))
    def test_unreachable_procedure_otr97(self):
        input = '''
            procedure main();
            begin
            end
            procedure func1();
            begin
                func2();
            end
            procedure func2();
            begin
                func3();
            end
            procedure func3();
            begin
                func4();
            end
            procedure func4();
            begin
                main();
            end
        '''
        expect = "Unreachable Procedure: func1"
        self.assertTrue(TestChecker.test(input,expect,473))
    def test_undeclared_identifier_func(self):
        input = '''
            function func(param: real):real;
            begin
                param := param + 1;
                return .11111999;
            end
            PROCEDURE Main();
            var x: real;
            begin
                x := (not (func(func(func(func(func)))) mod 2) and FALSE OR TRUE) * 1.1111999;
                putInt(x);
                return;
            end
        '''
        expect = "Undeclared Identifier: func"
        self.assertTrue(TestChecker.test(input,expect,474))
    def test_no_entry_point_main_funcion(self):
        input = '''
            function MAIN(x, y: integer):integer;
            begin
                return x - 1611931 + fx();
            end
            function fx():integer;
            begin
                return MAIN(0, 0);
            end
        '''
        expect = "No entry point"
        self.assertTrue(TestChecker.test(input,expect,475))
    def test_redeclared_procedure_builtin(self):
        input = '''
            procedure PUTSTRING(p:integer;q:real);
            begin
                putSTring("abc");
                return;
            end
            procedure main();
            begin
            end
        '''
        expect = "Redeclared Procedure: PUTSTRING"
        self.assertTrue(TestChecker.test(input,expect,476))
    def test_typemismatchstatement_while(self):
        input = '''
            procedure main();
            var a,b: boolean;
            begin
                with a:integer; do
                begin
                    while a do
                        a := a - 1;
                end
            end
        '''
        expect = "Type Mismatch In Statement: While(Id(a),[AssignStmt(Id(a),BinaryOp(-,Id(a),IntLiteral(1)))])"
        self.assertTrue(TestChecker.test(input,expect,477))
    ef test_undeclared_identifier_in_expr(self):
        input = '''
            procedure main();
            begin
                while 2 <> (3.5 / 4 / Getfloat moD 0) do
                begin
                    begin
                        begin end
                    end
                end
            end
        '''
        expect = "Undeclared Identifier: Getfloat"
        self.assertTrue(TestChecker.test(input,expect,478))
    def test_typemismatchstatement_for(self):
        input = '''
            var i, j, k: integer;
            procedure printrange(n: integer);
            begin
                for i := ((j + k div j + 10 - i) / 2) - 1 to n do
                    putIntLn(i);
            end
            procedure main();
            begin
                printRange(10);
            end
        '''
        expect = "Type Mismatch In Statement: For(Id(i)BinaryOp(-,BinaryOp(/,BinaryOp(-,BinaryOp(+,BinaryOp(+,Id(j),BinaryOp(div,Id(k),Id(j))),IntLiteral(10)),Id(i)),IntLiteral(2)),IntLiteral(1)),Id(n),True,[CallStmt(Id(putIntLn),[Id(i)])])"
        self.assertTrue(TestChecker.test(input,expect,479))
    def test_typemismatchstatement_assign_complex(self):
        input = '''
            function isPrime(main:integer):boolean;
            var i: integer;
            begin
                if main < 2 then
                    return NOT TRUE;
                else 
                begin
                    if main = 2 then
                        return TRUE;
                    else
                    begin
                        for i := 2 to main - 1 do
                            if (main mod i) = 0 then
                                return FALSE;
                        return TRUE;
                    end
                end
            end
            procedure main();
            var x, y: integer;
            begin
                x := getInt();
                y := isPrime(x);
                putString("Finish");
            end
        '''
        expect = "Type Mismatch In Statement: AssignStmt(Id(y),CallExpr(Id(isPrime),[Id(x)]))"
        self.assertTrue(TestChecker.test(input,expect,480))
    def test_typemismatchstatement_assign_more(self):
        input = '''
            var x, y, z: real;
                t, u: integer;
                k: boolean;
            procedure main();
            var u:boolean;
            begin
                u := u and k or u or k;
                z := t div 2 mod t;
                x := ((x + y * z) / t) + (t div t);
                t := ((t + 2 * t) / 3) + (t div 100);
                y := t / 0;
                k := (x > y) or else (y < z);
            end
        '''
        expect = "Type Mismatch In Statement: AssignStmt(Id(t),BinaryOp(+,BinaryOp(/,BinaryOp(+,Id(t),BinaryOp(*,IntLiteral(2),Id(t))),IntLiteral(3)),BinaryOp(div,Id(t),IntLiteral(100))))"
        self.assertTrue(TestChecker.test(input,expect,481))
    def test_typemismatchstatement_complex_return(self):
        input = '''
            var t: array[1 .. 2] of integer;
            procedure main();
            var foo: real;
            begin
                foo := func(t);
            end
            function Func(ab: array[1 .. 2] of integer):integer;
            var t: integer;
            begin
                ab[ab[10]] := t := 10;
                return ab[ab[t]] > ab[t];
            end
        '''
        expect = "Type Mismatch In Statement: Return(Some(BinaryOp(>,ArrayCell(Id(ab),ArrayCell(Id(ab),Id(t))),ArrayCell(Id(ab),Id(t)))))"
        self.assertTrue(TestChecker.test(input,expect,482))
    def test_typemismatchexpression_arraycell(self):
        input = '''
            var t: integer;
            procedure main();
            var x: array[0 .. 1] of integer;
            begin
                t := x[1 + 1 - 2 div 43];
                t := 2 + 1[2] div 1.5;
            end
        '''
        expect = "Type Mismatch In Expression: ArrayCell(IntLiteral(1),IntLiteral(2))"
        self.assertTrue(TestChecker.test(input,expect,483))
    def test_typemismatchexpression_operator(self):
        input = '''
            procedure main();
            begin
                with a,b:integer; c:boolean; d:string; do
                begin
                    c := ((-a---b) <> a) and then c;
                    a := (a Div b) mod 11 - 11 * 1999;
                    
                end
                return;
            end
        '''
        expect = "Type Mismatch In Expression: BinaryOp(DiV,BinaryOp(/,Id(a),Id(b)),Id(a))"
        self.assertTrue(TestChecker.test(input,expect,484))
    def test_breaknotinloop_complex(self):
        input = '''
            procedure MAIN();
            begin
                if True then
                begin
                    if false then
                    begin
                        putStringLn("break after here");
                        break;
                    end
                end
                return;
            end
        '''
        expect = "Break Not In Loop"
        self.assertTrue(TestChecker.test(input,expect,485))

    def test_function_notreturn_more_complex(self):
        input = '''
            function FOO():integer;
            var x, y: integer;
            begin
                while x <> y do
                begin
                    FOR x := 0 to 99 do 
                    begin
                        putString("not return");
                        if x * y <> 0 then
                            putStringLn("break after here");
                        else
                            break;
                        with a,b: integer; do
                        begin
                            if x * y <> 0 then
                                continue;
                            else
                                putStringLn("return after here");
                            return 0;
                        end
                    end
                    return 0;
                end
            end
            procedure main();
            var func: integer;
            begin
                func := foo();
            end
        '''
        expect = "Function FOONot Return "
        self.assertTrue(TestChecker.test(input,expect,486))
    def test_typemismatch_with_str(self):
        input = """
        procedure main();
        var a: boolean;
        begin
            a:= false / "abc";
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(/,BooleanLiteral(False),StringLiteral(abc))'
        self.assertTrue(TestChecker.test(input,expect,487))
    def test_op_or(self):
        input = """
        procedure main();
        var a: boolean;
        begin
            a:= false or "abc";
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(or,BooleanLiteral(False),StringLiteral(abc))'
        self.assertTrue(TestChecker.test(input,expect,488))
    def test_op_boolean(self):
        input = """
        procedure main();
        var a: boolean;
        begin
            a:= false <= true;
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(<=,BooleanLiteral(False),BooleanLiteral(True))'
        self.assertTrue(TestChecker.test(input,expect,489))
    def test_op_add_boolean(self):
        input = """
        procedure main();
        var a: boolean;
        begin
            a:= false + true;
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(+,BooleanLiteral(False),BooleanLiteral(True))'
        self.assertTrue(TestChecker.test(input,expect,490))
    def test_op_equal_boolean(self):
        input = """
        procedure main();
        var a: boolean;
        begin
            a:= false = false;
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(=,BooleanLiteral(False),BooleanLiteral(False))'
        self.assertTrue(TestChecker.test(input,expect,491))
    def test_op_assign_str(self):
        input = """
        procedure main();
        var a: string;
        begin
            a:= "abc" <= 1;
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(<=,StringLiteral(abc),IntLiteral(1))'
        self.assertTrue(TestChecker.test(input,expect,492))
    def test_op_string_sub(self):
        input = """
        procedure main();
        var a: string;
        begin
            a:= "abc" - 1;
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(-,StringLiteral(abc),IntLiteral(1))'
        self.assertTrue(TestChecker.test(input,expect,493))

    def test_op_string_mul(self):
        input = """
        procedure main();
        var a: string;
        begin
            a:= "abc" * 1;
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(*,StringLiteral(abc),IntLiteral(1))'
        self.assertTrue(TestChecker.test(input,expect,494))

    def test_op_string_divide(self):
        input = """
        procedure main();
        var a: string;
        begin
            a:= "abc" / 1;
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(/,StringLiteral(abc),IntLiteral(1))'
        self.assertTrue(TestChecker.test(input,expect,495))

    def test_op_string_div(self):
        input = """
        procedure main();
        var a: string;
        begin
            a:= "abc" div 1;
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(div,StringLiteral(abc),IntLiteral(1))'
        self.assertTrue(TestChecker.test(input,expect,496))

    def test_op_string_mod(self):
        input = """
        procedure main();
        var a: string;
        begin
            a:= "abc" mod 1;
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(mod,StringLiteral(abc),IntLiteral(1))'
        self.assertTrue(TestChecker.test(input,expect,497))
    def test_op_string_andthen(self):
        input = """
        procedure main();
        var a: string;
        begin
            a:= "abc" and then 1;
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(andthen,StringLiteral(abc),IntLiteral(1))'
        self.assertTrue(TestChecker.test(input,expect,498))

    def test_op_string_orelse(self):
        input = """
        procedure main();
        var a: string;
        begin
            a:= "abc" or else 1;
        end
        """
        expect = 'Type Mismatch In Expression: BinaryOp(orelse,StringLiteral(abc),IntLiteral(1))'
        self.assertTrue(TestChecker.test(input,expect,499))

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

    
    