import os
from unittest import TestCase

from tests.base_test_cases import AlgorithmsBaseTestCase
from reactea.case_studies.compound_quality import CompoundQuality
from reactea.io_streams import Loaders, Writers
from reactea.optimization.jmetal.ea import ChemicalEA


class TestSOAlgorithms(AlgorithmsBaseTestCase, TestCase):

    def run_algorithm(self, algorithm):
        # set up algorithm
        self.configs['algorithm'] = algorithm
        self.configs['multi_objective'] = False

        # set up output folder
        self.output_folder = self.output_folder / algorithm
        self.configs['output_dir'] = self.output_folder

        # define number of molecules to use to only 1 in the case of RandomSearch
        if algorithm in ['SA', 'LS']:
            self.configs['init_pop_size'] = 1

        # initialize population and initialize population smiles
        init_pop, init_pop_smiles = Loaders.initialize_population(self.configs)
        self.assertEqual(len(init_pop), self.configs['init_pop_size'])
        self.assertEqual(len(init_pop_smiles), self.configs['init_pop_size'])

        # case study
        case_study = CompoundQuality(init_pop_smiles, self.configs)

        # set up objective
        objective = case_study.objective

        # initialize reaction rules
        reaction_rules = Loaders.initialize_rules()

        # set up folders
        Writers.set_up_folders(self.output_folder)

        # initialize objectives
        problem = objective()

        # Initialize EA
        ea = ChemicalEA(self.configs['algorithm'], problem, initial_population=init_pop, reaction_rules=reaction_rules,
                        max_generations=self.configs['generations'], visualizer=False, configs=self.configs)

        # Run EA
        final_pop = ea.run()
        self.assertIsInstance(final_pop, list)

        # Save population
        Writers.save_final_pop(final_pop, self.configs, case_study.feval_names())
        # Save Transformations
        Writers.save_intermediate_transformations(final_pop, self.configs)

        # save configs
        Writers.save_configs(self.configs)

    def test_algorithms(self):
        self.run_algorithm('NSGAIII')
        self.run_algorithm('NSGAII')
        self.run_algorithm('SPEA2')
        self.run_algorithm('IBEA')
        self.run_algorithm('SA')
        self.run_algorithm('GA')
        self.run_algorithm('ES')
        self.run_algorithm('LS')
