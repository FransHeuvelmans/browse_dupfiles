from browse_dejadup.tree import Node

def test_sample_tree():
    """Create a sample tree and check its get_leaf output"""
    first = Node(name="alpha")
    second = Node(name="beta", parent=first)
    first.contents.append(second)
    third = Node(name="gamma", parent=second)
    second.contents.append(third)
    fourth = Node(name="delta", parent=third)
    fifth = Node(name="epsilon", parent=third)
    third.contents.append(fourth)
    third.contents.append(fifth)


    sample_strlst = ["alpha", "beta", "zeta"]
    assert first.name == sample_strlst[0]
    node, not_available = first.get_leaf(sample_strlst[1:])
    assert node is second
    assert not_available == ["zeta"]