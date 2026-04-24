from app.utils.chunking import build_chunks, split_text
from app.utils.document_parsers import ParsedPage


def test_split_text_preserves_overlap() -> None:
    text = "A" * 1000
    chunks = split_text(text=text, chunk_size=400, overlap=100)

    assert len(chunks) == 3
    assert chunks[0][-100:] == chunks[1][:100]
    assert chunks[1][-100:] == chunks[2][:100]


def test_build_chunks_preserves_metadata() -> None:
    pages = [ParsedPage(page=3, text="B" * 950)]
    chunks = build_chunks(
        pages=pages,
        doc_id="doc-1",
        doc_name="manual.txt",
        source_type="txt",
        module="inventory",
        chunk_size=400,
        overlap=100,
    )

    assert len(chunks) == 3
    assert chunks[0].doc_id == "doc-1"
    assert chunks[0].doc_name == "manual.txt"
    assert chunks[0].source_type == "txt"
    assert chunks[0].page == 3
    assert chunks[0].module == "inventory"
