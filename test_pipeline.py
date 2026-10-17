import unittest,pandas as pd,numpy as np
from pipeline import transform,NUMERIC
class Pipeline(unittest.TestCase):
 def frame(self):
  f=pd.DataFrame({c:[1.,2.,3.] for c in NUMERIC});f['sale_date']='2024-01-01';f['gpu']='Integrated';return f
 def test_invariants(self):
  f=self.frame();f.loc[1,'customer_rating']=np.nan;r=transform(f);self.assertEqual(len(r),3);self.assertEqual(r.customer_rating.iloc[1],2);self.assertEqual(len(set(r)-set(f)),6);self.assertTrue(f.customer_rating.isna().iloc[1])
 def test_invalid_schema_and_values(self):
  for kind in ['missing','null','date','zero']:
   f=self.frame()
   if kind=='missing':f=f.drop(columns='gpu')
   if kind=='null':f['ram_gb']=np.nan
   if kind=='date':f['sale_date']='invalid'
   if kind=='zero':f['cpu_cores']=0
   with self.subTest(kind=kind),self.assertRaises(ValueError):transform(f)
if __name__=='__main__':unittest.main()
