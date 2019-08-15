#!/usr/bin/env python3
import ursgal
import pandas as pd
import click


@click.command()
@click.argument('peptide', nargs=1) #, description="Peptide in with unimod format, e.g. PENNER#TMTplex6:6")
def main(peptide):
    """Example script for the ursgal peptide fragmentor

    required argument is PEPTIDE with optional unimod modification, e.g.:

    python fragment_peptide.py REALLY#TMTplex6:6
    """
    pd.set_option('display.max_columns', 500)
    pd.set_option('display.max_row', 5000)

    fragger = ursgal.upepfragger.UPeptideFragmentor(peptide)
    df = fragger.df
    print(df.head(10))
    print(df.describe())
    df_by = df[df['series'].isin(['b', 'y'])]
    print(df_by[['name', 'modstring', 'mz']].sort_values('mz').head(1000))


if __name__ == '__main__':
    main()

