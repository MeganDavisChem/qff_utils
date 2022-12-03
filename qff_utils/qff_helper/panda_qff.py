"""Defines QFF class. Probably won't do anything else in this file. Really it's
just practice"""
import json
import itertools
#import pandas as pd
from pandas import DataFrame 
from pandas import concat 
from pandas import MultiIndex


class QFF:
    """QFF class etc"""

    def __init__(self, inp, theory, molecule):
        with open(inp, encoding="utf-8") as file:
            self.summarize_data = json.loads(file.read())
            self.zpt = self.summarize_data["ZPT"]
            self.theory = theory
            self.molecule = molecule

            for rots in self.summarize_data["Rots"]:
                rots.sort(reverse=True)
            self.make_headers()

            self.summarize_data["Deltas"], delta_column = self.distortion_units(
                "Deltas"
            )
            self.summarize_data["Phis"], phi_column = self.distortion_units("Phis")

            # Make list of JSON data we need
            rot_list = list(itertools.chain(*self.summarize_data["Rots"]))
            labels = ["Harm", "Fund", "Deltas", "Phis", "Ralpha"]
            mappings = [self.summarize_data[label] for label in labels]
            mappings.append(rot_list)

            # Convert JSON data to DataFrame and store in dict (might change this
            # later)
            keys = ["harm", "anharm", "deltas", "phis", "geos", "rots"]
            self.frames = {}
            for i, key in enumerate(keys):
                self.frames[key] = DataFrame(
                    mappings[i], columns=[theory], index=self.headers[i]
                )

            self.frames["deltas"].insert(0, "units", delta_column)
            self.frames["phis"].insert(0, "units", phi_column)
            self.frames["dis"] = concat([self.frames["deltas"], self.frames["phis"]])
            del self.frames["phis"]
            del self.frames["deltas"]

            self.frames["rots"] = self.wvnum_to_mhz(self.frames["rots"])

    @staticmethod
    def wvnum_to_mhz(frame):
        """Converts dataframe from cm-1 to MHz"""
        conv_factor = 29979.2458
        return frame.mul(conv_factor)

    def distortion_units(self, const_set):
        """Figure out right units for distortion constants"""
        # I'm just copying Brent's way of doing this
 #       units = {"GHz": 1e-9, "MHz": 1e-6, "kHz": 1e-3, "Hz": 1.0, "mHz": 1e3}
        units = {"GHz": 1e-3, "MHz": 1.0, "kHz": 1e3, "Hz": 1.0e6, "mHz": 1e9}
        new_units = []
        unit_column = []
        for i, discon in enumerate(self.summarize_data[const_set]):
            for unit in units.items():
                new_con = f"{discon*unit[1]:.3f}"
                l = len(new_con)
                if l > 4 and abs(float(new_con)) >= 1.0 and l <= 7:
                    new_con = float(new_con)
                    new_units.append(new_con)
                    unit_column.append(unit[0])
                    break
        return new_units, unit_column

    def join_qff(self, second_qff):
        """Joins QFFs together"""
        # TODO find a better way to manage distortion unit merging
        for key in second_qff.frames:
            self.frames[key] = self.frames[key].join(
                second_qff.frames[key], rsuffix=second_qff.theory
            )

    def stack_vibs(self):
        """Stacks vibs, should probably call this in constructor"""
        self.frames["vibs"] = concat([self.frames["harm"], self.frames["anharm"]])

    def make_csv(self, output_file):
        """Prints a spreadsheet friendly csv :)"""
        with open(output_file, "w", encoding="utf-8") as output:
            for item in self.frames.items():
                csv_item = item[1].to_csv()
                output.write(csv_item)

    def print_latex(self, output_file):
        """Prints tables as one file"""
        with open(output_file, "w", encoding="utf-8") as output:
            for item in self.frames.items():
                styled_frame = self._style_latex(item[1], item[0])
                #                latex_frame = styled_frame.to_latex(environment="table")
                latex_frame = self._style_to_latex(styled_frame, self.molecule, item[0])
                output.write(latex_frame)

    def print_latex_sep(self, output_prefix="fixme"):
        """Prints tables as separate files"""
        # TODO give optional prefix and make default the molecule name
        for item in self.frames.items():
            table_file = output_prefix + "_" + item[0] + ".tex"
            with open(table_file, "w", encoding="utf-8") as output:
                styled_frame = self._style_latex(item[1], item[0])
                latex_frame = self._style_to_latex(styled_frame, self.molecule, item[0])
                output.write(latex_frame)

    #    @staticmethod
    def _style_to_latex(self, styled_frame, molecule, table_contents):
        """This will handle the latex options, environment etc, centering for
        long tables"""
        table_label = molecule + "_" + table_contents
        if table_contents == "harm":
            cap = "Harmonic Frequencies in cm$^{-1}$"
        elif table_contents == "anharm":
            cap = "Anharmonic Frequencies in cm$^{-1}$"
        elif table_contents == "rots":
            cap = "Rotational Constants in MHz"
        elif table_contents == "dis":
            cap = "Distortion Constants"
        elif table_contents == "geos":
            cap = "Geometrical Parameters in \AA~and degrees"
        else:
            cap = ""
        table_caption = molecule + " " + cap

        frame_dimensions = self.frames[table_contents].shape
        if frame_dimensions[0] > 30:
            table_environment = "longtable"
            latex_frame = styled_frame.to_latex(
                environment=table_environment,
                hrules=True,
                # position_float="centering",
                label=table_label,
                caption=table_caption,
            )
        else:
            table_environment = "table"
            latex_frame = styled_frame.to_latex(
                environment=table_environment,
                hrules=True,
                position_float="centering",
                label=table_label,
                caption=table_caption,
            )

        return latex_frame

    def _style_latex(self, frame_to_style, table_contents):
        """Styles LaTex tables. May add options later"""
        styled_frame = frame_to_style.style
        # Adds escape characters to indices
        #        styled_frame.format_index(escape="latex", axis=1)
        #        styled_frame.format_index(escape="latex", axis=0)
        if table_contents == "harm":
            table_precision = 1
        elif table_contents == "anharm":
            table_precision = 1
        elif table_contents == "rots":
            table_precision = 1
        elif table_contents == "dis":
            table_precision = 3
        elif table_contents == "geos":
            table_precision = 3
        else:
            table_precision = 1
        styled_frame.format(precision=table_precision)
        return styled_frame

    def make_multicolumns(self, multicol_header, cols):
        """WIP, don't use yet. Should probably call this in _style_latex?"""
        for item in self.frames.items():
            item[1].columns = MultiIndex.from_tuples(
                [(multicol_header, cols[0]), (multicol_header, cols[1])]
            )

    def make_headers(self):
        """Forms headers needed"""
        dofs = [index + 1 for index in range(len(self.summarize_data["Harm"]))]

        # Form all headers for data frames
        delta_headers = [
            "$\Delta_J$",
            "$\Delta_K$",
            "$\Delta_{JK}$",
            "$\delta_j$",
            "$\delta_k$",
        ]
        phi_headers = [
            "$\Phi_J$",
            "$\Phi_K$",
            "$\Phi_{JK}$",
            "$\Phi_{KJ}$",
            "$\phi_j$",
            "$\phi_{jk}$",
            "$\phi_k$",
        ]
        harm_headers = []
        anharm_headers = []
        rot_headers = ["A$_0$", "B$_0$", "C$_0$"]
        #        geo_headers = self.summarize_data["Rhead"]
        geo_headers = self.make_geo_headers()
        for index in dofs:
            harm_headers.append(f"$\omega_{{{index}}}$")
            anharm_headers.append(f"$\\nu_{{{index}}}$")
            for letter in ["A", "B", "C"]:
                rot_headers.append(f"{letter}$_{index}$")
        self.headers = [
            harm_headers,
            anharm_headers,
            delta_headers,
            phi_headers,
            geo_headers,
            rot_headers,
        ]

    def make_geo_headers(self):
        geo_headers = []
        # TODO check if torsions need to be handled differently
        for header in self.summarize_data["Rhead"]:
            split_header = header.rstrip(")").split("(")
            if split_header[0] == "<":
                split_header[0] = "$\\angle$"
            elif split_header[0] == "r":
                split_header[0] = "r$_0$"
            header = split_header[0] + "(" + split_header[1] + ")"
            geo_headers.append(header)
        return geo_headers


# class LinQFF(QFF):
# """Special handling for linear molecules, will figure out later"""
