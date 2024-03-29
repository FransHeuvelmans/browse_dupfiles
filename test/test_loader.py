from browse_dupfiles import loader


def test_line_processing():
    """See if important log file-lines are properly split up"""
    testin = "Tue Oct  9 19:23:01 2012 alpha/beta/gamma/delta/epsilon/zeta/eta/theta"
    testout = loader.process_line(testin)
    assert testout == [
        "alpha",
        "beta",
        "gamma",
        "delta",
        "epsilon",
        "zeta",
        "eta",
        "theta",
    ]

    testin = "  Sun  Jul   9 15:22:39 1970 a/b/c/d"
    testout = loader.process_line(testin)
    assert testout == ["a", "b", "c", "d"]


def test_loadfile():
    """Try use a simple testfile and check the contents"""
    num, head_node = loader.load_file("testload.txt")
    assert num == 16

    assert head_node.name == "home"
    x_node = head_node.contents[0]  # Should load the lines in order
    assert str(x_node) == "x"
    y_node = x_node.contents[0]
    assert str(y_node) == "y"
    z_node = x_node.contents[1]
    assert str(z_node) == "z"
    assign1_node = z_node.contents[0].contents[0].contents[0]
    assert str(assign1_node.contents[0]) == "2"
