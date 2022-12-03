"""Console script for qff_helper."""
import sys
import click
import qff_utils.qff_helper.qff_helper as qffh


@click.command()
@click.argument("files_dir")
@click.argument("intder_geom_file")
@click.argument("energy_dat")
@click.argument("molecule")
@click.argument("theory")
@click.argument("freqs_dir", default="freqs")
@click.option(
    "--matdisp",
    is_flag=True,
    default=False,
    help="uses matdisp for anpass mostly for HNCO",
)
@click.option(
    "--lin",
    is_flag=True,
    default=False,
    help="skip a step for linear molecules until I stop being lazy",
)
@click.option(
    "--eland",
    is_flag=True,
    default=False,
    help="points to right program paths for eland",
)
def main(
    files_dir,
    intder_geom_file,
    energy_dat,
    molecule,
    theory,
    freqs_dir,
    matdisp,
    lin,
    eland,
):
    """Console script for qff_helper."""
    helper = qffh.QffHelper(freqs_dir, eland)
    helper.auto_spec(files_dir, intder_geom_file, energy_dat, matdisp, lin)
    if not lin:
        helper.run_spec_to_latex(theory, molecule)
    helper.collect_misc_data(theory, lin)
    helper.format_force_constants(theory)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
