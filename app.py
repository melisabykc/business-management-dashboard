import argparse, json, sqlite3
from pathlib import Path
DB=Path(__file__).with_name('data.sqlite3')
def connect(path=DB):
 c=sqlite3.connect(str(path)); c.row_factory=sqlite3.Row; c.execute('CREATE TABLE IF NOT EXISTS metrics(id INTEGER PRIMARY KEY, name TEXT NOT NULL, value REAL NOT NULL, category TEXT NOT NULL, period TEXT NOT NULL)'); return c
def add(name,value,category,period,path=DB):
 value=float(value)
 if not name.strip() or value<0: raise ValueError('name is required and value must be nonnegative')
 with connect(path) as c: cur=c.execute('INSERT INTO metrics(name,value,category,period) VALUES(?,?,?,?)',(name,value,category,period)); return cur.lastrowid
def listing(path=DB):
 with connect(path) as c:return [dict(r) for r in c.execute('SELECT * FROM metrics ORDER BY id DESC')]
def report(path=DB):
 rows=listing(path); cats={}
 for r in rows: cats[r['category']]=cats.get(r['category'],0)+r['value']
 return {'metric_count':len(rows),'total_value':sum(r['value'] for r in rows),'by_category':cats}
def main():
 p=argparse.ArgumentParser(description='Business KPI dashboard'); s=p.add_subparsers(dest='cmd',required=True); a=s.add_parser('add'); a.add_argument('--name',required=True); a.add_argument('--value',required=True,type=float); a.add_argument('--category',required=True); a.add_argument('--period',required=True); s.add_parser('list'); s.add_parser('report'); x=p.parse_args()
 if x.cmd=='add': print(json.dumps({'id':add(x.name,x.value,x.category,x.period)}))
 elif x.cmd=='list': print(json.dumps(listing(),indent=2))
 else: print(json.dumps(report(),indent=2))
if __name__=='__main__': main()
