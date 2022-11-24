import argparse
import yaml
from pathlib import Path
from roomgraph.data.cubicasa5k import Cubicasa5k

def test(config):
    test_dir = Path(config['test_dir'])
    test_paths = (test_dir / 'test.txt').read_text().splitlines()
    test_paths = [test_dir / Path(p[1:]) for p in test_paths]

    dataset = Cubicasa5k(test_paths, config['buffer_pct'])
    for path, graph in zip(test_paths, iter(dataset)):
        case = path.name
        print(f"Testing {case}")
        match case:
            case 'fully-connected':
                # Make sure number of nodes/edges lines up with expected
                assert graph.num_edges == 2
                assert graph.num_nodes == 2
                # Make sure first room comes through correctly
                assert graph.x[0,0] == 10_000
                assert graph.x[0,1] == 100
                assert graph.x[0,2] == 100
                assert graph.x[0,3] == 0
            case 'partially-connected':
                # Make sure number of nodes/edges lines up with expected
                # (3 rooms, but only 2 are connected)
                assert graph.num_edges == 2
                assert graph.num_nodes == 3
            case 'with-doors':
                assert graph.num_edges == 2
                assert graph.num_nodes == 2
                # Make sure both rooms find the associated door
                assert graph.x[0,3] == 1
                assert graph.x[1,3] == 1
            case _:
                raise ValueError(f"Unknown test case: {case}")


if __name__ == "__main__":
    config_path = Path('config/data-params.yaml')
    config = yaml.safe_load(config_path.open())

    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['train', 'test'], type=str)

    args, _ = parser.parse_known_args()
    match args.action:
        case "train":
            raise NotImplementedError()
        case "test":
            test(config)