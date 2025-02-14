# Inference Engine
This is my implementation of a Propositional Logic Inference Engine that processes queries within Horn-form Knowledge Bases (KBs) through user-supplied files. The engine is designed to utilize three fundamental inferential methods: Truth Table (TT), Forward Chaining (FC), and Backward Chaining (BC). Each method uniquely evaluates whether a given query, represented as a propositional symbol, can be derived from the rules and facts outlined in the KB. The inference engine's functionality is encapsulated in a command-line interface, which allows for straightforward operation and testing

# Usage instruction
If you are using a Windows machine, you can use Command Prompt to run the program by either typing “cmd” into the Start menu or press Windows + R to open the Run program and then type “cmd”. After that, navigate to the directory where you have all the source code of the program.
Before executing the program, make sure you have installed all the necessary python packages, which is only Sympy in this case. To do that, simply run pip install SymPy from your command line. The syntax for how to run the program from windows 10 Command Prompt is as below.
 ``` python main.py [path to input file] [algorithm] ```
 There are three necessary command line arguments needed to execute the program. The first required argument is the file that containing the driver code of the program, which in this case is main.py. The next argument, <filename>, is the path to the text file containing input for the knowledge base and the query. The third argument is the algorithm the program should perform. There are four available options for the [algorithm] command line argument:
-	BC – Backward Chaining
-	FC – Forward Chaining
-	TT – Truth Table
-	RES – Resolution-based prover
One restriction is that forward chaining and backward chaining can only work with Horn-based KB. Therefore, if BC or FC is performed with a generic knowledge base, the output will be “Not Implemented”.
An example program execution command can be as follows:
python main.py tests/HornKB/test_HornKB.txt TT

For those with a MacOS machine, the process is quite similar to the one above, except that you are going to use the terminal.

For more details, refer to [this documentation](https://drive.google.com/file/d/1mYt-z7bOb1UDf5GzNgSW-ldUkjMmjhjJ/view?usp=sharing)
