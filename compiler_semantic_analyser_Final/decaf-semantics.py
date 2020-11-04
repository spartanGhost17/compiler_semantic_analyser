import antlr4 as ant
from DecafLexer import DecafLexer
from DecafParser import DecafParser
from DecafVisitor import DecafVisitor
from SymbolTable import HEAP, STACK, SymbolTable, VarSymbol, MethodSymbol

class DecafSemanticChecker(DecafVisitor):
    def __init__(self):
        super().__init__()
        self.st = SymbolTable()
        
    def visitProgram(self, ctx:DecafParser.ProgramContext):
        ##enter global scope
        self.st.enterScope()
        ##visit all children
        self.visitChildren(ctx)
        ##leave global scope
        self.st.exitScope()       
        
    # Visit a parse tree produced by DecafParser#expr.
    def visitExpr(self, ctx:DecafParser.ExprContext):
        
        line_num = ctx.start.line
        
        #print(">>>>>> list of expr ",len(ctx.expr()))
        
        if ctx.location():
            loc_name = ctx.location().ID().getText()
            #print("##### ",loc_name)
            location = self.st.lookup(loc_name) ##look to local and global scope
            
            ##if location name is not yet define Error
            if location==None:
                print("\nError at line ",line_num,
                      " variable '",loc_name,"' assigned before it is defined\n")
        ##if expression is method call
        elif ctx.method_call():
             ## visit method call
             print("\nEXPR before visit method call\n")

        ##if we have two expression evaluation
        elif len(ctx.expr()) == 2:            
            expr0_type = "None"
            expr1_type = "None"
            ## check for expr0 
                        
            if ctx.expr(0).location()!=None:
                ##find location on the symbol table to see if it was declared
                expr0_name = self.st.probe(ctx.expr(0).location().ID().getText())
                if expr0_name!=None:
                    expr0_type = expr0_name.type
                else:
                    print("\nError at line",line_num," variable \n")

            elif ctx.expr(0).method_call():
                expr0_name = self.st.lookup(ctx.expr(0).method_call().method_name().getText())
                
                if expr0_name != None:
                    expr0_type = expr0_name.type.getText()
                    #print("\n++++++++++++ epxr 0 is method call ",expr0_type)
                else:
                    print("\nError at line ",line_num," method was not declared\n")
            
            elif ctx.expr(0).literal():
                ##if expr is literal, see which kind
                if ctx.expr(0).literal().int_literal():
                    expr0_type = "int"
                elif ctx.expr(0).literal().bool_literal():
                    expr0_type = "boolean"
                elif ctx.expr(0).char_literal():
                    expr0_type = "char"
                elif ctx.expr(0).literal().string_literal():
                    expr0_type = "string"
                    #print(">>>>>> ",expr0_type)
            
            ##visit expr1
            
            
            if ctx.expr(1).location()!=None:
                ##find location on the symbol table to see if it was declared
                expr1_name = self.st.probe(ctx.expr(1).location().ID().getText())
                if expr1_name!=None:
                    expr1_type = expr1_name.type
                else:
                    print("\nError at line",line_num," variable ",expr1_name.id,"\n")
                    
            elif ctx.expr(1).method_call():
                expr1_name = self.st.lookup(ctx.expr(1).method_call().method_name().getText())
                expr1_type = expr1_name.type.getText()
                if expr1_name != None:
                    expr1_type = expr1_name.type.getText()
                    #print("\n++++++++++++ epxr 1 is method call ",expr1_type)
                else:
                    print("\nError at line ",line_num," method ",expr1_name.id," was not declared\n")
            
            elif ctx.expr(1).literal():
                ##if expr is literal, see which kind
                if ctx.expr(1).literal().int_literal():
                    expr1_type = "int"
                elif ctx.expr(1).literal().bool_literal():
                    expr1_type = "boolean"
                elif ctx.expr(1).char_literal():
                    expr1_type = "char"
                elif ctx.expr(1).literal().string_literal():
                    expr1_type = "string"
            
            
            if expr0_type !="None" and expr1_type !="None":
                if ctx.PLUS() or ctx.MINUS() or ctx.MULTIPLY() or ctx.DIVIDE() or ctx.MOD():
                    ##print("\n TEST TYPE VAR 1 ", expr0_type, " TYPE VAR2 ",expr1_type,"\n")
                    
                    if expr0_type != expr1_type:
                        print("\nError at line ",line_num," Type missmatch for operation, expression '",
                              expr0_name.id,"' is of type '",expr0_type.getText(),
                              "' and expression '",expr1_name.id,"' of type '",expr1_type.getText(),"' \n")
     
                elif ctx.LESS_THAN() or ctx.GREATER_THAN() or ctx.LESS_OR_EQUAL() or ctx.GREATER_OR_EQUAL() or ctx.DOUBLE_EQUAL() or ctx.NOT_EQUAL() or ctx.AND() or ctx.OR():
                    if expr0_type != expr1_type:
                        print("\nError at line ",line_num," Type missmatch for operation, expression '",
                              expr0_name.id,"' is of type '",expr0_type.getText(),
                              "' and expression '",expr1_name.id,"' of type '",expr1_type.getText(),"' \n")
            
            ##If one of the two expression is None, print error            
            elif expr0_type =="None" or expr1_type =="None":
                print("\nError at line ",line_num," operation cannot be performed",
                      " one of the expression was not declared \n")            
            
            
        self.visitChildren(ctx)
        

    # Visit a parse tree produced by DecafParser#statement.
    def visitStatement(self, ctx:DecafParser.StatementContext):
        
        flag = True
        line_num = ctx.start.line
        ##think about handling case with data type
        ##if statement has assigment op
        if ctx.FOR():
            ##if VAR ID doesn't exist, error 
            if self.st.lookup(ctx.ID().getText())!=None:
                print("\nError at line",line_num," variable ",ctx.ID().getText(),
                      " assigned before it is declared\n")
        elif ctx.FOR() == None and (ctx.CONTINUE() or ctx.BREAK()):
                print("\nError at line",line_num," no for loop was defined \n")            
                               
            
        self.visitChildren(ctx)        
        

    def visitVar_decl(self, ctx:DecafParser.Var_declContext):

        line_num = ctx.start.line 
        variable_decl_ID = ctx.ID()
        var_type = ctx.data_type()
               
        ##iterate list of variable declarations

        for i in range(len(variable_decl_ID)):
            var_ID = variable_decl_ID[i].getText()
            #print("............ ",var_ID)
            
            ##check if variable was declared in the current scope
            var_symbol = self.st.probe(var_ID)
            ## if declared var is in current scope, Error. Else add to it to current scope
            if var_symbol != None:
                print("\nError at line ",line_num,
                          "duplicate variable ",var_ID," already exists at line ",var_symbol.line)
            else:
                    
                var_symbol = VarSymbol(id=var_ID,
                                       type=var_type,
                                       line=line_num,
                                       size=8,
                                       mem=HEAP)
                self.st.addSymbol(var_symbol)        
        
        self.visitChildren(ctx)
        
     


    def visitField_decl(self, ctx:DecafParser.Field_declContext):
        data_type = ctx.data_type().getText()
        line_num = ctx.start.line
        array_size = 1
        if ctx.SEMICOLON() == None:
            print("\nMissing Semicolon at line ",line_num)        
        
        ##for all field_names in field declaration 
        for i in range(len(ctx.field_name())):
            field_name = ctx.field_name(i)
            ##look at symbol table of local scope for field_name at index i
            field_symbol = self.st.probe(field_name.ID().getText())
            
            ## if field name exists and contains an int literal, we have an array
            ## array declaration cannot have size of less than zero
            if field_name.int_literal() != None:
                #print("\n------------- ",field_name.int_literal().getText())
                array_size = int(field_name.int_literal().getText())
                if array_size <= 0:
                    print("\nNew Error on line ",line_num,
                          " field Array ", field_name.ID().getText(),
                          " can only have size greater than zero\n")
            
            ## if field ID exists on the symbol table in current scope, Print Error    
            if field_symbol != None:
                print("\nError at line ",line_num,
                      "field'", field_name.ID().getText(),
                      "' already declared on line ",field_symbol.line,"\n")
       
            else:
                ## create symbol 
                field_symbol = VarSymbol(id=field_name.ID().getText(),
                                         type=data_type,
                                         line=line_num,
                                         size=8*array_size,#multiply bytes by 8 if array, int take size 8 in x86 
                                         mem=HEAP)
                self.st.addSymbol(field_symbol)
        
        ##visit children        
        self.visitChildren(ctx)


    def visitMethod_decl(self, ctx:DecafParser.Method_declContext):
        #create method symbol
        # store a list of params in the method symbol
        # push method symbol with params list to global scope
        line_num = ctx.start.line
        method_id = ctx.method_name().getText()
        method_params=[]
        
        method_type = ctx.return_type()
        
        ##check local scope for method name
        method_symbol = self.st.probe(ctx.method_name().getText())
        
        ##if method exists error
        ##else, method doesn't exist, add it to scope

        if method_symbol !=None:
            print("\nError at line ",line_num," method ",method_id,
                  " was already declared on line ",method_symbol.line)
        else:
            
            ##create method parameters as var symbol objects + create method method and add to symbol table
            ##visible for current scope
            for i in range(len(ctx.ID())):
                param_type = ctx.data_type(i).getText()
                param_name = ctx.ID(i).getText()
                param_symbol = VarSymbol(id=param_name,type=param_type,line=line_num,size=8,mem=STACK)
                method_params.append(param_symbol)##add symbol obj to list
                        
                method_symbol = MethodSymbol(id=method_id,
                                            type=method_type,
                                            line=line_num,
                                            params=method_params)
                self.st.addSymbol(method_symbol)      
                
        #enter new local scope for variables within methods
        self.st.enterScope()
        method_type = ctx.return_type().getText()
        
        ## for every param in list create 
        for i in range(len(method_params)):
            data_type = method_params[i].type 
            param_name = method_params[i].id
            var_symbol = self.st.probe(param_name)
            if var_symbol != None:
                print("\nError at line ",line_num,"duplicate parameter ",data_type," ",param_name,
                      " was already declared on a line "
                      ,var_symbol.line)
            else:
                ##add current symbol to symbol table
                self.st.addSymbol(method_params[i])
        
        ##visit all children in current scope
        self.visitChildren(ctx)
        ##exist local scope
        self.st.exitScope()   

    # Visit a parse tree produced by DecafParser#method_call.
    def visitMethod_call(self, ctx:DecafParser.Method_callContext):
        method_name = ctx.method_name().getText()
        line_num = ctx.start.line
        
        ##lookup other scopes for method id
        method_symbol = self.st.lookup(method_name)
        
        ##if method name does not exist Error, cannot call a non defined method
        if method_symbol == None:
           print("\nError at line ",line_num,
                 " method '",ctx.method_name().getText(),"' was not declared \n")
        
        ## if method name alredy exists on symbol table
        elif method_symbol  != None:
            
            ##if 
            ##if we don't have the same number of arguments, error! 
            if len(ctx.expr())!=len(method_symbol.params):
                print("\nError at line ",line_num ," The number and types of arguments in a ",
                      "method call must be the same as the number and types of formal ",
                      "signature must identical to method '", method_symbol.id,
                      "' at line ", method_symbol.line, "\n")
                
            ##if we have the same number of arguments
            ##check that type match to type of argument in method signature
            elif len(ctx.expr())==len(method_symbol.params):
                
                for i in range(len(ctx.expr())):
                    ##if we have a location
                    if ctx.expr()[i].location() != None:
                        ##see that location was declared
                        var_symbol1 = self.st.lookup(ctx.expr()[i].location().ID().getText())
                        ##if location exists
                        if var_symbol1 != None:
                            ##check if it has same type as the param at that index on st
                            if var_symbol1.type != method_symbol.params[i].type:    
                                print("\nError at line ",line_num ," The number and types of arguments in a ",
                                      "method call must be the same as the number and types of formal ",
                                      "signature must identical to method '", method_symbol.id,
                                      "' at line ", method_symbol.line, "\n")
                    
                    ##if expression is method call retreive method parsed as argument from st
                    elif ctx.expr()[i].method_call() != None:
                        
                        ##see if method call was declared
                        method_symbol1 = self.st.lookup(ctx.expr()[i].method_call().method_name().getText())
                        
                        ##if method symbol is found
                        if method_symbol1 != None:
                            
                            ##since it's an <argument> method call visit children of method call to see if they are legal
                            #------self.visitChildren(ctx.expr()[i])

                            ## check if types are different, Error
                            if method_symbol1.type.getText() != method_symbol.params[i].type:    
                             print("Error at line",line_num,
                                   " type missmatch found, return type of method argument '",method_symbol1.id,
                                   "' argument n ",i,
                                   " must be of type '",method_symbol.params[i].type,"' for method '",method_symbol.id,
                                   "' decalared at line ",method_symbol.line,"\n")
                            
                            
                    ##check if expr is a literal       
                    elif ctx.expr()[i].literal() != None:
                        ##if we have an int_literal check if type of param at same index is same type 
                         if ctx.expr()[i].literal().int_literal() != None and method_symbol.params[i].type!="int":

                             print("_____Error at line",line_num,
                                   " type missmatch found, argument n ",i,
                                       " must be of type '",method_symbol.params[i].type,"' for method '",method_symbol.id,
                                       "' decalared at line ",method_symbol.line,"\n")
                             
                         ##if we have an bool_literal check if type of param at same index is same type boolean     
                         elif ctx.expr()[i].literal().bool_literal() != None and method_symbol.params[i].type!="boolean":

                             print("Error at line",line_num,
                                       " type missmatch found, argument n ",i,
                                       " must be of type '",method_symbol.params[i].type,"' for method '",method_symbol.id,
                                       "' decalared at line ",method_symbol.line,"\n")
                             
                         ##if we have an char_literal check if type of param at same index is same type char
                         elif ctx.expr()[i].literal().char_literal() != None and method_symbol.params[i].type!="char":

                             print("////Error at line",line_num,
                                       " type missmatch found, argument n ",i,
                                       " must be of type '",method_symbol.params[i].type,"' for method '",method_symbol.id,
                                       "' decalared at line ",method_symbol.line,"\n")   
                            

                             
        elif ctx.CALLOUT():
            pass          
        self.visitChildren(ctx)
      

filein = open('test.dcf', 'r')
lexer = DecafLexer(ant.InputStream(filein.read()))

stream = ant.CommonTokenStream(lexer)

parser = DecafParser(stream)
tree = parser.program()

visitor = DecafSemanticChecker()
visitor.visit(tree)
