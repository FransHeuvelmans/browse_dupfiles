from browse_dupfiles.tree import Node


def test_sample_tree():
    """Create a sample tree and check its get_leaf output"""
    first = Node(name="alpha")
    second = Node(name="beta")
    second.parent = first
    first.contents.append(second)
    third = Node(name="gamma")
    third.parent = second
    second.contents.append(third)
    fourth = Node(name="delta")
    fourth.parent = third
    fifth = Node(name="epsilon")
    fifth.parent = third
    third.contents.append(fourth)
    third.contents.append(fifth)

    sample_strlst = ["alpha", "beta", "zeta"]
    assert first.name == sample_strlst[0]
    node, not_available = first._get_leaf(sample_strlst[1:])
    assert node is second
    assert not_available == ["zeta"]


def test_stringlist_tree():
    """Go from a list of strings to a tree and test contents"""
    str_list = ["start", "but", "wait", "there", "is", "more"]
    base = Node(name=str_list[0])
    base.add_children(str_list)
    is_node = base.contents[0].contents[0].contents[0].contents[0]
    assert str(is_node.contents[0]) == "more"
