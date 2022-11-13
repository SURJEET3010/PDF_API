from flask import Flask
import PyPDF2
import os

appFlask = Flask(__name__)


@appFlask.route("/")
def index():
    return "<h2> To rotate pdf enter <br>file_path,<br> page_no and <br> angle of rotation in url </h2>"


@appFlask.route('/<path:file_path>/<int:n>/<int:angle_of_rotation>', methods=["GET"])
def Rotate_pdf(file_path, n, angle_of_rotation):
    file_path = file_path.replace("'/'", "'\\'")

    # checking the file extention
    if file_path.rsplit('.', 1)[1].lower() != "pdf":
        return "File must be pdf !"

    # creating a pdf File object of original pdf
    pdfFileObj = open(file_path, 'rb')

    # creating a pdf Reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    # if given page number is greater than all pages
    if pdfReader.numPages < n - 1 or angle_of_rotation%90 != 0 :
        return "Invalid page number or angle"


    # creating a pdf writer object for new pdf
    pdfWriter = PyPDF2.PdfFileWriter()

    # rotating the desired page
    for page in range(pdfReader.numPages):
        # creating rotated page object
        if page == n - 1:
            pageObj = pdfReader.getPage(page)
            pageObj.rotateClockwise(angle_of_rotation)
        else:
            pageObj = pdfReader.getPage(page)

        # adding each page object to pdf writer
        pdfWriter.addPage(pageObj)

    # name of output file
    newFilename = "RotatedFile.pdf"

    # new pdf file object
    outputFile = open(newFilename, 'wb')

    path = "\\".join([os.getcwd(), newFilename])

    # writing rotated pages to new file
    pdfWriter.write(outputFile)

    # closing the original pdf file object
    pdfFileObj.close()

    # closing the new pdf file object
    outputFile.close()

    return path


if __name__ == "__main__":
    appFlask.run(debug=True)

