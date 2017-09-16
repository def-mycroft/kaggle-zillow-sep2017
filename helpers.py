"""Helpers for general data analysis"""
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind as t_test
import sqlite3
db_path = r"C:\Users\dasen\Google Drive\SYNC TO PC\data998_database.sqlite3"


def inspect_database(filepath=db_path):
    """Returns list of tables in the database"""
    conn = sqlite3.connect(filepath)
    cur = conn.cursor()
    output = cur.execute("select name from sqlite_master where type='table'").fetchall()
    conn.close()
    return output

def query_database(query, filepath=db_path):
    """Returns a dataframe based on sql query"""
    conn = sqlite3.connect(filepath)
    cur = conn.cursor()
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def view_table_cols(table, filepath=db_path):
    """Allows view of columns within specific table"""
    conn = sqlite3.connect(filepath)
    cur = conn.execute('select * from %s' % table)
    return list(map(lambda x: x[0], cur.description))

def nan_summary(df, columns, return_dict=False, display=True):
    """Given a df and list of cols, display missing value stats"""
    output = dict()
    len_entire = len(df)
    print('length of entire df: %s' % len_entire) # length of entire df
    for column in columns:
        len_notnull = len(df[df[column].notnull()])
        fraction_null = (len_entire - len_notnull) / (len_entire) * 100
        fraction_null = round(fraction_null, 2)
        output[column] = fraction_null
        msg = '%s percent null in %s (%s notnull)' % (
                fraction_null,
                column,
                len_notnull)
        if display:
            print(msg)

    if return_dict:
        return output

def my_t_test(a, b, a_label='a', b_label='b'):
    """Given two array-like objects, calculates the P-Value"""
    p_value = t_test(a, b)[1]
    mean_a = round(a.mean(),2)
    mean_b = round(b.mean(),2)
    p_value = round(p_value, 4)
    if p_value < 0.05:
        print('The difference is statistically significant. p =', p_value)
        print('Mean of array "%s": %s. N=%s' % (a_label, mean_a, len(a)))
        print('Mean of array "%s": %s. N=%s' % (b_label, mean_b, len(b)))
    else:
        print('Cannot reject the null hypothesis. p =', p_value)
        print('Mean of array "%s": %s. N=%s' % (a_label, mean_a, len(a)))
        print('Mean of array "%s": %s. N=%s' % (b_label, mean_b, len(b)))
