import tempfile, unittest
from pathlib import Path
import app
class Tests(unittest.TestCase):
 def test_metric(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'test.sqlite3'; app.add('Revenue',100,'Finance','Q4',p); self.assertEqual(app.report(p)['metric_count'],1)
if __name__=='__main__': unittest.main()
