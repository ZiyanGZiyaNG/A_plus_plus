# parser.py

from ast_nodes import *

sample_program = Block([
    Assign("x", Number(3)),

    IfElse(
        BinaryOp(">=", Variable("x"), Number(2)),
        then_body=Block([
            Print(Variable("x")),
            While(BinaryOp(">", Variable("x"), Number(0)), Block([
                Print(Variable("x")),
                Assign("x", BinaryOp("-", Variable("x"), Number(1)))
            ]))
        ]),
        else_body=Block([
            Print(Number(0))
        ])
    ),

    Assign("sum", Number(0)),
    For("i", Number(1), Number(4), Block([
        Assign("sum", BinaryOp("+", Variable("sum"), Variable("i"))),
        IfElse(
            BinaryOp("==", BinaryOp("%", Variable("i"), Number(2)), Number(0)),
            then_body=Block([
                Print(Variable("i"))
            ]),
            else_body=Block([
                Print(Number(999))
            ])
        )
    ])),

    Print(Variable("sum"))
])
