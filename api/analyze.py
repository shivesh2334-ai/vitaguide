from http.server import BaseHTTPRequestHandler
import json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from engine import SupplementRecommender

def normalize(raw):
    p=dict(raw)
    for k in ['sex','diet_type','sun_exposure']:
        p[k]=str(p.get(k,'')).lower().split()[0] if p.get(k) else ''
    for k in ['pregnancy_status','vitamin_d_level','b12_level','iron_status','iodized_salt']:
        p[k]=str(p.get(k,'')).lower().replace(' ','_')
    p['pregnancy_status']={'currently_pregnant':'pregnant','currently_breastfeeding':'lactating'}.get(p['pregnancy_status'],p['pregnancy_status'])
    p['religious_preference']=str(p.get('religious','none')).lower().split()[0]
    p['conditions']=[{'Anemia/Iron deficiency':'anemia','Osteoporosis/Osteopenia':'osteoporosis','Diabetes/Pre-diabetes':'diabetes','Celiac disease':'celiac','History of bariatric surgery':'bariatric_surgery','Malabsorption issues':'malabsorption'}.get(c,c.lower().replace('/','_').replace(' ','_')) for c in p.get('conditions',[]) if c!='None/Healthy']
    if "Crohn's disease/Ulcerative colitis" in raw.get('conditions',[]):p['conditions'].extend(['crohns','ulcerative_colitis'])
    for k in ['fish_intake','dairy_intake']:p[k]='none' if p.get(k)=='Never/None' else str(p.get(k,'')).lower()
    p['test_deficiencies']=[k for k in ['vitamin_d_level','b12_level','iron_status'] if any(v in str(raw.get(k,'')).lower() for v in ['deficient','insufficient','low'])]
    if p.get('heavy_periods') or p.get('high_triglycerides'):p['test_deficiencies'].append('additional_risk')
    if p['vitamin_d_level'].startswith(('deficient','insufficient')):p['vitamin_d_level']='low'
    p['age']=int(p.get('age',30))
    if not 1<=p['age']<=120:raise ValueError('Age must be between 1 and 120')
    return p

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200);self.send_header('Content-Type','application/json');self.end_headers();self.wfile.write(b'{"status":"ok"}')
    def do_POST(self):
        try:
            size=int(self.headers.get('Content-Length',0))
            if size>32000:raise ValueError('Profile is too large')
            profile=normalize(json.loads(self.rfile.read(size)))
            result={'profile':profile,'recommendations':SupplementRecommender().analyze_user(profile)}
            self.send_response(200)
        except (ValueError,TypeError,KeyError,AttributeError):
            result={'error':'Invalid profile. Please check your entries.'}; self.send_response(400)
        self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(json.dumps(result).encode())
