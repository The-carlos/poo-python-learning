from dinodex.cli.main import main

def test_cli_main_runs(capsys):
    main()
    captured = capsys.readouterr()
    assert "hello world" in captured.out.lower()
