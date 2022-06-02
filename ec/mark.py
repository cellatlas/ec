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
  non_repeat_genes = dfc['name'].value_counts()[dfc['name'].value_counts() < gs].index.values
  
  # remove repeated genes, sort by effect size
  m = dfc[dfc.name.isin(non_repeat_genes)].sort_values('es', ascending = False)
  
  # get number of genes per cell type to extract
  n_sample = m["group_id"].value_counts().min()
  
  # extract markers with highet effect size
  markers = m.groupby('group_id').tail(n_sample)
  
  # make dictionary
  markers_dict = markers.groupby("group_id")["name"].apply(lambda x: list(x)).to_dict()
  
  # write dictionary
  write_markers(output_fname, markers_dict)

  
