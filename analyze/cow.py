# -*- coding: utf-8 -*-  
# create: 2015/5/26
# author: Yu
from gap import GAP
from reverse import ReverseSignal
from weak_down import WeakDownSignal
from jump_out import JumpOutSignal


print '====================== Jump Out Signal ======================'
JumpOutSignal().check()

print '====================== Weak Down Signal ======================'
WeakDownSignal().check()


print '====================== Reverse Signal ======================'
ReverseSignal().check()

print '====================== GAP Signal ======================'
GAP().check()

