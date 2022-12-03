"""Main module."""
import os
import shutil
import qff_utils.spec2latex.panda_qff as panda_qff
import subprocess
import pickle


class QffHelper:
    def __init__(self, _freqs_dir: str = "freqs", _on_eland: bool = "False"):
        # TODO setup optional initializations with sane defaults
        if _on_eland:
            top = "/home/r410/programs"
            self.programs = {
                "anpass": top + "/anpass/anpass_cerebro.x",
                "spectro": 'gspectro -cmd /home/r410/programs/spec3jm.ifort-O0.static.x',
                "intder": top + "/intder/Intder2005.x",
            }
        else:
            top = "/ddn/home6/r2533/programs"
            self.programs = {
                "anpass": top + "/anpass/anpass_cerebro.x",
                "spectro": "gspectro",
                "intder": top + "/intder/Intder2005.x",
            }
        cwd = os.getcwd()
        abs_freqs_dir = cwd + "/" + _freqs_dir
        self.freqs_dir = _freqs_dir
        self.freqs_files = {
            "anpass": abs_freqs_dir + "/anpass.tmp",
            "intder": abs_freqs_dir + "/intder.tmp",
            "spectro": abs_freqs_dir + "/spectro.tmp",
        }
        self.input_files = {
            "anpass1": abs_freqs_dir + "/anpass1.in",
            "anpass2": abs_freqs_dir + "/anpass2.in",
            "intder_geom": abs_freqs_dir + "/intder_geom.in",
            "intder": abs_freqs_dir + "/intder.in",
            "spectro": abs_freqs_dir + "/spectro.in",
        }
        self.output_files = {
            "anpass1": abs_freqs_dir + "/anpass1.out",
            "anpass2": abs_freqs_dir + "/anpass2.out",
            "intder_geom": abs_freqs_dir + "/intder_geom.out",
            "intder": abs_freqs_dir + "/intder.out",
            "spectro": abs_freqs_dir + "/spectro2.out",
            "summarize": abs_freqs_dir + "/spectro2.sum",
            "json": abs_freqs_dir + "/spectro2.json",
        }

    files = {}
    freqs_files = {}
    energies = []
    relative_energies = []
    freqs_dir = "freqs"
    anpass_refit_energy = 0.0

    #    top_location =   "/home/lailah/Documents/OleMiss/programming/Python/qff_helper/Programs"
    #    anpass_location = "/home/megan/Programs/anpass/anpass_cerebro.x"
    #    spectro_location = "/home/megan/Programs/spec3jm.ifort-00.static.x"
    #    intder_location = "/home/megan/Programs/intder/Intder2005.x"
    #    anpass_location = top_location + "/anpass/anpass_cerebro.x"
    #    spectro_location = top_location + "/spec3jm.ifort-00.static.x"
    #   intder_location = top_location = "/intder/Intder2005.x"
    # TODO change this based on host. Or allow user input or something.
    #    programs = {
    #        "anpass": "/home/megan/Programs/anpass/anpass_cerebro.x",
    #        "spectro": "/home/megan/Programs/spec3jm.ifort-00.static.x",
    #        "intder": "/home/megan/Programs/intder/Intder2005.x",
    #    }

    def setup_spectro_dir(
        self, _files_dir: str, _intder_geom_file: str, _matdisp: bool = False
    ):
        """Takes input directory with spectro.tmp, anpass.tmp and intder.tmp as well
        as location of intder.in for pts
        Makes a structured freqs directory with em
        """
        # TODO handle matdisp.pl stuff, but later
        try:
            with open(_intder_geom_file) as intder_file:
                intder_lines = intder_file.readlines()
            disp_index = [
                i for i, line in enumerate(intder_lines) if "DISP" in line
            ].pop()
            int_geom_header = intder_lines[0:disp_index]
            # TODO might need to fix spacing here
            int_geom_header.append("DISP 1")
        except:
            print("Could not open inter_geom file")

        if not os.path.exists(self.freqs_dir):
            os.makedirs(self.freqs_dir)
        with open(self.freqs_dir + "/intder_geom.in", "w") as int_geom_file:
            for line in int_geom_header:
                int_geom_file.write(line)
        self.files = {
            "anpass": _files_dir + "/anpass.tmp",
            "intder": _files_dir + "/intder.tmp",
            "spectro": _files_dir + "/spectro.tmp",
        }

        for file in self.files.values():
            shutil.copy(file, self.freqs_dir)
        if _matdisp:
            shutil.copy(_files_dir + "/matdisp.pl", self.freqs_dir)

    def make_relative_energies(self, _energy_file: str):
        """Converts energy.dat file to relative energies"""
        try:
            with open(_energy_file) as f:
                energies = [
                    float(energy.strip().split()[-1]) for energy in f.readlines()
                ]
        except:
            print("improperly formatted energy.dat file")
        self.energies = energies
        min_energy = min(energies)
        self.min_energy = min_energy
        self.relative_energies = [energy - min_energy for energy in energies]
        return self.relative_energies

    def run_anpass(self, _matdisp: bool = False):
        """Passes relative energies into anpass"""
        # paste the relative energies into the properly formatted anpass file

        # this is all to do with setting up anpass1.in
        anpass_temp = self.freqs_files["anpass"]
        anpass1_in = self.input_files["anpass1"]
        anpass1_out = self.output_files["anpass1"]
        anpass2_in = self.input_files["anpass2"]
        # anpass2_out = self.output_files["anpass2"]

        with open(anpass_temp) as anpass_temp:
            anpass_lines = [line.strip("\n") for line in anpass_temp.readlines()]

        datapoint_line_index = self.find_index(anpass_lines, "DATA POINTS")

        anpass_header = anpass_lines[0 : datapoint_line_index + 3]

        number_of_points = int(anpass_header[-2].split()[0])
        number_of_coordinates = int(anpass_header[-4])

        start_points_index = datapoint_line_index + 3
        end_points_index = number_of_points + start_points_index

        anpass_points = anpass_lines[start_points_index:end_points_index]
        # probably a better way to do this
        anpass_footer = [line for line in anpass_lines[end_points_index:] if line != ""]

        # now to start processing the points
        header_string = "\n".join(anpass_header)
        footer_string = "\n".join(anpass_footer)
        if _matdisp:
            cwd = os.getcwd()
            os.chdir(self.freqs_dir)
            with open("relE.dat", "w") as f:
                f.write("\n".join([f"{line}" for line in self.relative_energies]))
            coord_string = subprocess.run(
                "./matdisp.pl", stdout=subprocess.PIPE, text=True
            ).stdout
            os.chdir(cwd)
        else:
            anpass_coords = [
                [float(coord) for coord in line.split()[:-1]] for line in anpass_points
            ]

            for i in range(len(anpass_coords)):
                anpass_coords[i].append(self.relative_energies[i])

            coord_string_template = "%12.8f " * number_of_coordinates + "%20.12f"
            coord_string = "\n".join(
                [coord_string_template % (tuple(line)) for line in anpass_coords]
            )

        # this is where we actually write anpass1
        with open(anpass1_in, "w") as f:
            f.write(header_string)
            f.write("\n")
            f.write(coord_string)
            if not _matdisp:
                f.write("\n")
            f.write(footer_string)

        # this is where we actually run anpass
        self.run_program("anpass1")

        # now do anpass2
        with open(anpass1_out) as f:
            anpass1_lines = f.readlines()

        # find squared sum and minimum energy here to print later
        sq_sum_index = self.find_index(anpass1_lines, "SQUARED RESIDUALS IS")
        self.sq_sum = anpass1_lines[sq_sum_index].split()[-1]

        # This is all unique to anpass2
        energy_index = self.find_index(anpass1_lines, "WHERE ENERGY IS")

        self.anpass_refit_energy = float(
            anpass1_lines[energy_index].strip("\n").split()[-1]
        )
        if number_of_coordinates == 1:
            anpass_refit_coords = anpass1_lines[
                energy_index + number_of_coordinates + 2
            ].strip("\n")
        else:
            anpass_refit_coords = anpass1_lines[
                energy_index + number_of_coordinates + 1
            ].strip("\n")

        self.anpass_refit_coords = anpass_refit_coords

        # find stationary point from output file

        # handle stationary points
        anpass_footer.pop(-2)
        anpass_footer.insert(-3, "STATIONARY POINT")
        anpass_footer.insert(-3, anpass_refit_coords)

        # reform footer string
        footer_string = "\n".join(anpass_footer)

        with open(anpass2_in, "w") as f:
            f.write(header_string)
            f.write("\n")
            f.write(coord_string)
            if not _matdisp:
                f.write("\n")
            f.write(footer_string)

        # now run anpass2.out
        self.run_program("anpass2")
        # TODO split run anpass and read anpass into separate functions? yes

    def find_index(self, _list_of_lines, _search_string):
        """Gets the index of the first occurence search string for a list of lines"""
        # TODO generalize this to "find indices"?
        return [i for i, line in enumerate(_list_of_lines) if _search_string in line][0]

    def run_intder_geom(self):
        """Reads anpass2.out and runs intder_geom"""

        # TODO do this with try/except and make it more elegant as a standalone  fn
        intgeom_coords = self.anpass_refit_coords.strip().split()[:-1]

        # TODO definitely refactor this code to store all these
        intgeom_file = self.freqs_dir + "/intder_geom.in"

        with open(intgeom_file, "a") as f:
            for i, disp in enumerate(intgeom_coords):
                j = i + 1
                f.write("\n" + f"{j:5}      {disp:15}")
            f.write("\n    0")

        # with open(intgeom_file) as input_file, open(anpass2_out, "w") as out_file:
        #    subprocess.run(self.anpass_location, stdin=anpass_in, stdout=out_file)
        self.run_program("intder_geom")

        outfile = self.output_files["intder_geom"]
        with open(outfile) as f:
            geom_lines = f.readlines()
        new_geo_index = self.find_index(geom_lines, "NEW CARTESIAN GEOMETRY (BOHR)")
        self.new_geom_str = geom_lines[new_geo_index + 2 :]
        print("New geometry formed")
        # TODO separate reading and running just like for anpass

    def run_program(self, _program: str):
        """Runs a program. Accepts anpass1 or anpass2 :)"""
        input_file = self.input_files[_program]
        output_file = self.output_files[_program]
        cwd = os.getcwd()
        os.chdir(self.freqs_dir)

        if _program == "anpass1" or _program == "anpass2":
            _program = "anpass"
        elif _program == "intder_geom":
            _program = "intder"
        executable = self.programs[_program]

        if _program == "spectro":
            with open(output_file, "w") as output_file:
                executable = executable.split()
                executable.append(input_file)
                #subprocess.run([executable, input_file])
                subprocess.run(executable)
        else:
            with open(input_file) as input_file, open(output_file, "w") as output_file:
                subprocess.run(executable, stdin=input_file, stdout=output_file)
        os.chdir(cwd)

    def run_intder(self, _lin):
        """Reads intder_geom.out and runs intder"""
        temp_file = self.freqs_files["intder"]

        with open(temp_file) as f:
            temp_lines = f.readlines()

        geom_index = self.find_index(temp_lines, "GEOM")
        header = "".join(temp_lines[:geom_index])
        if _lin:
            atom_list = temp_lines[geom_index + 1:geom_index + 1 + 3]
            atom_list = "".join(atom_list)
        else:
            atom_list = temp_lines[geom_index + 1]
        new_geom = "".join(self.new_geom_str)

        infile = self.input_files["intder"]

        # hacky, do this in python (later)
        cwd = os.getcwd()
        os.chdir(self.freqs_dir)
        force_constants = ""
        force_constants = subprocess.run(
            "format.sh", stdout=subprocess.PIPE, text=True
        ).stdout
        os.chdir(cwd)
        with open(infile, "w") as f:
            f.write(header)
            f.write(new_geom)
            f.write(atom_list)
            f.write(force_constants)

        self.run_program("intder")

        print("SIC force constants transformed to Cartesian coordinates")
        # cpfort stuff

    def copy_force_constants(self):
        shutil.copy(self.freqs_dir + "/file15", self.freqs_dir + "/fort.15")
        shutil.copy(self.freqs_dir + "/file20", self.freqs_dir + "/fort.30")
        shutil.copy(self.freqs_dir + "/file24", self.freqs_dir + "/fort.40")

    #            shutil.copy(self.freqs_dir + '/spectro.tmp', self.freqs_dir + '/spectro.in')

    def run_spectro(self, _lin):
        """Reads cartesian force constants and runs spectro"""
        self.copy_force_constants()
        spectro_temp = self.freqs_files["spectro"]
        infile = self.input_files["spectro"]
        with open(spectro_temp) as f:
            spectro_lines = f.readlines()

        geom_index = self.find_index(spectro_lines, "GEOM") + 2
        end_geom_index = (
            self.find_index(spectro_lines[geom_index:], "#") + geom_index - 1
        )

        header = "".join(spectro_lines[:geom_index])
        spectro_geom = spectro_lines[geom_index : end_geom_index + 1]
        footer = "".join(spectro_lines[end_geom_index + 1 :])

        atom_numbers = [line.split()[0] for line in spectro_geom]
        new_geom = self.new_geom_str
        new_spectro_geom = []
        if _lin:
            for i, line in enumerate(atom_numbers[:-2]):
                new_spectro_geom.append("%s %s" % (line, new_geom[i]))
            new_spectro_geom.append(spectro_geom[-2])
            new_spectro_geom.append(spectro_geom[-1])
        else:
            for i, line in enumerate(atom_numbers):
                new_spectro_geom.append("%s %s" % (line, new_geom[i]))
        new_spectro_geom = "".join(new_spectro_geom)

        with open(infile, "w") as f:
            f.write(header)
            f.write(new_spectro_geom)
            f.write(footer)

        self.run_program("spectro")
        print("Spectro ran")

    def run_summarize(self):
        """Runs summarize program after spectro is output"""
        spectro_out = self.output_files["spectro"]
        summarize_out = self.output_files["summarize"]
        summarize_json = self.output_files["json"]
        with open(summarize_out, "w") as f:
            subprocess.run(["summarize", spectro_out], stdout=f)
        with open(summarize_json, "w") as f:
            subprocess.run(["summarize", "-json", spectro_out], stdout=f)

    def run_spec_to_latex(self, _theory, _molecule):
        """Does spectro to latex stuff"""
        cwd = os.getcwd()
        os.chdir(self.freqs_dir)
        summarize_json = self.output_files["json"]
        qff = panda_qff.QFF(summarize_json, _theory, _molecule)
        self.qff = qff
        #        prefix = _molecule + _theory
        #        csv_file = prefix + ".csv"
        #        tex_file = prefix + ".tex"
        #        pickle_file = prefix + ".pickle"
        csv_file = "data.csv"
        tex_file = "data.tex"
        pickle_file = "data.pickle"
        self.csv_file = csv_file
        qff.make_csv(csv_file)
        qff.print_latex(tex_file)
        with open(pickle_file, "wb") as file:
            pickle.dump(qff, file)

        os.chdir(cwd)
        print("Spec'd to latex")
        # TODO latex separate files

    def collect_misc_data(self, _theory, _lin: bool = False):
        """Tacks useful stuff to end of panda_qff csv"""
        cwd = os.getcwd()
        os.chdir(self.freqs_dir)
        zpt = "not here lol"
        if not _lin:
            zpt = self.qff.zpt
        self.csv_file = "data.csv"
        with open(self.csv_file, "a") as f:
            f.write(",\n")
            f.write(f",{_theory}\n")
            f.write(f"ZPT,{zpt}\n")
            f.write(f"anpass,{self.anpass_refit_energy}\n")
            f.write(f"minimum,{self.min_energy}\n")
            f.write(f"squared sum,{self.sq_sum}\n")
        os.chdir(cwd)

    def format_force_constants(self, _theory):
        """Tacks force constants to the end of panda_qff csv"""
        # TODO do this in python instead of calling shell script
        cwd = os.getcwd()
        os.chdir(self.freqs_dir)
        with open(self.csv_file, "a") as f:
            f.write(",\n")
            f.write(f",{_theory}\n")
        with open(self.csv_file, "a") as f:
            subprocess.run("forces_csv.sh", stdout=f)
        os.chdir(cwd)

    def auto_spec(
        self,
        _files_dir: str,
        _intder_geom_file: str,
        _energy_file: str,
        _matdisp: bool = False,
        _lin: bool = False,
    ):
        """Does the whole spectro process...automatically!!!"""
        self.setup_spectro_dir(_files_dir, _intder_geom_file, _matdisp)
        self.make_relative_energies(_energy_file)
        self.run_anpass(_matdisp)
        self.run_intder_geom()
        self.run_intder(_lin)
        self.run_spectro(_lin)
        self.run_summarize()
        # self.run_spec_to_latex()
