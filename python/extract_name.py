#!/usr/bin/env python3

class ClassDef(object):
    def __init__(self, cls_name):
        self.cls_name = cls_name
        self.meths = []
        self.fields = []
    def add_meth(self, meth):
        self.meths.append(meth)
    def add_field(self, field):
        self.fields.append(field)
    def dump(self):
        print(self.cls_name)
        for m in self.meths:
            print(' '*2, m)
        for f in self.fields:
            print(' '*2, f)
    def to_file(self, fname):
        if self.cls_name.find('>') != -1: return
        if self.cls_name.find('<') != -1: return
        if self.cls_name.find('(') != -1: return
        if self.cls_name.find(')') != -1: return
        if self.cls_name.find('*') != -1: return
        buf = ''
        buf += '#ifndef _{}_\n'.format(self.cls_name.upper())
        buf += '#define _{}_\n'.format(self.cls_name.upper())
        buf += 'struct {}\n{{\n'.format(self.cls_name)
        for m in self.meths:
            buf += '  {}\n'.format(m)
        for f in self.fields:
            buf += '  {}\n'.format(f)
        buf += '}\n'
        buf += '#endif\n'
        with open(fname, 'w') as f:
            f.write(buf)

G_ALL_CLASS = dict()
def get_class(cls_name):
    if cls_name in G_ALL_CLASS:
        return G_ALL_CLASS[cls_name]
    cd = ClassDef(cls_name)
    G_ALL_CLASS[cls_name] = cd
    return cd

def main():
    with open('names.txt', 'r') as f:
        ls = f.readlines()
        ls = [l.strip() for l in ls]
    for l in ls:
        if l.find('::') == -1: continue
        parts = l.split('::')
        if len(parts) < 2: continue
        leaf = parts[-1]
        node = parts[-2]
        if node.find('(') != -1: continue
        cd = get_class(node)
        if leaf.endswith(')'):
            cd.add_meth(leaf)
        else:
            pass
            cd.add_field(leaf)
    for k,v in G_ALL_CLASS.items():
        if ord('A') <= ord(k[0]) <= ord('Z'):
            v.dump()
            if k[0] == 'C':
                fname = 'out/{}.h'.format(k)
                print(k, fname)
                v.to_file(fname)

    print('total item ', len(G_ALL_CLASS))
if __name__  == '__main__':
    main()
