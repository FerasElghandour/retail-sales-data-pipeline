"""Offline example using the public implementation; see README for evidence scope."""
import sys,json,pathlib,os
repo=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(repo));sys.path.insert(0,str(repo/'src'));os.chdir(repo)
import pandas as pd,numpy as np,contextlib,io
from notebook_units import definitions
scope=definitions(['clean_types_and_missing','add_derived_features'],{'pd':pd,'np':np})
cols=['base_price','final_price','discount_pct','quantity_sold','revenue','customer_rating','weight_kg','battery_life_hours','ram_gb','storage_gb','cpu_cores','cpu_base_ghz','display_inches']
raw=pd.DataFrame({k:[1.,np.nan,3.] for k in cols})
raw['sale_date']=['2024-01-01','2024-02-01','2024-03-01'];raw['gpu']=['Integrated','NVIDIA RTX','Integrated']
with contextlib.redirect_stdout(io.StringIO()):
 clean=scope['clean_types_and_missing'](raw);result=scope['add_derived_features'](clean)
print(json.dumps({"fixture":"three generated laptop rows","rating":result.customer_rating.tolist(),"gpu":result.has_dedicated_gpu.tolist(),"months":result.sale_month.tolist(),"original_missing":int(raw.customer_rating.isna().sum())}))
