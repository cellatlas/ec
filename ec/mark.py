#!/usr/bin/env python3

import pandas as pd
from ec.utils import write_markers


def ec_mark(mp, mfc, gs, output_fname, deg_fname):
  # column names
  pval_col_name = 'p_corr'
  fc_col_name = 'log_fc'
  
  # read dataframe
  df = pd.read_csv(deg_fname, sep = '\t')
  
  # filter by criteria
  dfc = df.query(f"{pval_col_name} <= {mp} & {fc_col_name} >= {mfc}")
  
  # mask out genes that are shared between max_gene_shares cell type
  non_repeat_genes = dfc['target'].value_counts()[dfc['target'].value_counts() < gs].index.values
  
  # remove repeated genes, sort by effect size
  m = dfc[dfc.target.isin(non_repeat_genes)].sort_values(fc_col_name, ascending = False)
  
  # get number of genes per cell type to extract
  n_sample = m["group"].value_counts().min()
  
  # extract markers with highet effect size
  markers = m.groupby('group').tail(n_sample)
  
  # make dictionary
  markers_dict = markers.groupby("group")["target"].apply(lambda x: list(x)).to_dict()
  
  # write dictionary
  write_markers(output_fname, markers_dict)

  
