import csv
import numpy as np
import pandas as pd


class Analysis:
    def __init__(self, input_filename, atom_type, time_between_frames):
        self.input_filename = input_filename
        self.atom_type = atom_type
        self.l_ts, self.l_id, self.l_x, self.l_y, self.l_z = self.extract_data()
        self.dt = time_between_frames

    def extract_data(self):
        self.atom_type = 1
        list_timestep, l_id, l_x_coord, l_y_coord, l_z_coord = [], [], [], [], []
        read_timestep_flag = False
        current_timestep = None
        read_coord = False
        with open(self.input_filename, newline='') as trj_file:
            reader = csv.reader(trj_file, delimiter=' ')
            line_number = 0
            for line in reader:
                line_string = ' '.join(line)
                if read_timestep_flag:
                    current_timestep = int(line_string)
                    read_timestep_flag = False
                if line_string == 'ITEM: TIMESTEP':
                    read_timestep_flag = True
                    read_coord = False
                if read_coord:
                    if int(line[1]) == self.atom_type:
                        list_timestep.append(current_timestep)
                        l_id.append(int(line[0]))
                        l_x_coord.append(float(line[2]))
                        l_y_coord.append(float(line[3]))
                        l_z_coord.append(float(line[4]))
                if line_string == 'ITEM: ATOMS id type xs ys zs':
                    read_coord = True
                line_number += 1
        return np.array(list_timestep), np.array(l_id), np.array(l_x_coord), np.array(l_y_coord), np.array(l_z_coord)

    def output_coord(self, output_filename):
        df = pd.DataFrame({
            'time step': self.l_ts,
            'id': self.l_id,
            'x': self.l_x,
            'y': self.l_y,
            'z': self.l_z
        })
        df.to_csv(output_filename, index=False)

    def find_coords(self, time_step, atom_id):
        for i, ts_ in enumerate(self.l_ts):
            if ts_ == time_step:
                if self.l_id[i] == atom_id:
                    return self.l_x[i], self.l_y[i], self.l_z[i]

    @property
    def unique_id(self):
        return np.unique(self.l_id)

    @property
    def N(self):
        return len(self.unique_id)

    def msd(self, timestep):
        numerator = 0
        for id_ in self.unique_id:
            x_,y_,z_ = self.find_coords(time_step=0, atom_id=id_)
            x,y,z = self.find_coords(time_step=timestep, atom_id=id_)
            distance = np.sqrt((x - x_)**2 + (y - y_)**2 + (z - z_)**2)
            numerator += distance**2
        return numerator / self.N

    def calc_D(self):
        msd = self.msd(self.l_ts[-1]) * 1e-20
        t = self.dt * self.l_ts[-1]
        return msd/(6*t)
