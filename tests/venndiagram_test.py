import ursgal
import csv
import os
import glob

input1 = os.path.join(
    'tests',
    'data',
    'venndiagram',
    'venndiagram_test_input1.csv'
)

input2 = os.path.join(
    'tests',
    'data',
    'venndiagram',
    'venndiagram_test_input2.csv'
)

input3 = os.path.join(
    'tests',
    'data',
    'venndiagram',
    'venndiagram_test_input3.csv'
)

expected_output = os.path.join(
    'tests',
    'data',
    'venndiagram',
    'venndiagram_test_expected_output.csv'
)

column_name = ['Sequence']
output_diagram = 'testing_diagram'

def venndiagram(input1, input2, input3, column_name, output_diagram, engine_version):
    '''
    Example for plotting a simple Venn diagram with single ursgal csv files.

    usage:
        ./simple_venn_example.py


    '''
    uc = ursgal.UController(
        params={
            'visualization_label_positions': {
                '0': 'set1',
                '1': 'set2',
                '2': 'set3'
            },

            'visualization_column_names': column_name,
            'visualization_header' : output_diagram,
            'extract_venndiagram_file' : True,
        }
    )

    file_list = [input1, input2, input3]

    output_path = uc.visualize(
        input_files=file_list,
        engine=engine_version,
        output_file_name='actual_output',
        force=True,
    )

    for file in glob.glob(os.path.join(os.path.dirname(output_path),'*.json')):
        os.remove(file)

    for file in glob.glob(os.path.join(os.path.dirname(output_path),'*.svg')):
        os.remove(file)

    return output_path

return_list = []
expected_list = []
for engine_version in ['venndiagram_1_0_0', 'venndiagram_1_1_0']:
    output_path = venndiagram(
        input1,
        input2,
        input3,
        column_name,
        output_diagram,
        engine_version
    )

    #sort the venndiagram results by sequence column
    output_csv_file = output_path.replace('.svg','.csv')
    with open(output_csv_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        sortedList = sorted(reader, key=lambda row: row['Sequence'], reverse=False)

        with open(output_csv_file, 'w', newline='') as ff:
            writer = csv.DictWriter(ff, fieldnames=fieldnames)
            writer.writeheader()
            for row in sortedList:
                writer.writerow(row)


    for row in csv.DictReader(open(output_csv_file, 'r')):
        return_list.append(row)

    for row in csv.DictReader(open(expected_output, 'r')):
        import pprint
        pprint.pprint(row)
        expected_list.append(row)

    #initial test
    assert len(return_list) == len(expected_list)

def venndiagram_test():
    for test_id, expected_dict in enumerate(expected_list):
        test_dict = return_list[test_id]
        yield venndiagram_output, test_dict, expected_dict

def venndiagram_output(test_dict, expected_dict):
    assert test_dict == expected_dict, print(
        test_dict,
        expected_dict
    )

if __name__ == '__main__':
    print(__doc__)
    for test_id, expected_dict in enumerate(expected_list):
        test_dict = return_list[test_id]
        venndiagram_output(test_dict, expected_dict)