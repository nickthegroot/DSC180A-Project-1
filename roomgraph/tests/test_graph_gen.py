from .. import consts as Consts
from ..data.util import generate_graph


def test_graph_gen_fc():
    model_path = Consts.TEST_DATA_DIR / "fully-connected"
    graph = generate_graph(model_path, 0.03)

    # Make sure number of nodes/edges lines up with expected
    assert graph.num_edges == 2
    assert graph.num_nodes == 2
    # Make sure first room comes through correctly
    assert graph.x[0, 0] == 10_000
    assert graph.x[0, 1] == 100
    assert graph.x[0, 2] == 100
    assert graph.x[0, 3] == 0


def test_graph_gen_partially_connected():
    model_path = Consts.TEST_DATA_DIR / "partially-connected"
    graph = generate_graph(model_path, 0.03)

    # Make sure number of nodes/edges lines up with expected
    # (3 rooms, but only 2 are connected)
    assert graph.num_edges == 2
    assert graph.num_nodes == 3


def test_graph_gen_with_doors():
    model_path = Consts.TEST_DATA_DIR / "with-doors"
    graph = generate_graph(model_path, 0.03)

    assert graph.num_edges == 2
    assert graph.num_nodes == 2
    # Make sure both rooms find the associated door
    assert graph.x[0, 3] == 1
    assert graph.x[1, 3] == 1


def test_graph_gen_non_square():
    model_path = Consts.TEST_DATA_DIR / "non-square"
    graph = generate_graph(model_path, 0.03)

    assert graph.x[0, 0] == 50 * 100
    assert graph.x[0, 1] == 100
    assert graph.x[0, 2] == 50
