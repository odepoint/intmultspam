from pathlib import Path
from fractions import Fraction as Q
import json,sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from general_network_guard import guard,strict_integer_power,limiting_ceiling,hypothetical_parameters

ROOT=Path(__file__).resolve().parents[1]

class GeneralNetworkGuard(unittest.TestCase):
    def test_retained_complex_guard_is_identical(self):
        c=json.loads((ROOT/'certificates/complex-compression.json').read_text())
        n=c['counts'];a=c['assembly_control'];p=a['parameters']
        g=guard(int(n['m']),int(n['s']),int(a['guard_node_charge']),Q(p['beta']),Q(1,1000),Q(5))
        self.assertEqual(g['C0'],int(a['guard_C0']))
        self.assertEqual(g['C1'],Q(a['guard_C1']))

    def test_integer_residual_power_is_strict(self):
        for m in (3,5,16):
            for s in (2,m-1,m,m*m-1,m*m,m**7):
                L=strict_integer_power(m,s)
                self.assertLess(s,m**L)
                if L>1:self.assertGreaterEqual(s,m**(L-1))

    def test_exact_stopped_recurrences(self):
        for m in (3,5):
            for L in (1,2,5,7):
                s=m**L-1
                for beta in (Q(1,4),Q(1,2),Q(3,4),Q(9,10)):
                    D=beta.denominator*2;d=m**D;leaf=m**int(D*beta)
                    for E in (0,1,19):
                        g=guard(m,s,E,beta,Q(1,100),Q(L))
                        for e in (1,leaf-1,leaf,d):
                            child=e;j=0
                            while child>=leaf:child//=m;j+=1
                            actual=8*child*s**j+E*sum(s**i for i in range(j))
                            exponent=Q(D)*(L-(L-1)*beta)
                            self.assertEqual(exponent.denominator,1)
                            upper=s*(8+E)*m**exponent.numerator
                            self.assertLessEqual(actual,upper)
                            self.assertGreater(g['C1'],1)

    def test_rational_residual_exponent(self):
        g=guard(4,7,10,Q(1,2),Q(1,10),Q(3,2))
        self.assertEqual(g['C1'],Q(27,20))
        with self.assertRaises(Exception):guard(4,8,10,Q(1,2),Q(1,10),Q(3,2))

    def test_larger_guard_can_use_complex_headroom(self):
        weak=hypothetical_parameters(Q(16,10**8),Q(16,10**8),Q(7),Q(1,100))
        strong=hypothetical_parameters(Q(16,10**8),Q(32,10**8),Q(7),Q(1,2))
        self.assertFalse(weak['parameter_system_passes'])
        self.assertTrue(strong['parameter_system_passes'])
        self.assertFalse(strong['finite_networks_verified'])
        self.assertFalse(strong['scalar_node_charge_verified'])

    def test_necessary_ceiling_bounds_all_stopping_choices(self):
        for ab,ac in ((Q(1,10**7),Q(3,10**7)),(Q(3,10**7),Q(1,10**7)),(Q(1,10**7),Q(1,10**7))):
            for alpha in (Q(1),Q(5),Q(7),Q(21,2)):
                bound=limiting_ceiling(ab,ac,alpha)
                for i in range(1,100):
                    t=Q(i,100)
                    value=min(ab,t*ac)/max(Q(5),1+(alpha-1)*t)
                    self.assertLessEqual(value,bound['upper'])
                ratio=bound['complex_to_bit_ratio_for_gaussian_value_of_this_bound']
                self.assertGreaterEqual(ratio,1)
        self.assertEqual(limiting_ceiling(Q(1,10**7),Q(2,10**7),Q(7))['upper'],Q(1,5*10**7))

    def test_invalid_guard_inputs(self):
        for args in ((2,2,1,Q(1,2),Q(1,10)),(3,1,1,Q(1,2),Q(1,10)),(3,2,-1,Q(1,2),Q(1,10)),(3,2,1,0.5,Q(1,10))):
            with self.assertRaises(Exception):guard(*args)
        with self.assertRaises(Exception):guard(3,2,1,Q(1,2),Q(1,10),Q(1,2))

if __name__=='__main__':unittest.main()
