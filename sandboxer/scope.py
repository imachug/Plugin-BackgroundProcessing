class Scope(object):
    def __init__(self, inherits=None):
        self.vars = {}
        self.inherits = inherits
        self.inheritsVariable = {}

    def import_(self, names, from_, level):
        for name, asname in names:
            if asname is None:
                asname = name

            if from_ is not None:
                line = "from %s import %s as import_module" % (from_, name)
            else:
                line = "import %s as import_module" % name

            exec compile(line, "<import>", "single")
            self[asname] = import_module
            del import_module


    def __getitem__(self, name):
        if name in self.inheritsVariable:
            scope = self.inheritsVariable[name]
            return scope[name]
        if name in self.vars:
            return self.vars[name]

        # Vars
        if name == "vars":
            return self.getVars()


        if self.inherits is not None:
            return self.inherits[name] # Recursive: type(inherits)==Scope

        raise NameError(name)

    def __setitem__(self, name, value):
        if name in self.inheritsVariable:
            scope = self.inheritsVariable[name]
            scope[name] = value
            return

        self.vars[name] = value


    def inherit(self):
        return Scope(self)
    def inheritVariable(self, scope, name):
        self.inheritsVariable[name] = scope


    def getVars(self):
        class ThisNone(object):
            pass
        def vars(object=ThisNone):
            if object is ThisNone:
                return self.locals()
            return object.__dict__
        return vars