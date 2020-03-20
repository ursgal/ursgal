#!/usr/bin/python

# ./combined_FDR2.py /media/lukas/storage/uni/uSearch/combined_FDR --label 15N --cutoff 0.01

from __future__ import print_function
from __future__ import division

from collections import OrderedDict
from collections import defaultdict as ddict
from itertools import compress, product
from csv import DictReader, DictWriter
from pprint import pprint
import argparse
import glob
import os.path



def geometric_mean ( *values ):
    '''
    (without fancy imports...)
    n = number of values
    geo. mean = nth root of all values multiplied with each other
    '''
    product = 1
    for val in values:
        product *= val
    n = len(values)
    
    return product ** (1 / n)  # nth root of product


def calc_intercept_and_slope (a, b):
    '''
    Given two points in 2D-space (tuples a and b), calculates
    the slope (m) and intercept (b) of the line connecting
    both points. Required for FDR Score calculcation.
    Returns intercept and slope in a tuple.
    '''
    # calculating the slope (m) between two points
    if b[0] - a[0] == 0:
        slope = 0
    else:
        slope = \
        (
            ( b[1] - a[1] )
            /
            ( b[0] - a[0] )
        )
    # calculating the intercept (b) of that slope (b = -m * x + y):
    intercept = -slope*a[0] + a[1]
    
    # prevent PEPs above 1 because that would not make sense.
    #if intercept > 1:
        #intercept = 1

    return (intercept, slope)


def all_combinations( iterable ):
    '''
    example:
    
    input:  [ 'xtandem', 'msgf', 'omssa' ]
    output: [{'omssa'}, {'msgf'}, {'msgf', 'omssa'}, {'xtandem'}, {'xtandem', 'omssa'}, {'msgf', 'xtandem'}, {'msgf', 'xtandem', 'omssa'}]
    from http://stackoverflow.com/questions/464864/python-code-to-pick-out-all-possible-combinations-from-a-list
    '''
    out = [ set(compress(iterable,mask)) for mask in product(*[[0,1]]*len(iterable)) ]
    return out[1:]


def calc_FDR ( PSM_count, false_positives ):
    '''
    FDR Method 2 (Käll et al. 2008) as explained by Jones et al. 2009
    '''
    true_positives  = PSM_count - (2 * false_positives)
    if true_positives <= 0:  # prevent FDR above 1. Not sure if this is done?
        return 1.0
    FDR = false_positives / ( false_positives + true_positives)
    return FDR


def calc_FDR_score( e_value, gradient, intercept ):
    '''
    calculating the FDR Score according to Jones et al. 2009
    Algorithm 1.4.b.
    '''
    
    FDR_score = ( e_value * gradient ) + intercept
    
    return FDR_score



class MultiScorer(object):
    # attributes that are shared across all input CSV instances:
    csv_instances  = []  # list of existing class instances (one for each engine)
    AFS_lookup     = {}  # will store the average fdr score of each PSM
    summary_output = []  # will be populated with row_dicts
    known_engines = [
        "tandem", "omssa", "msgf", "msamanda", "myrimatch",
    ]
    unknown_engine_count = 0
    # if an engine name can't be identified from the input csv, it will be called "unknown_engine_{count}"

    def __init__( self, csv_path, info=None ):
        MultiScorer.csv_instances.append( self )  # add this class instance to the list of instances

        self.csv_path = csv_path

        if info == None:
            self.engine         = self.find_engine_name()
            self.engine_colname = self.engine
        else:
            self.engine         = info["engine_name"]
            self.engine_colname = info["engine_colname"]

        self.rowdict  = self.parse_csv()


    def parse_csv( self ):
        '''
        parses the input csv file and indexes it with PSM tuples
        returns a dict: { ('ASDF', 1234) : row, ... }
        '''
        
        # since we do not need all the column information later,
        # we will not store some information to save a bit of RAM:
        deletable_cols = ["PSM_ID","Pass Threshold"]
        
        fname = os.path.basename( self.csv_path )
        print('[{0:^22}] {1}'.format( self.engine.upper(), fname ))
        
        with open(self.csv_path, 'r') as csv_file:

            # skip csv comments / preamble:
            for line in csv_file:
                if not line.startswith('#'):
                    header = line.strip().split(',')
                    break

            reader = DictReader(csv_file, fieldnames=header)

            row_dict = {}
            
            for row in reader:

                # save some RAM
                for colname in deletable_cols:
                    if colname in row:
                        del row[ colname ]
                
                # only consider 'the best' PSM for each spectrum
                #if "rank" in row:
                    #if int(row["rank"]) != 1:
                        #continue
                # same effect as 'select-best-PSM.py' from msblender
                
                pep_sequence        = row[ 'Sequence' ]
                modifications       = row[ 'Modifications' ]
                spectrum_identifier = row[ 'Spectrum Title' ]

                # if 'decoy' in row['proteinacc_start_stop_pre_post_;'].lower():
                #     row['Is decoy'] = 'true'

                PSM_tuple        = ( pep_sequence, spectrum_identifier, modifications, row['Is decoy'] )
                row["PSM tuple"] = PSM_tuple
                row["Percolator:q-Value"] = row["q-value"]
                del row["q-value"]
                
                if PSM_tuple not in row_dict:
                    row_dict[ PSM_tuple ] = row
                else:
                    # if there are multiple PSMs with the same sequence and ID
                    # (i.e. different modifications), only the PSM with the lowest
                    # PEP is kept.
                    old_PEP = float( row_dict[ PSM_tuple ]["PEP"] )
                    new_PEP = float( row["PEP"] )
                    if new_PEP < old_PEP:
                        row_dict[ PSM_tuple ] = row

        return row_dict


    def find_engine_name( self ):
        ''' guess the engine name from its filename '''
        fname = os.path.split(self.csv_path)[-1]
        engine_name = False
        for string in MultiScorer.known_engines:
            if string in fname.lower():
                engine_name = string
        if not engine_name:
            MultiScorer.unknown_engine_count += 1
            engine_name = "unknown_engine_" + str(MultiScorer.unknown_engine_count)
        
        return engine_name

    @classmethod
    def _reset( cls ):
        '''
        cleanup after a single run... not sure why this is necessary
        '''
        cls.csv_instances  = []  # list of existing class instances (one for each engine)
        cls.AFS_lookup     = {}  # will store the average fdr score of each PSM
        cls.summary_output = []  # will be populated with row_dicts
        cls.known_engines = [
            "tandem", "omssa", "msgf", "msamanda", "myrimatch",
        ]
        cls.unknown_engine_count = 0


    @classmethod
    def get_AFS( cls, PSM_tuple, engine_scores ):
        '''
        returns the geometric average FDR or PEP.
        attempts to find this value in a lookup dict,
        if not present it will be calculated based on
        the scores of each engine (engine_scores)
        '''
        if PSM_tuple in cls.AFS_lookup:
            return cls.AFS_lookup[ PSM_tuple ]

        else:
            AFS = geometric_mean( *engine_scores )
            cls.AFS_lookup[ PSM_tuple ] = AFS
            return AFS


    @classmethod
    def get_shared_PSM_rowlist( cls, csv_instances, other_csv_instances ):

        PSM_tuple_sets = [ 
            set(eng.rowdict.keys()) for eng in csv_instances
        ]
        other_PSM_tuple_sets = [
            set(eng.rowdict.keys()) for eng in other_csv_instances
        ]

        engines_str = ";".join( sorted( {i.engine_colname for i in csv_instances} ) )
        shared_PSMs = set.intersection( *PSM_tuple_sets ).difference ( *other_PSM_tuple_sets )

        PSM_rowlist = []
        for PSM in shared_PSMs:

            PSM_scores = []
            PSM_decoy_bools = []
            
            potentially_conflicting_colnames = {
                "Retention Time (s)" : set(),
                "Charge"             : set(),
                #"Calc m/z"           : set(),
                #"Exp m/z"            : set(),
                #"Is decoy"           : set(),
            }

            for csv in csv_instances:
                csv_row = csv.rowdict[ PSM ]

                PSM_scores.append( float(csv_row[ 'FDR Score' ]) )  # FINALLY FIXED
                PSM_decoy_bools.append( csv_row[ 'Is decoy' ] )

                # debugging
                for k in potentially_conflicting_colnames.keys():
                    # try:
                    v = csv_row[ k ]
                    # except:
                    #     import pprint
                    #     pprint.pprint(csv_row)
                    #     print(k)
                    #     exit()
                    potentially_conflicting_colnames[k].add( v )
            
            # if one engine thinks a hit is decoy, it probably is...
            PSM_is_decoy = 'true' if 'true' in PSM_decoy_bools else 'false'

            row = {
               'PSM'      : PSM,
               'AFS'      : cls.get_AFS(PSM, PSM_scores),
               
               'Is decoy' : PSM_is_decoy,
               'Engines'  : engines_str,
               
               # debugging information, remove this later (TODO)
               '_individual_scores'      : PSM_scores,
               '_individual_decoy_bools' : PSM_decoy_bools,
            }
                
            for k,v in potentially_conflicting_colnames.items():
                if len(v) > 1:
                    print('[ Warning! ] Conflicting {0} column: {1}'.format( k, str(v) ) )
                # debugging
                row[k] = list(v)[0]
                

            PSM_rowlist.append( row )
    
        return PSM_rowlist


    @classmethod
    def add_estimated_FDR( cls, shared_PSMs ):
        '''
        Adding the estimated FDR (based on # of decoys).
        based on Jones et al. 2009: Algorithm 2, step 3
        careful, input file must be sorted by average score (low->high) already!
        '''
        
        # In certain datasets, decoy hits are not
        # observed at any score threshold for identifications made by all
        # three search engines. To correct for the size of the result set, an
        # artificial decoy hit is added at the end of each data series, such
        # that no identification has a combined FDR/PEP Score = 0.
        artificial_decoy = [ {'Is decoy' : 'true'} ]
        
        PSM_count = 0
        decoy_count = 0

        # Traverse identifications from lowest AFS to highest:
        for row in shared_PSMs + artificial_decoy:
            PSM_count += 1

            if row['Is decoy'] == 'true':
                decoy_count += 1

            # calculate and store the estimated FDR (FDRest) for each identification according to FDR Method 2.
            row['Estimated FDR']  = calc_FDR ( PSM_count, decoy_count )
            #row['_decoy_percent'] = decoy_count / PSM_count


    @classmethod
    def add_qvalues( cls, shared_PSMs ):
        '''
        Adding (engine-combination specific!) q-values (based on estimated FDR).
        based on Jones et al. 2009: Algorithm 2, step 4
        careful, input file must be sorted by average score (high->low) already!
        '''
    
        # 3) Traverse identifications from highest e-value to lowest, storing
        # the lowest estimated FDR (FDR min) that has been observed so far.
        FDRmin = float('inf')  # starts as infinity, ugly but works...
        for row in shared_PSMs:
            # a. For each identification, retrieve FDRest:
            FDRest = row['Estimated FDR']

            # i. If FDRest > FDR min, q-value = FDR min.
            if FDRest > FDRmin:
                q_value = FDRmin
            # ii. Else, q-value = FDRest and FDR min = FDRest.
            else:
                q_value = FDRest
                FDRmin = FDRest

            row['q-Value'] = q_value

    @classmethod
    def add_FDR_score( cls, idents ):
        # 4) Traverse the set of identifications from
        # lowest q-value to highest, identifying a set of step points, where
        # the q-value of the identification changes (q-value[i] > q-value[i-1] ).

        step_point_prev = ( 0.0, 0.0 )  # intercept is (0,0)
        intercept       =   0
        q_val_prev      = 0.0
        gradient        =   0

        for i, row in enumerate(idents):

            # a. At a step-point, calculate the intercept c and gradient g
            # between previous step-point[prev] (e-value[prev], q-value[prev]) and
            # current step-point[curr] (e-value[curr], q-value[curr] ).
            # Since we don't have q-values in out output, we use the percolator PEP
            # instead. It's only used for ordering, so any quality measure should
            # be fine!
            e_val = float( row['PEP'] )
            q_val = float( row['q-Value'] )

            # check if we are currently at a step-point! otherwise keep previous gradient
            # or if we reached the end of the file, this also counts as a step point...
            if q_val != q_val_prev or i == len(idents)-1:
                step_point_curr = ( e_val, q_val )
                
                intercept, gradient = calc_intercept_and_slope( step_point_prev, step_point_curr )

                # we found a new step point and calculated its gradient and intecept,
                # so let's enter the FDR Score for all PSMs between this step point and the previous one!
                # looping backwards and entering FDR Score until we reach the previous step point...
                pos = 0
                while i-pos >= 0:
                    earlier_row = idents[i-pos]
                    if "FDR Score" in earlier_row.keys():
                        # FDR Score is already entered, so we must have reached an 'old' step point
                        break
                    
                    PSM_e_val = float( earlier_row['PEP'] )
                    combined_score = calc_FDR_score ( PSM_e_val, gradient, intercept )
                    earlier_row[ "FDR Score" ] = combined_score
                    
                    pos += 1

                # in the next iteration, this will be the previous step point
                step_point_prev = step_point_curr

            q_val_prev = q_val


    @classmethod
    def add_combined_FDR_score( cls, shared_PSMs ):
        # 4) Traverse the set of identifications from
        # lowest q-value to highest, identifying a set of step points, where
        # the q-value of the identification changes (q-value[i] > q-value[i-1] ).

        qval_sorted_csv = sorted(shared_PSMs,
                key=lambda x: (float(x['q-Value']), x['AFS']) ) # sort csv by q-value (AFS if ties)

        step_point_prev = ( 0.0, 0.0 )  # intercept is (0,0)
        intercept       =   0
        q_val_prev      = 0.0
        gradient        =   0

        for i, row in enumerate(qval_sorted_csv):

            # a. At a step-point, calculate the intercept c and gradient g
            # between previous step-point[prev] (e-value[prev], q-value[prev]) and
            # current step-point[curr] (e-value[curr], q-value[curr] ).
            e_val = float( row['AFS'] )
            q_val = float( row['q-Value'] )

            # check if we are currently at a step-point! otherwise keep previous gradient
            # or if we reached the end of the file, this also counts as a step point...
            if q_val != q_val_prev or i == len(qval_sorted_csv)-1:
                step_point_curr = ( e_val, q_val )
                
                intercept, gradient = calc_intercept_and_slope( step_point_prev, step_point_curr )

                # we found a new step point and calculated its gradient and intecept,
                # so let's enter the FDR/PEP Score for all PSMs between this step point and the previous one!
                # looping backwards and entering FDR/PEP Score until we reach the previous step point...
                pos = 0
                while i-pos >= 0:
                    earlier_row = qval_sorted_csv[i-pos]
                    if 'Combined FDR Score' in earlier_row.keys():
                        # combined PEP score is already entered, so we must have reached an 'old' step point
                        break
                    
                    PSM_e_val = float( earlier_row['AFS'] )
                    combined_score = calc_FDR_score ( PSM_e_val, gradient, intercept )
                    earlier_row[ 'Combined FDR Score' ] = combined_score
                    
                    if earlier_row['Is decoy'] == 'false':
                        cls.current_stats['PSM_count'] += 1
                        if earlier_row['Combined FDR Score'] < cls.cutoff:
                            cls.current_stats['passed_count'] += 1
                        #if earlier_row['AFS'] < cls.cutoff:
                            #cls.current_stats['percolator_passed_count'] += 1
                    
                    cls.summary_output.append( earlier_row )

                    pos += 1

                # in the next iteration, this will be the previous step point
                step_point_prev = step_point_curr

            q_val_prev = q_val


    @classmethod
    def current_engine_combination_status_str( cls, used_engines, other_engines ):
        
        engines_string = ' and '.join( [i.engine for i in used_engines] )
        other_engines_string = ' or '.join( [i.engine for i in other_engines] )
        
        if len(other_engines) == 0:
            return 'Scoring PSMs that were identified by all {0} engines...'.format( len(used_engines) )
        else:
            return 'Scoring PSMs that were identified by {0}, but not by {1}...'.format( engines_string, other_engines_string )


    @classmethod
    def print_PSM_threshold_stats( cls ):
        d = cls.current_stats
        if d['PSM_count'] == 0:  # preventing division by 0 errors
            d['pass_fraction']            = 0
            #d['percolator_pass_fraction'] = 0
        else:
            d['pass_fraction']            = (d['passed_count'] / d['PSM_count'])
            #d['percolator_pass_fraction'] = (d['percolator_passed_count'] / d['PSM_count'])
        d['threshold']                    = cls.cutoff
        d['score']                        = 'Combined FDR Score'
        
        s1 = '{pass_fraction:>6.1%} of target PSMs are below {threshold:.1%} {score}.   ({passed_count:>6} /{PSM_count:>7})\n'
        #s2 = '{percolator_pass_fraction:>6.1%} of target PSMs are below {threshold:.1%} mean Percolator PEP.  ({percolator_passed_count:>6} /{PSM_count:>7})\n'
        print( s1.format( **d ) )
        #print( s2.format( **d ) )


    @classmethod
    def write_summary_csv( cls, full_file_path ):

        print( 'Writing summary CSV...' )
        
        all_PSMs = cls.AFS_lookup.keys()
        #header   = ['Raw data location', 'Spectrum ID', 'Charge', 'Sequence', 'proteinacc_start_stop_pre_post_;', 'Is decoy', 'Combined PEP Score', '_individual_decoy_bools', '_individual_scores']
        header_start = [
            'Raw data location', # new
            'Spectrum ID',
            'Spectrum Title', # new
            'Retention Time (s)',
            'Calc m/z', # new
            'Exp m/z', # new
            'Charge',
            'Sequence', 
            'Modifications',
            'Engines',
            'Combined FDR Score', 
            'Average FDR Score',
        ]
        header_end = [
            'Is decoy',
            'Protein ID'
        ]
        header_center = []
        for instance in cls.csv_instances:
            header_center.append( instance.engine_colname + ':PEP' )
            header_center.append( instance.engine_colname + ':FDR' )

        header = header_start + header_center + header_end
        
        output_row_list = []
        
        for raw_row in cls.summary_output:
            # decoys and hits above cutoff are filtered out, if desired
            if cls.filter_cutoff and float(raw_row[ 'Combined FDR Score' ]) > cls.cutoff:
                continue
            if cls.filter_decoys and raw_row['Is decoy'] == 'true':
                continue
            
            PSM = raw_row['PSM']
            row = {}
            
            for key in header:
                if key in raw_row:
                    row[key] = raw_row[key]
            row['Average FDR Score'] = raw_row['AFS']
            #row['q_value']           = raw_row['q-Value']
            #row['fdr_est']           = raw_row['Estimated FDR']

            for instance in cls.csv_instances:
                if PSM in instance.rowdict:
                    row[ instance.engine_colname + ':PEP'] = instance.rowdict[PSM]['PEP']
                    row[ instance.engine_colname + ':FDR'] = instance.rowdict[PSM]['Estimated FDR']
                    for key in header:
                        if key in instance.rowdict[PSM]:
                            row[key] = instance.rowdict[PSM][key]

            output_row_list.append( row )

        # sorting the output csv by quality and then dumping it in a file:
        sorted_output_row_list = sorted(
            output_row_list,
            key = lambda x: ( float(x['Combined FDR Score']), float(x['Average FDR Score']) )
            )
        with open(full_file_path, 'w', newline='') as output_file:
            dict_writer = DictWriter( output_file, header )
            dict_writer.writeheader()
            for output_row in sorted_output_row_list:
                dict_writer.writerow( output_row )

        print( 'Wrote summary CSV to {}\n'.format( full_file_path ) )
        return full_file_path


def main(
    input_file_list,
    directory,
    cutoff          = 0.01,
    file_info       = None,
    output_filename = None,
    filter_decoys   = True,
    filter_cutoff   = True,
    label           = "",
        ):
    
    print( "Parsing CSV files:" )
    
    for csv_path in input_file_list:
        if file_info == None:
            # if no info is provided, engine name and label name will be guessed from the file name
            MultiScorer( csv_path )
        else:
            MultiScorer( csv_path, info = file_info[ csv_path ] )

    MultiScorer.cutoff        = cutoff
    MultiScorer.filter_decoys = filter_decoys
    MultiScorer.filter_cutoff = filter_cutoff
    
    print()

    # algorithm 1 from Jones et al. (2009):
    # for each ident CSV, calculating the FDR Score for each PSM
    for csv_instance in MultiScorer.csv_instances:
        ident_csv_unsorted = list( csv_instance.rowdict.values() )
        ident_csv = sorted(
            ident_csv_unsorted,
            key=lambda x: ( float(x['PEP']), float(x['Percolator:q-Value']) )
        )

        MultiScorer.add_estimated_FDR( ident_csv )
        MultiScorer.add_qvalues( reversed(ident_csv) )
        MultiScorer.add_FDR_score( ident_csv )

        # we calculated FDR Scores, so let's add them to the CSV's rowdict!
        for row in ident_csv:
            csv_instance.rowdict[ row['PSM tuple'] ]['FDR Score'] = \
                row['FDR Score']
                
    
    # algorithm 2 from Jones et al. (2009):
    # re-calculating the FDR-scores for each set of identifications that
    # was made by a particular combination of search engines:
    for engine_combo in all_combinations( MultiScorer.csv_instances ):
        other_engines = [i for i in MultiScorer.csv_instances if i not in engine_combo]
        
        MultiScorer.current_stats  = {     # reset stats counter for the current engine combination...
            'PSM_count'              : 0,
            'passed_count'           : 0,  # how many PSMs passed our combined FDR threshold
            #'percolator_passed_count': 0,  # how many PSMs passed the input percolator PEP threshold
        }  
        
        # printing i.e. 'Scoring PSMs that were identified by omssa & msgf, but not by xtandem...'
        status_string = MultiScorer.current_engine_combination_status_str( engine_combo, other_engines )
        print( status_string, end='\r' )
        
        # peptide identifications made by a particular combination of search engines:
        shared_PSMs_unordered = MultiScorer.get_shared_PSM_rowlist( engine_combo, other_engines )
        
        # Order identifications according to AFS (= geometric mean fdr score) within that set:
        shared_PSMs = sorted(shared_PSMs_unordered, key=lambda x: float(x['AFS']) )
        
        MultiScorer.add_estimated_FDR( shared_PSMs )
        MultiScorer.add_qvalues( reversed(shared_PSMs) )
        MultiScorer.add_combined_FDR_score( shared_PSMs )
        
        print( status_string + ' done!' )
        
        MultiScorer.print_PSM_threshold_stats()


    if output_filename == None:
        output_filename = 'combined_FDR_summary_{0}.csv'.format( label )
    else:
        # make sure we don't add the directory twice
        output_filename = os.path.basename( output_filename )

    full_file_path = os.path.join(directory, output_filename )
    summary_csv = MultiScorer.write_summary_csv( full_file_path )
    
    MultiScorer._reset()  # cleaning up previous csv instances
    
    return summary_csv


if __name__ == '__main__':
    
    # parsing command line arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument('directory',
        help='the directory in which to look for \'*complete_v.csv\'-files')
    parser.add_argument('-C', '--cutoff', default=0.01,
        help='the desired combined FDR cutoff, as a fraction', type=float)
    parser.add_argument('-L', '--label',
        help='a substring that allows label identification from the csv file name')
    args = parser.parse_args()

    input_file_list = []
    found_csv = False
    for csv_path in glob.glob(os.path.join(args.directory, '*complete_v.csv')):
        if args.label in os.path.split(csv_path)[-1]:
            input_file_list.append( csv_path )
            found_csv = True
    if not found_csv:
        print( 'Error: No CSV file that ends in \'*complete_v.csv\' and contains label identifier \'{0}\' was found in directory \'{1}\'.'.format(args.label, args.directory) )
