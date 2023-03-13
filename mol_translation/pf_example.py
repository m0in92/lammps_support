from read_data import Atoms


pf = Atoms('PF.data')
print(pf.atom_type_list)
pf.translate(-17.1391,-34.1549,-40.1795)
pf.translate(2.0, 2.0, 21)
print(pf.display_info())
pf.write_data('pf_atoms.csv')
