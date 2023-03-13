import csv
import numpy as np
import pandas as pd


class Data:
    def __init__(self, file_dir, data_type = 'lammps'):
        supported_data_types = ['lammps','moltemplate']
        if data_type not in supported_data_types:
            raise ValueError(f"{data_type} not supported.")
        self.data_type = data_type
        self.data_list = self.read_data_file(file_dir=file_dir)
        self.tot_lines = len(self.data_list)

    @staticmethod
    def read_data_file(file_dir):
        line_list = []
        with open(file_dir, newline='') as csv_file:
            data_reader = csv.reader(csv_file, delimiter=' ')
            for line in data_reader:
                row_string = ' '.join(line)
                try:
                    if not (row_string[0] == '#'):
                        line_list.append(row_string) # this condition ignores the comments section
                except:
                    line_list.append(row_string)
        return line_list

    def read_line(self, line_num):
        if line_num > self.tot_lines:
            raise ValueError("Not enough lines in the data file.")
        return self.data_list[line_num]


class Atoms(Data):
    def __init__(self, file_dir, data_type="lammps"):
        super().__init__(file_dir=file_dir, data_type=data_type)
        self.atom_id_list = []
        self.mol_id_list = []
        self.atom_type_list = []
        self.partial_charge_list = []
        self.x_coord_list = []
        self.y_coord_list = []
        self.z_coord_list = []
        self.parse_atom_section()
        self.tot_lines = len(self.atom_type_list)
        # del self.data_list

    @property
    def start_line_num(self):
        for line_num, line_data in enumerate(self.data_list):
            if (self.data_type == "lammps") and (line_data == "Atoms"):
                return line_num
            if (self.data_type == "moltemplate") and ('''write("Data Atoms"){''' in line_data):
                return line_num

    @property
    def end_line_num(self):
        if self.data_type == 'lammps':
            for line_num in range(self.start_line_num+2, self.tot_lines):
                if not self.data_list[line_num]:
                    return line_num
        elif self.data_type == 'moltemplate':
            for line_num in range(self.start_line_num+1, self.tot_lines):
                if "}" in self.data_list[line_num]:
                    return line_num

    @property
    def atom_data_list(self):
        if self.data_type == 'lammps':
            return self.data_list[self.start_line_num+2:self.end_line_num]
        elif self.data_type == 'moltemplate':
            return self.data_list[self.start_line_num+1:self.end_line_num]

    def parse_atom_section(self):
        for atom in self.atom_data_list:
            # if self.data_type == "lammps":
            info = atom.split(" ")
            info_remove_spaces = [item for item in info if item]
            # print(info_remove_spaces)
            self.atom_id_list.append(info_remove_spaces[0])
            self.mol_id_list.append(info_remove_spaces[1])
            self.atom_type_list.append(info_remove_spaces[2])
            self.partial_charge_list.append(info_remove_spaces[3])
            self.x_coord_list.append(info_remove_spaces[4])
            self.y_coord_list.append(info_remove_spaces[5])
            self.z_coord_list.append(info_remove_spaces[6])
        # convert list to numpy array if data_type is lammps
        if self.data_type == "lammps":
            self.atom_id_list = np.array(self.atom_id_list).astype(int)
            self.mol_id_list = np.array(self.mol_id_list).astype(int)
            self.atom_type_list = np.array(self.atom_type_list).astype(int)
        self.partial_charge_list = np.array(self.partial_charge_list).astype(np.float64)
        self.x_coord_list = np.array(self.x_coord_list).astype(np.float64)
        self.y_coord_list = np.array(self.y_coord_list).astype(np.float64)
        self.z_coord_list = np.array(self.z_coord_list).astype(np.float64)

    def translate(self, x, y, z):
        self.x_coord_list += x
        self.y_coord_list += y
        self.z_coord_list += z

    def create_pd(self):
        df = pd.DataFrame({
            "Atom ID": self.atom_id_list,
            "Mol ID": self.mol_id_list,
            "Atom_type": self.atom_type_list,
            "Charges": self.partial_charge_list,
            "x": self.x_coord_list,
            "y": self.y_coord_list,
            "z": self.z_coord_list
        })
        return df

    def display_info(self):
        print(self.create_pd())

    def write_data(self, o_file_dir):
        self.create_pd().to_csv(o_file_dir, index=False, sep='\t')


