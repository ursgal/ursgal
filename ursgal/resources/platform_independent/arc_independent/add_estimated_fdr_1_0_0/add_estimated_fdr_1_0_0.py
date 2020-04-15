#!/media/lukas/storage/uni/forschungsmodul_proteomics/pypercolator/pypercolator/bin/python

'''
Parses a target/decoy search result file and adds a column called "estimated_FDR".
The CSV has to contain: a column with a quality score for each PSM (e-value, error probability etc.)
and a column called "Is decoy" indicating whether a PSM is decoy or target.

usage:
./add_estimated_fdr_1_0_0.py search_results.csv output_filename.csv name_of_my_quality_score_column
'''

import csv
import os.path
import sys


def calc_FDR ( PSM_count, false_positives ):
    '''
    calculate false discovery rate according to FDR Method 2
    (Käll et al. 2007) as explained by Jones et al. 2009
    '''
    true_positives  = PSM_count - (2 * false_positives)
    if true_positives <= 0:  # prevent FDR above 1. Not sure if this is done?
        return 1.0
    FDR = false_positives / ( false_positives + true_positives)
    return FDR


def main( input_file=None, output_file=None, score_colname=None, bigger_scores_better=False ):
    
    assert input_file is not None, "add_estimated_FDR requires an input file!"
    assert score_colname is not None, "add_estimated_FDR needs to know the quality score column's name!"

    if output_file is None:
        base, ext   = os.path.splitext( input_file )
        output_file = base + "_FDR" + ext

    PSM_count   = 0
    decoy_count = 0
    
    with open( input_file, 'r' ) as in_csv:
        with open( output_file, 'w', newline='' ) as out_csv:
            
            reader     = csv.DictReader( in_csv )

            assert "estimated_FDR" not in reader.fieldnames, '''
  Input file {0} to add_estimated_fdr already has a column called "estimated_FDR"!
            '''.format( input_file )

            print('''Sorting {0} by column "{1}" ...'''.format(input_file, score_colname) )

            sorted_csv = sorted( reader, key=lambda d: float(d[ score_colname ]), reverse=bigger_scores_better )
            header     = reader.fieldnames + [ "estimated_FDR" ]

            writer     = csv.DictWriter( out_csv, header )
            writer.writeheader()

            print('''Adding "estimated_FDR" column to {0} ...'''.format(input_file) )

            # Traverse identifications from lowest score to highest:
            for row in sorted_csv:
                PSM_count += 1

                if row['Is decoy'].lower() == 'true':
                    decoy_count += 1

                # calculate and store the estimated FDR (FDRest) for each identification according to FDR Method 2.
                row["estimated_FDR"]  = calc_FDR ( PSM_count, decoy_count )
                writer.writerow( row )


if __name__ == "__main__":
    main(
        input_file    = sys.argv[1],
        output_file   = sys.argv[2],
        score_colname = sys.argv[2],
    )