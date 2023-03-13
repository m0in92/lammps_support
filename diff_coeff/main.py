from analysis import Analysis


ana = Analysis(input_filename='nvt_test.lammpstrj', atom_type=1, time_between_frames=0.1e-15)
ana.output_coord(output_filename='li_coord.csv')
print(ana.unique_id)
print(ana.N)
print(ana.msd(1))
print(ana.calc_D())
