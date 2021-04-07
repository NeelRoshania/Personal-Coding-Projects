def convert_to(val, typefunc):

    # Convert a value a datatype if not null
    if not np.isnan(val):
        return typefunc(val)
    else:
        return val

def export_df(df, cols, **kwargs):

    # rename and return a dataframe of those columns
    # choose to export or not
    # choose to return df
    # choose to export to sql database
    
    _df = df.loc[:, cols]
    
    # rename dict
    if "rename_dict" in kwargs.keys() :
        _df.rename(columns=kwargs["rename_dict"], inplace=True)
        print('- Columns renamed.')
    
    # export data
    if "export_loc" in kwargs.keys():
        
        # handle data export
        try:
            
            if "export_name" in kwargs.keys():
                _location = '{}\{}.csv'.format(kwargs["export_loc"], kwargs["export_name"])
                _df.to_csv(_location)
                print(f"""- File exported to: {_location}""")
            else:
                _location = '{}\\adhoc_{}.csv'.format(kwargs["export_loc"], kwargs["export_name"], datetime.today().strftime("%m%d%y"))
                _df.to_csv(_location)
                print(f"""- File exported to: {_location}""")

        except:
            raise Exception(f"""export_loc must be of type str or other""")

    # export data
    if "return_df" in kwargs.keys():
        if kwargs['return_df']:
            return _df

def test(str_great):
    print(str_great)
    pass
 
