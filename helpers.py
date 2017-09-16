"""Helpers for general data analysis"""
import pandas as pd
import numpy as np
from matplotlib import pyplot
from tkinter import Tk
from scipy.stats import ttest_ind as t_test
import sqlite3
db_path = "C:/Users/dasenbrock/OneDrive - CivicPlus/Chaotic/my_database.sqlite3"
wfh_db_path = "C:/Users/dasen/Documents/my_database.sqlite3"
wfh_out_path = "C:/Users/dasen/Documents/"
wfh_downloads = "C:/Users/dasen/Downloads/"

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

def create_url(internal_id):
    """Creates a url given a client id"""
    return r'https://system.netsuite.com/app/common/entity/custjob.nl?id=%s' % internal_id

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

def create_bar_charts(df, group_column, sum_column, filepath='', size=20):
    """Create bar charts summing a value by a column"""
    group_object = pd.DataFrame(df.groupby([group_column])[sum_column].sum())
    group_object.plot(
        kind='bar', figsize=(size,size*0.5))
    # Graph title
    graph_title = 'sum of %s grouped by %s' % (sum_column, group_column)
    pyplot.suptitle(
        graph_title, x=0.5, y=0.92, ha='center', fontsize='xx-large')

    filepath += '%s-%s.png' % (sum_column, group_column)
    pyplot.savefig(filepath)
    pyplot.close()
    filepath = filepath[:-4] + '.csv'
    group_object.to_csv(filepath)

def string_to_clipboard(string):
    """Puts a string on the system clipboard"""
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(string)
    r.update()
    r.destroy()

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
