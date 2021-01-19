# nqueens_csp

This simple program solves the n-queens problem.  This is the problem in which you must
place a number of queens on a chess board in a way that none of them 'threaten' each other.
A queen is considered to 'threaten' another queen in the same row, column, or either
diagonal direction.  

To represent the problem, it is set up as a constraint satisfaction problem.  Each queen
is given a set of constraints and these constraints must be satisfied in order for the problem to 
be solved.  In order to place the queens in their respective rows, the AC3 algorithm is implemented
along with a recursive backtracking search algorithm.  


