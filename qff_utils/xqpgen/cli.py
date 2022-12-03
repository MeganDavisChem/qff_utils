"""Console script for xqpgen."""
import sys
import click


@click.command()
@click.option("--mol_name",'-M',required=True)
@click.option("--qff_type",'-q',required=True)
@click.option("--target_sym", '-t', required=True)
@click.option("--eom_type", '-e', required=True)
@click.option("--base_method", '-b', required=True)
@click.option("--charge", "-c", default="0", help="charge of molecule")
@click.option("--multiplicity", "-m", default="1", help="multiplicity")
@click.option(
    "--program",
    default="CFOUR",
    help="PSI4 or CFOUR for now, must be sane for qff type",
)
@click.option("--run_intder", default=False, help="Run intder, work in progress")
@click.option(
    "--highest_root",
    "-hr",
    default=1,
    help="highest root sym, only relevant for CO+ second sigma state so far",
)
def main(
    mol_name,
    qff_type,
    target_sym,
    eom_type,
    base_method,
    charge,
    multiplicity,
    program,
    run_intder,
    highest_root,
):
    import qff_utils.xqpgen.xqpgen as xqpgen

    xqpgen.points_driver(
        True,
        mol_name=mol_name,
        qff_type=qff_type,
        target_sym=target_sym,
        eom_type=eom_type,
        base_method=base_method,
        charge=charge,
        multiplicity=multiplicity,
        program=program,
        run_intder=run_intder,
        highest_root=highest_root,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
