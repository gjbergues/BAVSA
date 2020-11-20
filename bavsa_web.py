import pandas as pd
import numpy as np
import sys
from shutil import copyfile


def pivot_ofv(df, index_val):
    # Pivot table
    table_cpd_monto = df.pivot_table(index=index_val, columns=['PPV'], values='Monto')
    table_cpd_monto.columns.name = None
    # Create table1 for saving the values "Monto"
    table1 = table_cpd_monto.replace('nan', 0, regex=True)
    table_cpd_monto = ppv_columns(table_cpd_monto)
    # ##############################################################################################
    # Create pivot table2 with values "Of.V"
    # ######################################
    table2 = df.pivot_table(index=index_val, columns=['PPV'], values='Of.V.')
    table2.columns.name = None
    table2 = table2.replace('nan', 0, regex=True)

    # ##############################################################################################
    # Create pivot table OUT, product between two tables
    # ##################################################

    # Product Monto*Tasa
    table_out = table1.mul(table2, fill_value=0)
    table_out = ppv_columns(table_out)

    # Transform to numeric values
    table_cpd_monto = table_cpd_monto.astype(str).astype(float)
    table_out = table_out.astype(str).astype(float)

    # Calculate weighted average
    table_cpd = table_out.div(table_cpd_monto).replace(np.nan, '_').reset_index()
    return table_cpd


def empty_function(name):
    with open('tables/empty_table.html', 'r') as f:
        new_html = str(f.read())
    path = 'tables/' + name + '.html'
    with open(path, 'w') as f:
        f.write(new_html)
    # Add table to bavsa web
    TABLA = '@TABLA_' + name
    create_html_bavsa(name, TABLA)


def no_garantizado(data):
    # ##################################################################################
    # ############################# NEGOCIADA #########################################
    # ##################################################################################

    df = data.query('Segmento == "No Garantizado"')
    df = df.query('Estado == ["Negociada"]')
    df = df.rename(columns={'SGR / Librador': 'Librador'})
    if df.empty:
        path = 'tables/empty_table.html'
        with open(path, 'r') as f:
            new_html = str(f.read())

        table_list = ['negociada_NG_CPD.html', 'negociada_NG_ECHEQ.html', 'negociada_NG_FCE.html',
                      'negociada_NG_PAGARE.html', 'negociada_NG_TODOS.html']

        for name in table_list:
            path = 'tables/' + name
            with open(path, 'w') as f:
                f.write(new_html)
        # Add table to bavsa web
        create_html_bavsa('negociada_NG_CPD', '@TABLA_negociada_NG_CPD')
        create_html_bavsa('negociada_NG_ECHEQ', '@TABLA_negociada_NG_ECHEQ')
        create_html_bavsa('negociada_NG_FCE', '@TABLA_negociada_NG_FCE')
        create_html_bavsa('negociada_NG_PAGARE', '@TABLA_negociada_NG_PAGARE')
        create_html_bavsa('negociada_NG_TODOS', '@TABLA_negociada_NG_TODOS')
    else:
        # ##################################################################################
        # #################### Librador - PPV - Of. V. - Tipo=CPD ######################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        # Put the table in function of CPD
        df2 = df.query('Tipo == ["CPD"]')

        if df2.empty:
            empty_function('negociada_NG_CPD')
        else:
            # Pivot table
            table_cpd = pivot_ofv(df2, 'Librador')

            # Table to html
            table_cpd.to_html('tables/negociada_NG_CPD.html')
            # Add table to bavsa web
            create_html_bavsa('negociada_NG_CPD', '@TABLA_negociada_NG_CPD')

        # ##################################################################################
        # #################### Librador - PPV - Of. V. - Tipo=ECHEQ ######################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        # Put the table in function of CPD
        df2 = df.query('Tipo == ["ECHEQ"]')

        if df2.empty:
            empty_function('negociada_NG_ECHEQ')
        else:
            # Pivot table
            table_echeq = pivot_ofv(df2, 'Librador')

            # Table to html
            table_echeq.to_html('tables/negociada_NG_ECHEQ.html')
            # Add table to bavsa web
            create_html_bavsa('negociada_NG_ECHEQ', '@TABLA_negociada_NG_ECHEQ')

        # ##################################################################################
        # #################### Librador - PPV - Of. V. - Tipo=FCE ######################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        # Put the table in function of CPD
        df2 = df.query('Tipo == ["FCE"]')

        if df2.empty:
            empty_function('negociada_NG_FCE')
        else:
            # Pivot table
            table_fce = pivot_ofv(df2, 'Librador')

            # Table to html
            table_fce.to_html('tables/negociada_NG_FCE.html')
            # Add table to bavsa web
            create_html_bavsa('negociada_NG_FCE', '@TABLA_negociada_NG_FCE')

        # ##################################################################################
        # #################### Librador - PPV - Of. V. - Tipo=PAGARE ######################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        # Put the table in function of PAGARE
        df2 = df.query('Tipo == ["PAGARE"]')

        if df2.empty:
            empty_function('negociada_NG_PAGARE')
        else:
            # Pivot table
            table_pag = pivot_ofv(df2, 'Librador')

            # Table to html
            table_pag.to_html('tables/negociada_NG_PAGARE.html')
            # Add table to bavsa web
            create_html_bavsa('negociada_NG_PAGARE', '@TABLA_negociada_NG_PAGARE')

        # ##################################################################################
        # #################### librador - PPV - Of. V. - Tipo = TODOS  #################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        if df.empty:
            empty_function('negociada_NG_TODOS')
        else:
            # Pivot table
            table_todos = pivot_ofv(df, 'Librador')

            # Table to html
            table_todos.to_html('tables/negociada_NG_TODOS.html')
            # Add table to bavsa web
            create_html_bavsa('negociada_NG_TODOS', '@TABLA_negociada_NG_TODOS')

    # ##################################################################################
    # ############################# DESIERTA #########################################
    # ##################################################################################

    df = data.query('Segmento == "No Garantizado"')
    df = df.query('Estado == ["Desierta"]')
    df = df.rename(columns={'SGR / Librador': 'Librador'})
    if df.empty:
        path = 'tables/empty_table.html'
        with open(path, 'r') as f:
            new_html = str(f.read())

        table_list = ['desierta_NG_CPD.html', 'desierta_NG_ECHEQ.html',
                      'desierta_NG_PAGARE.html', 'desierta_NG_TODOS.html']

        for name in table_list:
            path = 'tables/' + name
            with open(path, 'w') as f:
                f.write(new_html)
        # Add table to bavsa web
        create_html_bavsa('desierta_NG_CPD', '@TABLA_desierta_NG_CPD')
        create_html_bavsa('desierta_NG_ECHEQ', '@TABLA_desierta_NG_ECHEQ')
        create_html_bavsa('desierta_NG_PAGARE', '@TABLA_desierta_NG_PAGARE')
        create_html_bavsa('desierta_NG_TODOS', '@TABLA_desierta_NG_TODOS')
    else:
        # ##################################################################################
        # #################### Librador - PPV - Of. V. - Tipo=CPD ######################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        # Put the table in function of CPD
        df2 = df.query('Tipo == ["CPD"]')

        if df2.empty:
            empty_function('desierta_NG_CPD')
        else:
            # Pivot table
            table_cpd = pivot_ofv(df2, 'Librador')

            # Table to html
            table_cpd.to_html('tables/desierta_NG_CPD.html')
            # Add table to bavsa web
            create_html_bavsa('desierta_NG_CPD', '@TABLA_desierta_NG_CPD')

        # ##################################################################################
        # #################### Librador - PPV - Of. V. - Tipo=ECHEQ ######################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        # Put the table in function of ECHEQ
        df2 = df.query('Tipo == ["ECHEQ"]')

        if df2.empty:
            empty_function('desierta_NG_ECHEQ')
        else:
            # Pivot table
            table_echeq = pivot_ofv(df2, 'Librador')

            # Table to html
            table_echeq.to_html('tables/desierta_NG_ECHEQ.html')
            # Add table to bavsa web
            create_html_bavsa('desierta_NG_ECHEQ', '@TABLA_desierta_NG_ECHEQ')

        # ##################################################################################
        # #################### Librador - PPV - Of. V. - Tipo=PAGARE ######################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        df2 = df.query('Tipo == ["PAGARE"]')
        table_pag_monto = df2.pivot_table(index='Librador', columns=['PPV'], values='Monto')

        if table_pag_monto.empty:
            empty_function('desierta_NG_PAGARE')
        else:
            # Pivot table
            table_pag = pivot_ofv(df2, 'Librador')

            # Table to html
            table_pag.to_html('tables/desierta_NG_PAGARE.html')
            # Add table to bavsa web
            create_html_bavsa('desierta_NG_PAGARE', '@TABLA_desierta_NG_PAGARE')

        # ##################################################################################
        # #################### librador - PPV - Of. V. - Tipo = TODOS  #################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        if df.empty:
            empty_function('desierta_NG_TODOS')
        else:
            # Pivot table
            table_todos = pivot_ofv(df, 'Librador')

            # Table to html
            table_todos.to_html('tables/desierta_NG_TODOS.html')
            # Add table to bavsa web
            create_html_bavsa('desierta_NG_TODOS', '@TABLA_desierta_NG_TODOS')


def no_Garantizado_epyme(data):
    # ##################################################################################
    # ############################# NEGOCIADA #########################################
    # ##################################################################################

    df = data.query('Segmento == "No Garantizado E.PYME"')
    df = df.query('Estado == ["Negociada"]')
    df = df.rename(columns={'SGR / Librador': 'Librador'})
    if df.empty:
        path = 'tables/empty_table.html'
        with open(path, 'r') as f:
            new_html = str(f.read())

        table_list = ['negociada_NGE_CPD.html', 'negociada_NGE_ECHEQ.html',
                      'negociada_NGE_PAGARE.html', 'negociada_NGE_TODOS.html']

        for name in table_list:
            path = 'tables/' + name
            with open(path, 'w') as f:
                f.write(new_html)
        # Add table to bavsa web
        create_html_bavsa('negociada_NGE_CPD', '@TABLA_negociada_NGE_CPD')
        create_html_bavsa('negociada_NGE_ECHEQ', '@TABLA_negociada_NGE_ECHEQ')
        create_html_bavsa('negociada_NGE_TODOS', '@TABLA_negociada_NGE_TODOS')
    else:
        # ##################################################################################
        # #################### Librador - PPV - Of. V. - Tipo=CPD ######################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        # Put the table in function of CPD
        df2 = df.query('Tipo == ["CPD"]')
        if df2.empty:
            empty_function('negociada_NGE_CPD')
        else:
            # Pivot table
            table_cpd = pivot_ofv(df2, 'Librador')

            # Table to html
            table_cpd.to_html('tables/negociada_NGE_CPD.html')
            # Add table to bavsa web
            create_html_bavsa('negociada_NGE_CPD', '@TABLA_negociada_NGE_CPD')

        # ##################################################################################
        # #################### Librador - PPV - Of. V. - Tipo=ECHEQ ######################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        # Put the table in function of CPD
        df2 = df.query('Tipo == ["ECHEQ"]')
        if df2.empty:
            empty_function('negociada_NGE_ECHEQ')
        else:
            # Pivot table
            table_echeq = pivot_ofv(df2, 'Librador')

            # Table to html
            table_echeq.to_html('tables/negociada_NGE_ECHEQ.html')
            # Add table to bavsa web
            create_html_bavsa('negociada_NGE_ECHEQ', '@TABLA_negociada_NGE_ECHEQ')

        # ##################################################################################
        # #################### librador - PPV - Of. V. - Tipo = TODOS  #################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        if df.empty:
            empty_function('negociada_NGE_TODOS')
        else:
            # Pivot table
            table_todos = pivot_ofv(df2, 'Librador')

            # Table to html
            table_todos.to_html('tables/negociada_NGE_TODOS.html')
            # Add table to bavsa web
            create_html_bavsa('negociada_NGE_TODOS', '@TABLA_negociada_NGE_TODOS')

    # ##################################################################################
    # ############################# DESIERTA #########################################
    # ##################################################################################

    df = data.query('Segmento == "No Garantizado E.PYME"')
    df = df.query('Estado == ["Desierta"]')
    df = df.rename(columns={'SGR / Librador': 'Librador'})
    if df.empty:
        path = 'tables/empty_table.html'
        with open(path, 'r') as f:
            new_html = str(f.read())

        table_list = ['desierta_NGE_CPD.html', 'desierta_NGE_ECHEQ.html', 'desierta_NGE_TODOS.html']

        for name in table_list:
            path = 'tables/' + name
            with open(path, 'w') as f:
                f.write(new_html)
        # Add table to bavsa web
        create_html_bavsa('desierta_NGE_CPD', '@TABLA_desierta_NGE_CPD')
        create_html_bavsa('desierta_NGE_ECHEQ', '@TABLA_desierta_NGE_ECHEQ')
        create_html_bavsa('desierta_NGE_TODOS', '@TABLA_desierta_NGE_TODOS')
    else:
        # ##################################################################################
        # #################### Librador - PPV - Of. V. - Tipo=CPD ######################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        # Put the table in function of CPD
        df2 = df.query('Tipo == ["CPD"]')

        if df2.empty:
            empty_function('desierta_NGE_CPD')
        else:
            # Pivot table
            table_cpd = pivot_ofv(df2, 'Librador')

            # Table to html
            table_cpd.to_html('tables/desierta_NGE_CPD.html')
            # Add table to bavsa web
            create_html_bavsa('desierta_NGE_CPD', '@TABLA_desierta_NGE_CPD')

        # ##################################################################################
        # #################### Librador - PPV - Of. V. - Tipo=ECHEQ ######################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################

        # Put the table in function of CPD
        df2 = df.query('Tipo == ["ECHEQ"]')
        if df2.empty:
            empty_function('desierta_NGE_ECHEQ')
        else:
            # Pivot table
            table_echeq = pivot_ofv(df2, 'Librador')

            # Table to html
            table_echeq.to_html('tables/desierta_NGE_ECHEQ.html')
            # Add table to bavsa web
            create_html_bavsa('desierta_NGE_ECHEQ', '@TABLA_desierta_NGE_ECHEQ')

        # ##################################################################################
        # #################### librador - PPV - Of. V. - Tipo = TODOS  #################
        # ##################################################################################

        # #####################################################################
        # Create pivot table Monto
        # ########################
        if df.empty:
            empty_function('desierta_NGE_TODOS')
        else:
            # Pivot table
            table_todos = pivot_ofv(df2, 'Librador')

            # Table to html
            table_todos.to_html('tables/desierta_NGE_TODOS.html')
            # Add table to bavsa web
            create_html_bavsa('desierta_NGE_TODOS', '@TABLA_desierta_NGE_TODOS')


def ppv_columns(table):
    # PPV columns (days)
    ppv_cpd = table.columns.values
    # PPV per month from 1 to 50 months
    months = np.arange(start=1, stop=1500, step=30)

    # Obtain the PPV range (a) per month
    for x in months:
        y = x + 29
        if x < 360:
            vars()['days_' + str(x) + '_' + str(y)] = np.where(np.logical_and(ppv_cpd >= x, ppv_cpd <= y))

    days_m366 = np.where(np.logical_and(ppv_cpd >= 366, ppv_cpd <= 1500))  # EXTRA line-> If (PPV > 365)

    # Insert new columns with the mean of PPV range
    for x in months:
        y = x + 29
        if x < 360:
            name = vars()['days_' + str(x) + '_' + str(y)]
            try:
                vars()['col_' + str(x) + '_' + str(y)] = table.iloc[:, np.amin(name):(np.amax(name)+1)]
                insert = str(x) + '_' + str(y)
                # Insert column
                table[insert] = vars()['col_' + str(x) + '_' + str(y)].mean(axis=1, skipna=np.nan).\
                    apply(lambda k: '%.2f' % k)
            except ValueError:
                pass

    col_m366 = table.iloc[:, days_m366[0]]  # EXTRA line->  If (PPV > 365)
    table['>365'] = col_m366.sum(axis=1, skipna=np.nan).apply(lambda k: '%.2f' % k)

    # Erase old PPV columns per days
    eliminate = np.arange(start=0, stop=len(ppv_cpd), step=1)
    table.drop(table.columns[eliminate], axis=1, inplace=True)
    return table


def negociada(data):
    # ##################################################################################
    # ############################# NEGOCIADA #########################################
    # ##################################################################################

    df = data.query('Estado == ["Negociada"]')
    # ##################################################################################
    # #################### Razón Social - PPV - Of. V. - Tipo=CPD ######################
    # ##################################################################################

    # #####################################################################
    # Create pivot table Monto
    # ########################

    # Put the table in function of CPD
    df2 = df.query('Tipo == ["CPD"]')

    # Pivot table
    table_cpd = pivot_ofv(df2, 'Razón Social de la SGR')

    # Table to html
    table_cpd.to_html('tables/negociada_CPD.html')
    # Add table to bavsa web
    create_html_bavsa('negociada_CPD', '@TABLA_negociada_CPD')
    # ##################################################################################
    # #################### Razón Social - PPV - Of. V. - Tipo=ECHEQ ####################
    # ##################################################################################

    # #####################################################################
    # Create pivot table Monto
    # ########################

    # Put the table in function of ECHEQ
    df3 = df.query('Tipo == ["ECHEQ"]')

    # Pivot table
    table_echeq = pivot_ofv(df3, 'Razón Social de la SGR')

    # Table to html
    table_echeq.to_html('tables/negociada_ECHEQ.html')
    # Add table to bavsa web
    create_html_bavsa('negociada_ECHEQ', '@TABLA_negociada_ECHEQ')
    # ##################################################################################
    # #################### Razón Social - PPV - Of. V. - Tipo=PAGARE ####################
    # ##################################################################################

    # #####################################################################
    # Create pivot table Monto
    # ########################

    # Put the table in function of PAGARE
    df4 = df.query('Tipo == ["PAGARE"]')

    if df4.empty:
        empty_function('negociada_PAGARE')
    else:
        # Pivot table
        table_pag = pivot_ofv(df4, 'Razón Social de la SGR')

        # Table to html
        table_pag.to_html('tables/negociada_PAGARE.html')
        # Add table to bavsa web
        create_html_bavsa('negociada_PAGARE', '@TABLA_negociada_PAGARE')

    # ##################################################################################
    # #################### Razón Social - PPV - Of. V. - Tipo = TODOS  #################
    # ##################################################################################

    # #####################################################################
    # Create pivot table Monto
    # ########################

    # Pivot table
    table_todos = pivot_ofv(df, 'Razón Social de la SGR')

    # Table to html
    table_todos.to_html('tables/negociada_TODOS.html')
    # Add table to bavsa web
    create_html_bavsa('negociada_TODOS', '@TABLA_negociada_TODOS')


def desierta(data):
    # ##################################################################################
    # ############################# DESIERTA #########################################
    # ##################################################################################

    df = data.query('Estado == ["Desierta"]')

    # ##################################################################################
    # #################### Razón Social - PPV - Of. V. - Tipo=CPD ######################
    # ##################################################################################

    # #####################################################################
    # Create pivot table Monto
    # ########################

    # Put the table in function of CPD
    df2 = df.query('Tipo == ["CPD"]')

    # Pivot table
    table_cpd = pivot_ofv(df2, 'Razón Social de la SGR')

    # Table to html
    table_cpd.to_html('tables/desierta_CPD.html')
    # Add table to bavsa web
    create_html_bavsa('desierta_CPD', '@TABLA_desierta_CPD')

    # ##################################################################################
    # #################### Razón Social - PPV - Of. V. - Tipo=ECHEQ ####################
    # ##################################################################################

    df = data.query('Estado == ["Desierta"]')
    df5 = df.query('Segmento == ["No Garantizado"]')
    df5 = df.query('Tipo == ["FCE"]')

    df5 = df5.rename(columns={'SGR / Librador': 'Librador'})

    if df5.empty:
        empty_function('desierta_NG_FCE')
    else:
        print(df5)
        # Pivot table
        table_cpd = pivot_ofv(df5, 'Librador')

        # Table to html
        table_cpd.to_html('tables/desierta_NG_FCE.html')
        # Add table to bavsa web
        create_html_bavsa('desierta_NG_FCE', '@TABLA_desierta_NG_FCE')

    # #####################################################################
    # Create pivot table Monto
    # ########################

    # Put the table in function of ECHEQ
    df3 = df.query('Tipo == ["ECHEQ"]')
    # Pivot table
    table_echeq = pivot_ofv(df3, 'Razón Social de la SGR')

    # Table to html
    table_echeq.to_html('tables/desierta_ECHEQ.html')
    # Add table to bavsa web
    create_html_bavsa('desierta_ECHEQ', '@TABLA_desierta_ECHEQ')
    # ##################################################################################
    # #################### Razón Social - PPV - Of. V. - Tipo=PAGARE ####################
    # ##################################################################################

    # #####################################################################
    # Create pivot table Monto
    # ########################

    # Put the table in function of PAGARE
    df4 = df.query('Tipo == ["PAGARE"]')
    if df4.empty:
        empty_function('desierta_PAGARE')
    else:
        # Pivot table
        table_pag = pivot_ofv(df4, 'Razón Social de la SGR')

        # Table to html
        table_pag.to_html('tables/desierta_PAGARE.html')
        # Add table to bavsa web
        create_html_bavsa('desierta_PAGARE', '@TABLA_desierta_PAGARE')

    # ##################################################################################
    # #################### Razón Social - PPV - Of. V. - Tipo = TODOS  #################
    # ##################################################################################

    # #####################################################################
    # Create pivot table Monto
    # ########################

    # Pivot table
    table_todos = pivot_ofv(df, 'Razón Social de la SGR')

    # Table to html
    table_todos.to_html('tables/desierta_TODOS.html')
    # Add table to bavsa web
    create_html_bavsa('desierta_TODOS', '@TABLA_desierta_TODOS')


def pivot_monto(df, index_val):
    # Create pivot table DESIERTA - NEGADA
    table_dn = df.pivot_table(index=index_val, columns='Estado', values='Monto', aggfunc=np.sum) \
        .reset_index()

    # Erase Desierta (Baja) column
    if len(table_dn.columns) > 3:
        table_dn.drop(table_dn.columns[2], axis=1, inplace=True)
        table_dn.columns.name = None

    table_dn.loc['Total'] = table_dn.select_dtypes(np.number).sum()
    table_dn.loc['Total', index_val] = ''

    # Fill Nan with zeros
    table_dn = table_dn.fillna(0)

    # Change format of columns
    # Column = "Desierta"
    table_dn['Desierta'] = table_dn['Desierta'].map('{:,.2f}'.format).str. \
        replace(",", "~").str.replace(".", ",").str.replace("~", ".")
    table_dn['Desierta'] = table_dn['Desierta'].replace('0,00', '-')
    # Column = "Negociada"
    table_dn['Negociada'] = table_dn['Negociada'].map('{:,.2f}'.format).str. \
        replace(",", "~").str.replace(".", ",").str.replace("~", ".")
    table_dn['Negociada'] = table_dn['Negociada'].replace('0,00', '-')

    return table_dn


def monto(data):

    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = CPD #####################
    # ##################################################################################

    df = data.query('Tipo == ["CPD"]')

    # Create pivot table DESIERTA - NEGADA
    table_dn = pivot_monto(df, 'Razón Social de la SGR')

    monto_cpd_des = table_dn.loc["Total", "Desierta"]
    monto_cpd_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    table_dn.to_html('tables/monto_CPD.html')
    # Add table to bavsa web
    create_html_bavsa('monto_CPD', '@TABLA_monto_CPD')
    # ##################################################################################
    # ################ Desierta - Negociada - Monto - Tipo = ECHEQ #####################
    # ##################################################################################

    df = data.query('Tipo == ["ECHEQ"]')

    # Create pivot table DESIERTA - NEGADA
    table_dn = pivot_monto(df, 'Razón Social de la SGR')

    monto_echeq_des = table_dn.loc["Total", "Desierta"]
    monto_echeq_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    table_dn.to_html('tables/monto_ECHEQ.html')
    # Add table to bavsa web
    create_html_bavsa('monto_ECHEQ', '@TABLA_monto_ECHEQ')
    # ##################################################################################
    # ################ Desierta - Negociada - Monto - Tipo = PAGARE ####################
    # ##################################################################################

    df = data.query('Tipo == ["PAGARE"]')

    # Create pivot table DESIERTA - NEGADA
    table_dn = df.pivot_table(index='Razón Social de la SGR', columns='Estado', values='Monto', aggfunc=np.sum)\
        .reset_index()
    table_dn.columns.name = None

    table_dn.loc['Total'] = table_dn.select_dtypes(np.number).sum()
    table_dn.loc['Total', 'Razón Social de la SGR'] = ''

    # Fill Nan with zeros
    table_dn = table_dn.fillna(0)

    # Change format of columns
    # Column = "Desierta"
    table_dn['Desierta'] = table_dn['Desierta'].map('{:,.2f}'.format).str.\
        replace(",", "~").str.replace(".", ",").str.replace("~", ".")
    table_dn['Desierta'] = table_dn['Desierta'].replace('0,00', '-')

    monto_pag_des = table_dn.loc["Total", "Desierta"]

    # Table to html
    table_dn.to_html('tables/monto_PAGARE.html')
    # Add table to bavsa web
    create_html_bavsa('monto_PAGARE', '@TABLA_monto_PAGARE')
    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = TODOS #####################
    # ##################################################################################

    # Create pivot table DESIERTA - NEGADA
    table_dn = pivot_monto(data, 'Razón Social de la SGR')

    monto_todos_des = table_dn.loc["Total", "Desierta"]
    monto_todos_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    table_dn.to_html('tables/monto_TODOS.html')
    # Add table to bavsa web
    create_html_bavsa('monto_TODOS', '@TABLA_monto_TODOS')

    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = NG CPD #####################
    # ##################################################################################

    df = data.query('Tipo == ["CPD"]')
    df = df.query('Segmento == "No Garantizado"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        empty_function('monto_NG_CPD')
        monto_NG_CPD_des = 0
        monto_NG_CPD_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_monto(df, 'Librador')

        monto_NG_CPD_des = table_dn.loc["Total", "Desierta"]
        monto_NG_CPD_neg = table_dn.loc["Total", "Negociada"]

        # Table to html
        table_dn.to_html('tables/monto_NG_CPD.html')
        # Add table to bavsa web
        create_html_bavsa('monto_NG_CPD', '@TABLA_monto_NG_CPD')

    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = NG ECHEQ #####################
    # ##################################################################################

    df = data.query('Tipo == ["ECHEQ"]')
    df = df.query('Segmento == "No Garantizado"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        empty_function('monto_NG_ECHEQ')
        monto_NG_ECHEQ_des = 0
        monto_NG_ECHEQ_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_monto(df, 'Librador')

        monto_NG_ECHEQ_des = table_dn.loc["Total", "Desierta"]
        monto_NG_ECHEQ_neg = table_dn.loc["Total", "Negociada"]
        # Table to html
        table_dn.to_html('tables/monto_NG_ECHEQ.html')
        # Add table to bavsa web
        create_html_bavsa('monto_NG_ECHEQ', '@TABLA_monto_NG_ECHEQ')

    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = NG FCE #####################
    # ##################################################################################

    df = data.query('Tipo == ["FCE"]')
    df = df.query('Segmento == "No Garantizado"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        empty_function('monto_NG_FCE')
        monto_NG_FCE_des = 0
        monto_NG_FCE_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_monto(df, 'Librador')

        monto_NG_FCE_des = table_dn.loc["Total", "Desierta"]
        monto_NG_FCE_neg = table_dn.loc["Total", "Negociada"]
        # Table to html
        table_dn.to_html('tables/monto_NG_FCE.html')
        # Add table to bavsa web
        create_html_bavsa('monto_NG_FCE', '@TABLA_monto_NG_FCE')

    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = NG PAGARE ###############
    # ##################################################################################

    df = data.query('Tipo == ["PAGARE"]')
    df = df.query('Segmento == "No Garantizado"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    table_dn = df.pivot_table(index='Librador', columns='Estado', values='Monto', aggfunc=np.sum) \
        .reset_index()

    if table_dn.empty:
        empty_function('monto_NG_PAGARE')
        monto_NG_PAGARE_des = 0
        monto_NG_PAGARE_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_monto(df, 'Librador')

        monto_NG_PAGARE_des = table_dn.loc["Total", "Desierta"]
        monto_NG_PAGARE_neg = table_dn.loc["Total", "Negociada"]

        # Table to html
        table_dn.to_html('tables/monto_NG_PAGARE.html')

        # Add table to bavsa web
        create_html_bavsa('monto_NG_PAGARE', '@TABLA_monto_NG_PAGARE')

    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = NG TODOS #####################
    # ##################################################################################

    df = data.query('Segmento == "No Garantizado"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        empty_function('monto_NG_TODOS')
        monto_NG_TODOS_des = 0
        monto_NG_TODOS_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_monto(df, 'Librador')

        monto_NG_TODOS_des = table_dn.loc["Total", "Desierta"]
        monto_NG_TODOS_neg = table_dn.loc["Total", "Negociada"]
        # Table to html
        table_dn.to_html('tables/monto_NG_TODOS.html')
        # Add table to bavsa web
        create_html_bavsa('monto_NG_TODOS', '@TABLA_monto_NG_TODOS')

    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = NGE CPD #####################
    # ##################################################################################

    df = data.query('Tipo == ["CPD"]')
    df = df.query('Segmento == "No Garantizado E.PYME"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        empty_function('monto_NGE_CPD')
        monto_NGE_CPD_des = 0
        monto_NGE_CPD_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_monto(df, 'Librador')

        monto_NGE_CPD_des = table_dn.loc["Total", "Desierta"]
        monto_NGE_CPD_neg = table_dn.loc["Total", "Negociada"]
        # Table to html
        table_dn.to_html('tables/monto_NGE_CPD.html')
        # Add table to bavsa web
        create_html_bavsa('monto_NGE_CPD', '@TABLA_monto_NGE_CPD')

    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = NGE ECHEQ #####################
    # ##################################################################################

    df = data.query('Tipo == ["ECHEQ"]')
    df = df.query('Segmento == "No Garantizado E.PYME"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        empty_function('monto_NGE_ECHEQ')
        monto_NGE_ECHEQ_des = 0
        monto_NGE_ECHEQ_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_monto(df, 'Librador')

        monto_NGE_ECHEQ_des = table_dn.loc["Total", "Desierta"]
        monto_NGE_ECHEQ_neg = table_dn.loc["Total", "Negociada"]
        # Table to html
        table_dn.to_html('tables/monto_NGE_ECHEQ.html')
        # Add table to bavsa web
        create_html_bavsa('monto_NGE_ECHEQ', '@TABLA_monto_NGE_ECHEQ')

    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = NG TODOS #####################
    # ##################################################################################

    df = data.query('Segmento == "No Garantizado E.PYME"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        empty_function('monto_NGE_TODOS')
        monto_NGE_TODOS_des = 0
        monto_NGE_TODOS_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_monto(df, 'Librador')

        monto_NGE_TODOS_des = table_dn.loc["Total", "Desierta"]
        monto_NGE_TODOS_neg = table_dn.loc["Total", "Negociada"]

        # Table to html
        table_dn.to_html('tables/monto_NGE_TODOS.html')
        # Add table to bavsa web
        create_html_bavsa('monto_NGE_TODOS', '@TABLA_monto_NGE_TODOS')

    list_montos = [monto_cpd_des, monto_cpd_neg, monto_echeq_des, monto_echeq_neg, monto_pag_des,
                   monto_todos_des, monto_todos_neg, monto_NG_CPD_des, monto_NG_CPD_neg, monto_NG_ECHEQ_des,
                   monto_NG_ECHEQ_neg, monto_NG_FCE_des, monto_NG_FCE_neg, monto_NG_PAGARE_des, monto_NG_PAGARE_neg,
                   monto_NG_TODOS_des, monto_NG_TODOS_neg, monto_NGE_CPD_des, monto_NGE_CPD_neg, monto_NGE_ECHEQ_des,
                   monto_NGE_ECHEQ_neg, monto_NGE_TODOS_des, monto_NGE_TODOS_neg]

    add_monto_tohtml_bavsa(list_montos)


def pivot_cheques(df, index_val):
    # Create pivot table DESIERTA - NEGADA
    table_dn = df.pivot_table(index=index_val, columns='Estado', values='Cheques', aggfunc=np.sum) \
        .reset_index()

    if len(table_dn.columns) > 3:
        # Erase Desierta (Baja) column
        table_dn.drop(table_dn.columns[2], axis=1, inplace=True)
        table_dn.columns.name = None

    table_dn.loc['Total'] = table_dn.select_dtypes(np.number).sum()
    table_dn.loc['Total', index_val] = ''

    # Fill Nan with zeros
    table_dn = table_dn.fillna(0)

    # Change format of columns
    # Column = "Desierta"
    table_dn['Desierta'] = table_dn['Desierta'].map('{:,.2f}'.format).str. \
        replace(",", "~").str.replace(".", ",").str.replace("~", ".")
    table_dn['Desierta'] = table_dn['Desierta'].replace('0,00', '-')
    # Column = "Negociada"
    table_dn['Negociada'] = table_dn['Negociada'].map('{:,.2f}'.format).str. \
        replace(",", "~").str.replace(".", ",").str.replace("~", ".")
    table_dn['Negociada'] = table_dn['Negociada'].replace('0,00', '-')

    return table_dn


def cant_cheques(data):
    # ##################################################################################
    # ################## Desierta - Negociada   - Tipo = CPD #####################
    # ##################################################################################

    df = data.query('Tipo == ["CPD"]')

    # Create pivot table DESIERTA - NEGADA
    table_dn = pivot_cheques(df, 'Razón Social de la SGR')

    cheques_cpd_des = table_dn.loc["Total", "Desierta"]
    cheques_cpd_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    # table_dn.to_html('tables/cheque_CPD.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_CPD', '@TABLA_cheque_CPD')
    # ##################################################################################
    # ################ Desierta - Negociada - Tipo = ECHEQ #####################
    # ##################################################################################

    df = data.query('Tipo == ["ECHEQ"]')

    # Create pivot table DESIERTA - NEGADA
    table_dn = pivot_cheques(df, 'Razón Social de la SGR')

    cheques_echeq_des = table_dn.loc["Total", "Desierta"]
    cheques_echeq_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    # table_dn.to_html('tables/cheque_ECHEQ.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_ECHEQ', '@TABLA_cheque_ECHEQ')

    # ##################################################################################
    # ################ Desierta - Negociada - Monto - Tipo = PAGARE ####################
    # ##################################################################################

    df = data.query('Tipo == ["PAGARE"]')

    # Create pivot table DESIERTA - NEGADA
    table_dn = df.pivot_table(index='Razón Social de la SGR', columns='Estado', values='Cheques', aggfunc=np.sum) \
        .reset_index()
    table_dn.columns.name = None

    table_dn.loc['Total'] = table_dn.select_dtypes(np.number).sum()
    table_dn.loc['Total', 'Razón Social de la SGR'] = ''

    # Fill Nan with zeros
    table_dn = table_dn.fillna(0)

    # Change format of columns
    # Column = "Desierta"
    table_dn['Desierta'] = table_dn['Desierta'].map('{:,.2f}'.format).str. \
        replace(",", "~").str.replace(".", ",").str.replace("~", ".")
    table_dn['Desierta'] = table_dn['Desierta'].replace('0,00', '-')

    cheques_pag_des = table_dn.loc["Total", "Desierta"]

    # Table to html
    # table_dn.to_html('tables/cheque_PAGARE.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_PAGARE', '@TABLA_cheque_PAGARE')

    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = TODOS #####################
    # ##################################################################################

    # Create pivot table DESIERTA - NEGADA
    table_dn = pivot_cheques(data, 'Razón Social de la SGR')

    cheques_todos_des = table_dn.loc["Total", "Desierta"]
    cheques_todos_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    # table_dn.to_html('tables/cheque_TODOS.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_TODOS', '@TABLA_cheque_TODOS')

    # ##################################################################################
    # ################## Desierta - Negociada - Tipo = NG CPD #####################
    # ##################################################################################

    df = data.query('Tipo == ["CPD"]')
    df = df.query('Segmento == "No Garantizado"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        cheques_NG_CPD_des = 0
        cheques_NG_CPD_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_cheques(df, 'Librador')

        cheques_NG_CPD_des = table_dn.loc["Total", "Desierta"]
        cheques_NG_CPD_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    # table_dn.to_html('tables/cheque_NG_CPD.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_NG_CPD', '@TABLA_cheque_NG_CPD')

    # ##################################################################################
    # ################## Desierta - Negociada - Tipo = NG ECHEQ #####################
    # ##################################################################################

    df = data.query('Tipo == ["ECHEQ"]')
    df = df.query('Segmento == "No Garantizado"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        cheques_NG_ECHEQ_des = 0
        cheques_NG_ECHEQ_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_cheques(df, 'Librador')

        cheques_NG_ECHEQ_des = table_dn.loc["Total", "Desierta"]
        cheques_NG_ECHEQ_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    # table_dn.to_html('tables/cheque_NG_ECHEQ.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_NG_ECHEQ', '@TABLA_cheque_NG_ECHEQ')

    # ##################################################################################
    # ################## Desierta - Negociada - Tipo = NG FCE #####################
    # ##################################################################################

    df = data.query('Tipo == ["FCE"]')
    df = df.query('Segmento == "No Garantizado"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        cheques_NG_FCE_des = 0
        cheques_NG_FCE_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_cheques(df, 'Librador')

        cheques_NG_FCE_des = table_dn.loc["Total", "Desierta"]
        cheques_NG_FCE_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    # table_dn.to_html('tables/cheque_NG_FCE.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_NG_FCE', '@TABLA_cheque_NG_FCE')

    # ##################################################################################
    # ################## Desierta - Negociada - Tipo = NG PAGARE ###############
    # ##################################################################################

    df = data.query('Tipo == ["PAGARE"]')
    df = df.query('Segmento == "No Garantizado"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    table_dn = df.pivot_table(index='Librador', columns='Estado', values='Cheques', aggfunc=np.sum) \
        .reset_index()

    if table_dn.empty:
        cheques_NG_PAGARE_des = 0
        cheques_NG_PAGARE_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_cheques(df, 'Librador')

        cheques_NG_PAGARE_des = table_dn.loc["Total", "Desierta"]
        cheques_NG_PAGARE_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    # table_dn.to_html('tables/cheque_NG_PAGARE.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_NG_PAGARE', '@TABLA_cheque_NG_PAGARE')

    # ##################################################################################
    # ################## Desierta - Negociada - Tipo = NG TODOS #####################
    # ##################################################################################

    df = data.query('Segmento == "No Garantizado"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        cheques_NG_TODOS_des = 0
        cheques_NG_TODOS_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_cheques(df, 'Librador')

        cheques_NG_TODOS_des = table_dn.loc["Total", "Desierta"]
        cheques_NG_TODOS_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    # table_dn.to_html('tables/cheque_NG_TODOS.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_NG_TODOS', '@TABLA_cheque_NG_TODOS')

    # ##################################################################################
    # ################## Desierta - Negociada - Tipo = NGE CPD #####################
    # ##################################################################################

    df = data.query('Tipo == ["CPD"]')
    df = df.query('Segmento == "No Garantizado E.PYME"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        cheques_NGE_CPD_des = 0
        cheques_NGE_CPD_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_cheques(df, 'Librador')

        cheques_NGE_CPD_des = table_dn.loc["Total", "Desierta"]
        cheques_NGE_CPD_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    # table_dn.to_html('tables/cheque_NGE_CPD.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_NGE_CPD', '@TABLA_cheque_NGE_CPD')

    # ##################################################################################
    # ################## Desierta - Negociada - Monto - Tipo = NGE ECHEQ #####################
    # ##################################################################################

    df = data.query('Tipo == ["ECHEQ"]')
    df = df.query('Segmento == "No Garantizado E.PYME"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        cheques_NGE_ECHEQ_des = 0
        cheques_NGE_ECHEQ_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_cheques(df, 'Librador')

        cheques_NGE_ECHEQ_des = table_dn.loc["Total", "Desierta"]
        cheques_NGE_ECHEQ_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    # table_dn.to_html('tables/cheque_NGE_ECHEQ.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_NGE_ECHEQ', '@TABLA_cheque_NGE_ECHEQ')

    # ##################################################################################
    # ################## Desierta - Negociada- Tipo = NG TODOS #####################
    # ##################################################################################

    df = data.query('Segmento == "No Garantizado E.PYME"')
    df = df.rename(columns={'SGR / Librador': 'Librador'})

    if df.empty:
        cheques_NGE_TODOS_des = 0
        cheques_NGE_TODOS_neg = 0
    else:
        # Create pivot table DESIERTA - NEGADA
        table_dn = pivot_cheques(df, 'Librador')

        cheques_NGE_TODOS_des = table_dn.loc["Total", "Desierta"]
        cheques_NGE_TODOS_neg = table_dn.loc["Total", "Negociada"]

    # Table to html
    # table_dn.to_html('tables/cheque_NGE_TODOS.html')
    # Add table to bavsa web
    # create_html_bavsa('cheque_NGE_TODOS', '@TABLA_cheque_NGE_TODOS')

    list_cheques = [cheques_cpd_des, cheques_cpd_neg, cheques_echeq_des, cheques_echeq_neg, cheques_pag_des,
                    cheques_todos_des, cheques_todos_neg, cheques_NG_CPD_des, cheques_NG_CPD_neg, cheques_NG_ECHEQ_des,
                    cheques_NG_ECHEQ_neg, cheques_NG_FCE_des, cheques_NG_FCE_neg, cheques_NG_PAGARE_des,
                    cheques_NG_PAGARE_neg, cheques_NG_TODOS_des, cheques_NG_TODOS_neg, cheques_NGE_CPD_des,
                    cheques_NGE_CPD_neg, cheques_NGE_ECHEQ_des, cheques_NGE_ECHEQ_neg,
                    cheques_NGE_TODOS_des, cheques_NGE_TODOS_neg]

    add_cheque_tohtml_bavsa(list_cheques)


def add_cheque_tohtml_bavsa(data):
    """
        Add values and quantities
    """
    # Static = bavsa
    with open('tables/bavsa.html', 'r') as f:
        static = str(f.read())

    tag_list = ["@cheques_cpd_des", "@cheques_cpd_neg", "@cheques_echeq_des", "@cheques_echeq_neg", "@cheques_pag_des",
                "@cheques_todos_des", "@cheques_todos_neg", "@cheques_NG_CPD_des", "@cheques_NG_CPD_neg",
                "@cheques_NG_ECHEQ_des", "@cheques_NG_ECHEQ_neg", "@cheques_NG_FCE_des", "@cheques_NG_FCE_neg",
                "@cheques_NG_PAGARE_des", "@cheques_NG_PAGARE_neg", "@cheques_NG_TODOS_des", "@cheques_NG_TODOS_neg",
                "@cheques_NGE_CPD_des", "@cheques_NGE_CPD_neg", "@cheques_NGE_ECHEQ_des", "@cheques_NGE_ECHEQ_neg",
                "@cheques_NGE_TODOS_des", "@cheques_NGE_TODOS_neg"]
    name = "bavsa"

    i = 0
    for tag in tag_list:
        begin = static.find(tag)
        str_l = len(tag)
        end = begin + str_l
        static = static[0:begin] + str(data[i]) + static[end:]
        i = 1 + i

    # Save bavsa web
    save_doc_to_html(static, name)


def create_html_bavsa(file_name, table_tag):
    name = "bavsa"

    if file_name == "negociada_CPD":
        # Static = Plantilla inicial
        with open('template.html', 'r') as f:
            static = str(f.read())
    else:
        # Static = bavsa
        with open('tables/bavsa.html', 'r') as f:
            static = str(f.read())
    # Open html table
    path = 'tables/' + file_name + '.html'
    with open(path, 'r') as f:
        str_table = str(f.read())

    if str_table.find('OTROS') == 243:
        new_table = str_table
        begin = static.find(table_tag)
        str_l = len(table_tag)
        end = begin + str_l
        html_file = static[0:begin] + new_table + static[end:]
    else:
        # Search begin and end of the table in html file
        begin = str_table.find('<table border="1" class="dataframe"> \n <thead>\n<tr style="text-align: right;">') + 83
        end = str_table.find('</table>') + 8
        # Create a string with only the table
        new_table = "<table class='table table-striped table-bordered dt-responsive nowrap' " \
                    "style='width:100%'>\n<thead>\n<tr>" + str_table[begin:end]
        begin = static.find(table_tag)
        str_l = len(table_tag)
        end = begin + str_l
        html_file = static[0:begin] + new_table + static[end:]

    # Save bavsa web
    save_doc_to_html(html_file, name)


def add_monto_tohtml_bavsa(data):
    """
        Add values and quantities
    """
    # Static = bavsa
    with open('tables/bavsa.html', 'r') as f:
        static = str(f.read())

    tag_list = ["@monto_cpd_des", "@monto_cpd_neg", "@monto_echeq_des", "@monto_echeq_neg", "@monto_pag_des",
                "@monto_todos_des", "@monto_todos_neg", "@monto_NG_CPD_des", "@monto_NG_CPD_neg", "@monto_NG_ECHEQ_des",
                "@monto_NG_ECHEQ_neg", "@monto_NG_FCE_des", "@monto_NG_FCE_neg", "@monto_NG_PAGARE_des",
                "@monto_NG_PAGARE_neg", "@monto_NG_TODOS_des", "@monto_NG_TODOS_neg", "@monto_NGE_CPD_des",
                "@monto_NGE_CPD_neg", "@monto_NGE_ECHEQ_des", "@monto_NGE_ECHEQ_neg", "@monto_NGE_TODOS_des",
                "@monto_NGE_TODOS_neg"]

    name = "bavsa"

    i = 0
    for tag in tag_list:
        begin = static.find(tag)
        str_l = len(tag)
        end = begin + str_l
        static = static[0:begin] + str(data[i]) + static[end:]
        i = 1 + i

    # Save bavsa web
    save_doc_to_html(static, name)


def save_doc_to_html(str_table, file_name):
    """
        Saves str_table into HTML file
        arg:
            string table
    """
    path = 'tables/' + file_name + '.html'
    with open(path, 'w') as f:
        f.write(str_table)


def main():
    # Fix file
    #file_name = 'subastas.xlsx'
    file_name = 'excelf.xlsx'
    file_path = 'excel/'

    # file_name = str(sys.argv[1])

    if len(sys.argv) == 2:
        file_name = str(sys.argv[1])

    try:
        # Read excel file with pandas (skip some rows)
        data = pd.read_excel(file_path + file_name, skiprows=range(0, 3))
    except FileNotFoundError:
        print('No such file of directory: ', file_path + file_name)
        return 0

    # Call FUNCTIONS

    # html negociada
    negociada(data)
    # html desierta
    desierta(data)
    # NO Garantizado
    no_garantizado(data)
    # NO Garantizado EPYME
    no_Garantizado_epyme(data)
    # html monto
    monto(data)
    # html cheques
    cant_cheques(data)
    # Graphics
    # graphics(data)

    copyfile('tables/bavsa.html', 'public/index.html')


if __name__ == "__main__":
    main()
