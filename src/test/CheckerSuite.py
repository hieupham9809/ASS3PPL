import unittest
from TestUtils import TestChecker
from AST import *

class CheckerSuite(unittest.TestCase):
    '''def test_redeclared_builtin_procedure(self):
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
        expect = "Type Mismatch In Expression: For(Id(a)IntLiteral(1),IntLiteral(10),True,[])"
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
        self.assertTrue(TestChecker.test(input,expect,452))'''
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

    
    