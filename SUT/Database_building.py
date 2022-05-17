#%% Importing all the libraries and external information
import pandas as pd
import mario
import os
#%%
path = pd.read_excel('Local paths/path.xlsx', index_col=[0]) # Reading the file where you can store your local path of Exiobase
year = path.loc['year','Value']

def extending_exio_SUT(name,year,SUT_path,IOT_path,SUT_agg,IOT_agg): # do everything with the path file
    # Parsing Exiobase SUT and IOT for selected year
    World_SUT = mario.parse_exiobase_sut(SUT_path) # Importing the SUT that will be used as the main result
    World_IOT = mario.parse_exiobase_3(IOT_path) # Importing the IOT that will be used to take the extensions

    # Aggregating both SUT and IOT with the same level of aggregation
    World_SUT.aggregate(SUT_agg) # Aggregating the SUT with the proper template file (it is generated by MARIO with get_aggregation_excel function) 
    World_IOT.aggregate(IOT_agg) # Aggregating the SUT with the proper template file (it is generated by MARIO with get_aggregation_excel function)

    # Adding the
    E_IOT = World_IOT.E # Taking Satellite account from world_IOT
    E_SUT = World_SUT.E # Taking Satellite account from world_SUT (is empty)
    new_E_SUT = pd.DataFrame(0, index=E_IOT.index, columns=E_SUT.columns)
    new_E_SUT.loc[:,(slice(None),'Activity')] = E_IOT.values
    new_units = World_IOT.units['Satellite account']
    #%%
    World_SUT.add_extensions(io= new_E_SUT, 
                            matrix= 'E',
                            units= new_units,
                            EY = World_IOT.EY,
                            inplace=True, # implementing the changes on the database
                            )
    #%%
    db_dir = f'Database/{name}_{year}'
    try:
        os.mkdir(db_dir)
    except OSError:
        print("Creation of the directory %s failed" % db_dir)
    else:
        print("Directory already exists %s" %db_dir)

    World_SUT.to_txt(f'Database/{name}_{year}')
# %%
from Database_building import extending_exio_SUT as b_SUT
import pandas as pd

path = pd.read_excel('Local paths/path.xlsx', index_col=[0]) # Reading the file where you can store your local path of Exiobase
SUT_path = path.loc['SUT','Value']
IOT_path = path.loc['IOT','Value']
year = path.loc['year','Value']
SUT_agg = "Aggregations/SUT_agg.xlsx"
IOT_agg = "Aggregations/IOT_agg.xlsx"

b_SUT("BASF",year,SUT_path,IOT_path,SUT_agg,IOT_agg)

# %%