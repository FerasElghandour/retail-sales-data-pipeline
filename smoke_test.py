import pandas as pd
import numpy as np
from notebook_units import definitions
scope=definitions(['clean_types_and_missing','add_derived_features'], {'pd':pd,'np':np})
cols=['base_price','final_price','discount_pct','quantity_sold','revenue','customer_rating','weight_kg','battery_life_hours','ram_gb','storage_gb','cpu_cores','cpu_base_ghz','display_inches']
raw=pd.DataFrame({k:[1.,np.nan,3.] for k in cols})
raw['sale_date']=['2024-01-01','2024-02-01','2024-03-01']
raw['gpu']=['Integrated','NVIDIA RTX','Integrated']
clean=scope['clean_types_and_missing'](raw)
assert not clean[cols].isna().any().any()
assert clean['customer_rating'].iloc[1]==2.
assert raw['customer_rating'].isna().sum()==1
derived=scope['add_derived_features'](clean)
assert derived['has_dedicated_gpu'].tolist()==[0,1,0]
assert derived['sale_month'].tolist()==['2024-01','2024-02','2024-03']
print('Retail pipeline: median imputation, input preservation, GPU/date derivation passed.')
