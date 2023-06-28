from types import SimpleNamespace


configs = SimpleNamespace(**{})
configs.dataset_dir = "../../datasets"
configs.results_dir = "../../results"
configs.ckpt_dir = "../../checkpoints"
configs.dataset_name = "oxford_pets"

configs.random_seed = 42