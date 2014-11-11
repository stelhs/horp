from horp import Program, Compiler, HorpError

try:
    prog = Program('example.horp.c')
    compiler = Compiler(prog)
    #print compiler.tree
    f = open('example.c', 'w')
    f.write(compiler.compile())
    f.close()
    print 'done'
except HorpError, msg:
    print('Parser error: ' + msg.message)

