import ursgal
import sys

if __name__ == "__main__":
    uc = ursgal.UController(verbose=False)

    uc.params['reporter_ion_tolerance'] = 0.002
    uc.params['reporter_ion_tolerance_unit'] = 'da'

    # specify names and masses of isobaric reporters
    reporters = {
        '126'  : 126.127726,
        '127L' : 127.124761,
        '127H' : 127.131081,
        '128L' : 128.128116,
        '128H' : 128.134436,
        '129L' : 129.131471,
        '129H' : 129.137790,
        '130L' : 130.134825,
        '130H' : 130.141145,
        '131L' : 131.138180,
        '131H' : 131.144499,
    }
    uc.params['reporter_ion_mzs'] = reporters

    uc.execute_misc_engine(
        sys.argv[1],
        engine="TMT_quant_1_0_0",
        force=True,
    )