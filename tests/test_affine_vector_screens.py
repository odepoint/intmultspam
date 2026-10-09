from pathlib import Path
import sys,unittest,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from experiments.affine_vector_screens import golay_code,leech_lines,leech_minor,polynomial_code_base,polynomial_code_witness
from experiments.cube_core_family import xor_permute


class AffineVectorScreens(unittest.TestCase):
    def test_exact_code_and_vector_inventory(self):
        self.assertEqual(len(golay_code()),4096)
        v=leech_lines();self.assertEqual(len(v),98280)
        self.assertEqual(len(set(v)),len(v))

    def test_finite_lattice_minor_and_corruption_rejection(self):
        path=Path(__file__).resolve().parents[1]/'scripts/experiments/affine_vector_witnesses.json'
        f=json.loads(path.read_text())['leech'][0]
        result=leech_minor(**f)
        self.assertTrue(result['positive_deficit_excluded'])
        self.assertEqual(result['binary_rank_lower'],683)
        f['independent_rows']=[0,0]
        with self.assertRaises(ValueError):leech_minor(**f)
        with self.assertRaises(ValueError):leech_minor([0,0],[0])
        with self.assertRaises(ValueError):leech_minor([0],[0],shift=3)

    def test_polynomial_code_rows_against_direct_word_evaluation(self):
        data=polynomial_code_base([(0,1,2)])
        def word(x):
            value=0
            for i,v in enumerate(data['basis']):
                if x>>i&1:value^=v
            return value
        for i in (0,1,17,12345):
            row=xor_permute(data['base'],i,data['n'])
            for j in (0,1,17,31,1024,54321,65535):
                self.assertEqual((row>>j)&1,int(i==j or (word(i)^word(j)).bit_count()==16))
        with self.assertRaises(ValueError):polynomial_code_base([(0,0,1)])
        with self.assertRaises(ValueError):polynomial_code_witness([(0,1,2)],[0,0])


if __name__=='__main__':unittest.main()
