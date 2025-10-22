from jarvis.tools import filesystem

def test_filesystem_write_and_read(tmp_path):
    f = tmp_path / "hello.txt"
    filesystem.write(path=str(f), text="Hola mundo")
    content = filesystem.read(path=str(f))
    assert "Hola" in content["text"]
