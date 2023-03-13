from read_data import Data, Atoms


ec = Atoms('_NDV_allatom_optimized_geometry.lt', data_type='moltemplate')
print(ec.display_info())
ec.translate(1.9716566044E+00, 3.2565567903E-07, -5.6957540750E-03)
print(ec.display_info())
ec.translate(0.0,1.25,0.9)
print(ec.display_info())
ec.translate(1.5,1.5,0)
print(ec.display_info())
ec.write_data("EC_atoms.csv")