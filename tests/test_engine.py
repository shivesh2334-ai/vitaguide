import sys,ast,json,random,pathlib
p=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(p/'api'))
from analyze import normalize
from engine import SupplementRecommender
src=ast.parse((p/'vitaguide_app.py').read_text());copy=ast.parse((p/'api/engine.py').read_text())
assert [ast.dump(n) for n in src.body if isinstance(n,ast.ClassDef)]==[ast.dump(n) for n in copy.body]
f=json.loads((p/'public/knowledge.json').read_text())['fields'];assert len(f)==17,len(f)
base={x['key']:x['value'] if x['type']=='number_input' else (False if x['type']=='checkbox' else [] if x['type']=='multiselect' else x['options'][0]) for x in f}
r=SupplementRecommender()
def rec(**kw):return r.analyze_user(normalize(dict(base,**kw)))
assert not rec()['supplements']
assert any('B12' in s['nutrient'] for s in rec(diet_type='Vegan (no animal products)')['supplements'])
assert any('Folic' in s['nutrient'] for s in rec(pregnancy_status='Currently pregnant')['supplements'])
assert any('Iron' in s['nutrient'] for s in rec(sex='Female',heavy_periods=True)['supplements'])
assert any('Calcium' in s['nutrient'] for s in rec(dairy_intake='Never/None',sun_exposure='Limited (office worker, limited outdoor)')['supplements'])
assert any('Halal' in s for s in rec(religious='Muslim (Halal)')['dietary_advice'])
assert any('glycemic' in s for s in rec(conditions=['Diabetes/Pre-diabetes'])['dietary_advice'])
random.seed(42)
for _ in range(100):
 profile={x['key']:random.randint(1,120) if x['type']=='number_input' else bool(random.getrandbits(1)) if x['type']=='checkbox' else random.sample(x['options'],min(2,len(x['options']))) if x['type']=='multiselect' else random.choice(x['options']) for x in f}
 json.dumps(r.analyze_user(normalize(profile)))
D=json.loads((p/'public/indian-medicines.json').read_text());assert len(D)==23 and all(len(v['products'])==5 for v in D.values())
assert all(x['source'].startswith('https://') for v in D.values() for x in v['products'])
print('PASS: exact original engine AST; 17 inputs; 7 assessment scenarios; 100 varied profiles; 23 categories / 115 sourced listings')
