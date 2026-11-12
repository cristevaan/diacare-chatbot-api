import pytest

from rag.config import RETRIEVE_K
from rag.pipeline import get_vectorstore
from rag.service import UpstreamError, answer, retrieve

QUESTIONS = [
    "Apa yang kamu tahu?",
    "Apa itu diabetes?",
    "Bagaimana cara mengelola diabetes?",
]


@pytest.fixture(scope="module")
def vectorstore():
    return get_vectorstore()


def test_retrieve(vectorstore):
    results = retrieve(QUESTIONS[1])
    assert 0 < len(results) <= RETRIEVE_K
    for doc, score in results:
        assert isinstance(doc.page_content, str)
        assert isinstance(score, float)


@pytest.mark.parametrize("question", QUESTIONS)
def test_answer(question):
    result = answer(question)
    assert isinstance(result, str)
    assert result.strip(), "jawaban kosong dari model setelah retry"


def test_answer_empty_raises(monkeypatch):
    class DummyChain:
        def __init__(self):
            self.calls = 0

        def invoke(self, query):
            self.calls += 1
            return ""

    chain = DummyChain()
    monkeypatch.setattr("rag.service.get_rag_chain", lambda: chain)
    with pytest.raises(UpstreamError):
        answer("Apa itu diabetes?")
    assert chain.calls == 2


def test_answer_retries_once(monkeypatch):
    class DummyChain:
        def __init__(self):
            self.calls = 0

        def invoke(self, query):
            self.calls += 1
            return "" if self.calls == 1 else "jawaban"

    chain = DummyChain()
    monkeypatch.setattr("rag.service.get_rag_chain", lambda: chain)
    assert answer("Apa itu diabetes?") == "jawaban"
    assert chain.calls == 2


def test_import_config_without_api_key(tmp_path):
    import os
    import subprocess
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[1]
    script = (
        "import os\n"
        "os.environ.pop('GROQ_API_KEY', None)\n"
        "import dotenv\n"
        "dotenv.load_dotenv = lambda *a, **k: None\n"
        "import rag.config\n"
    )
    env = {k: v for k, v in os.environ.items() if k != "GROQ_API_KEY"}
    env["PYTHONPATH"] = str(repo_root)
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr
