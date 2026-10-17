"""Validated reusable execution of the notebook's retail transformations."""
import argparse,contextlib,io,json,hashlib
from pathlib import Path
import numpy as np,pandas as pd
from notebook_units import definitions
NUMERIC=['base_price','final_price','discount_pct','quantity_sold','revenue','customer_rating','weight_kg','battery_life_hours','ram_gb','storage_gb','cpu_cores','cpu_base_ghz','display_inches']
def transform(frame):
 missing=set(NUMERIC+['sale_date','gpu'])-set(frame)
 if missing:raise ValueError('Missing required columns: '+', '.join(sorted(missing)))
 checked=frame.copy()
 if checked.gpu.isna().any() or checked.gpu.astype(str).str.strip().eq('').any():raise ValueError('Missing GPU classification')
 if pd.to_datetime(checked.sale_date,errors='coerce').isna().any():raise ValueError('Invalid or missing sale dates')
 for c in NUMERIC:
  values=pd.to_numeric(checked[c],errors='coerce')
  if values.isna().all() or np.isinf(values).any():raise ValueError('All-null or infinite numeric field: '+c)
  checked[c]=values
 scope=definitions(['clean_types_and_missing','add_derived_features'],{'pd':pd,'np':np})
 with contextlib.redirect_stdout(io.StringIO()):
  clean=scope['clean_types_and_missing'](checked)
  if any((clean[c]<=0).any() for c in ['ram_gb','storage_gb','cpu_cores']):raise ValueError('RAM, storage and CPU cores must be positive')
  result=scope['add_derived_features'](clean)
 if not np.isfinite(result['spec_score']).all():raise ValueError('Nonfinite derived hardware score')
 return result

def main():
 p=argparse.ArgumentParser();p.add_argument('csv',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
 if a.output.exists():raise ValueError('Use a new output directory')
 a.output.mkdir(parents=True);frame=pd.read_csv(a.csv);result=transform(frame);result.to_csv(a.output/'cleaned.csv',index=False)
 (a.output/'metrics.json').write_text(json.dumps({'input_sha256':hashlib.sha256(a.csv.read_bytes()).hexdigest(),'rows':len(result),'rows_preserved':len(result)==len(frame),'derived_columns':[c for c in result if c not in frame],'numeric_missing_after':int(result[NUMERIC].isna().sum().sum()),'total_revenue':float(result.revenue.sum())},indent=2)+'\n')
if __name__=='__main__':main()
