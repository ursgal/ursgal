'''
usage: python _test_node.py -i x -o test.txt -t1 a -t2 3
'''
import argparse

'''

NOTE:
    Currently the wrapper does not call this function.

'''

def _test(**kwargs):
    '''
    '''
    with open(kwargs['output_file'], 'w') as outf:
        for key, val in kwargs.items():
            outf.write('{0},{1}\n'.format(key, val))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-i', '--input_file', type=str, required=True,
        help='Input file name')
    parser.add_argument(
        '-o', '--output_file', type=str, required=True,
        help='Output file name')
    parser.add_argument(
        '-t1', '--test1', type=str, required=True,
        help='Test parameter 1')
    parser.add_argument(
        '-t2', '--test2', type=int, required=True,
        help='Test parameter 2')

    _test(
        **vars(parser.parse_args())
    )
