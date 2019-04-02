import os
from docx import Document

from flask import Flask, request, render_template
from flask_uploads import UploadSet, configure_uploads

from utils import check_jacow_styles, get_page_size, check_margins
from utils import RE_REFS, RE_FIG_INTEXT, RE_FIG_TITLES

documents = UploadSet("document", ("docx"))

app = Flask(__name__)
app.config.update(
    dict(UPLOADS_DEFAULT_DEST=os.environ.get("UPLOADS_DEFAULT_DEST", "/var/tmp"))
)

configure_uploads(app, (documents,))


@app.route("/")
def hello():
    return "Hello, World!"


@app.route("/upload", methods=["GET", "POST"])
def upload():
    if request.method == "POST" and documents.name in request.files:
        filename = documents.save(request.files[documents.name])
        full_path = documents.path(filename)
        try:
            doc = Document(full_path)
            report = []
            references = []
            figures_refs = []
            figures_titles = []
            summary = []

            report.append((check_jacow_styles(doc), "JACoW Styles"))
            report.append((True, f"Found {len(doc.sections)} sections"))

            for i, section in enumerate(doc.sections):
                report.append((True, f"Section {i} page size {get_page_size(section)}"))
                report.append((check_margins(section), f"Section {i} margins"))

            paragraph_count = 0
            for i, p in enumerate(doc.paragraphs):
                # ignore paragraphs with no text
                if p.text == '':
                    continue

                if paragraph_count == 0:
                    # title
                    report.append(
                        (
                            p.style.name == "JACoW_Paper Title",
                            f"{p.style.name} - should be JACoW_Paper Title"
                        )
                    )
                elif paragraph_count == 1:
                    # author list
                    report.append(
                        (
                            p.style.name == "JACoW_Author List",
                            f"{p.style.name} - should be JACoW_Author List"
                        )
                    )
                elif paragraph_count == 2:
                    # abstract heading
                    report.append(
                        (
                            p.style.name == "JACoW_Abstract_Heading",
                            f"{p.style.name} - should be JACoW_Abstract_Heading",
                        )
                    )

                # find reference markers in text
                for ref in RE_REFS.findall(p.text):
                    references.append(ref)

                # find figures
                for f in RE_FIG_INTEXT.findall(p.text):
                    figures_refs.append(f)
                for f in RE_FIG_TITLES.findall(p.text):
                    figures_titles.append(f)

                paragraph_count = paragraph_count+1

            return render_template(
                "upload.html",
                report=report,
                processed=filename,
                references=references,
                figures_refs=figures_refs,
                figures_titles=figures_titles,
            )
        finally:
            os.remove(full_path)

    return render_template("upload.html")