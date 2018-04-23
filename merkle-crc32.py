#!/usr/bin/env python3

import binascii

def hash(input):
    '''Calculate crc32 and convert to hex'''
    return '%08x' % binascii.crc32(input)

def hash_two(i, j):
    '''Concatenate two ascii hex numbers and hash them'''
    return hash((i + j).encode())

#l1 = ['Max', 'Ove', 'Per', 'Ali', 'Rex', 'Alf', 'Ida', 'Eli']
#l1 = ['Max', 'Ove', 'Ior', 'Ali', 'Rex', 'Alf', 'Ida', 'Eli']
l1 = ['Max', 'Rei', 'Ior', 'Ali', 'Rex', 'Alf', 'Ida', 'Eli']

l1b = [i.encode() for i in l1]

l1hash = [hash(i) for i in l1b]

print()
for n in l1:
    print('  ', n, '  ', end='')
print()
for h in l1hash:
    print(h, '', end='')
print()
print('     \    /            \    /            \    /            \    /       ')

l2hash = []
for i in range(0,len(l1hash),2):
    l2hash += [hash_two(l1hash[i], l1hash[i+1])]
for h in l2hash:
    print('   ', h, '     ', end='')
print()
print('            \        /                          \        /              ')

l3hash = []
for i in range(0,len(l2hash),2):
    l3hash += [hash_two(l2hash[i], l2hash[i+1])]
for h in l3hash:
    print('            ', h, '              ', end='')
print()
print('                    \___________        _________/')

print('                               ', hash_two(l3hash[0], l3hash[1]))
print()
