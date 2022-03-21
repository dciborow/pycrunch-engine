import os
from time import sleep


def test_dummy():
    # print('test_method')
    print('222 ')
    print('222 ')
    print('222 ')
    print('222 ')
    print('222 ')

    print('te st_method 2')

def test_x():
    print('test_x before assert')
    print(f'PID in test: {os.getpid()}')

    assert True
    print('test_method 3')

def test_z():
    print('test_method y')

def test_failing():
    assert True
    assert 3 == 2
