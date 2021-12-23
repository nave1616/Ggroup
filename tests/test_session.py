import unittest
import sys
from pathlib import Path
path = Path(__file__).resolve().parent.parent
sys.path.append(str(path/'lib'))
from Data import Session, datetime_now, next_time
from pathlib import Path
class TestSession(unittest.TestCase):
    
    def setUp(self):
        self.path = Path('/home/vegi/Desktop/Gproject/data/session.yml')
        self.path.unlink(missing_ok=True)
        self.empty_session = Session() #file dont exist
        self.session = Session()
    
    def tearDown(self) -> None:
        pass
    
    def test_create(self):
        self.assertTrue(self.empty_session.path.exists())
        self.assertTrue(self.session.path.exists())
    
    def test_dict(self):
        last = datetime_now()
        next = next_time(last,7)
        self.assertDictEqual(d1={'last':last,'next':next,'repeat':0},d2=self.empty_session.data)
        #self.session.last,self.session.repeat = '12:20',1
        

if __name__ == '__main__':
    unittest.main()