"""Console script for spec2latex."""
import sys
import click
import qff_utils.spec2latex.panda_qff as pq
import pickle
import subprocess


@click.command()
@click.argument("theory")
@click.argument("molecule")
@click.option("--json", is_flag=True, default=True, help="runs summarize")
@click.option("--csv", is_flag=True, default=True, help="makes a csv file")
@click.option("--tex", is_flag=True, default=True, help="makes tex file")
@click.option("--texsep", is_flag=True, default=False, help="makes sep tex files")
@click.option(
    "--preserve", is_flag=True, default=True, help="pickles data frame for later"
)
def main(theory, molecule, json, csv, tex, texsep, preserve):
    """Console script for spec2latex."""
    if json:
        with open("spectro2.json", "w") as json_file:
            spec_file = subprocess.Popen(
                ["summarize", "-json", "spectro2.out"], stdout=json_file
            ).wait()
    with open("spectro2.sum", "w") as sum_file:
        spec_file2 = subprocess.Popen(
            ["summarize", "spectro2.out"], stdout=sum_file
        ).wait()
    qff_data = pq.QFF("spectro2.json", theory, molecule)
    if csv:
        output_file = molecule + theory + ".csv"
        qff_data.make_csv(output_file)
    if preserve:
        pickle_file = molecule + theory + ".pickle"
        with open(pickle_file, "wb") as file:
            pickle.dump(qff_data, file)
    if tex:
        tex_file = molecule + theory + ".tex"
        qff_data.print_latex(tex_file)
    if texsep:
        tex_prefix = molecule + theory
        qff_data.print_latex(tex_prefix)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
