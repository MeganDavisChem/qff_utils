import qff_helper


helper = qff_helper.QffHelper('onepiecsde')
helper.auto_spec('example_files/hcf/files/freqs', 'example_files/hcf/pts/intder.in', 'example_files/energy.dat')
helper.run_spec_to_latex('f12-tz', 'h2o+')

#helper.setup_spectro_dir('example_files/hcf/files/freqs/', 'example_files/hcf/pts/intder.in')
#
#helper.make_relative_energies('example_files/energy.dat')
#
#helper.run_anpass()
#helper.run_intder_geom()
#helper.run_intder()
#helper.run_spectro()

