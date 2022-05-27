from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import findPath

app = Flask(__name__)

# create an upload folder
# app.config['UPLOAD_FOLDER'] = 'uploads/'

app.config['ALLOWED_FILE_EXTENSIONS'] = ['TSV']


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[-1].upper() in app.config['ALLOWED_FILE_EXTENSIONS']


@app.route('/', methods=['GET', 'POST'])
def file_uploader(output=''):
    # error = None

    if request.method == 'POST':

        # f = request.files['file']
        files = request.files.getlist("file[]")
        fileSort = {}
        for f in files:

            if f.filename == '':
                output = 'No filename.'
                return render_template('upload.html', error=output)

            if allowed_file(f.filename):
                # sort files
                name = f.filename.rsplit('_')[1]
                if name in fileSort:
                    fileSort[name].append(f.filename)
                else:
                    fileSort[name] = [f.filename]
                # filename = secure_filename(f.filename)
                # f.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                f.save(secure_filename(f.filename))

            else:
                output = 'The file extension is not allowed.'
                return render_template('upload.html', error=output)

        output += '<div class="container"><table class="table"> <thead><tr><th>Name</th><th>Length</th><th>Assembly</th></tr></thead><tbody>'

        for name, f in fileSort.items():
            # generate html result
            path = findPath.path(f)
            # turn result into html code then pass into template
            count = 0
            for i in path:
                count += 1
                output += '<tr class="table-info"><td>'
                if count == 1:
                    output += name
                output += '</td><td>'
                output += str(i[0])
                output += '</td><td>' + i[1] + '</td></tr>'
                for j in range(len(i)-2):
                    output += '<tr class="table-info"><td></td><td></td><td>' + \
                        i[j+2] + '</td></tr>'
        output += '</tbody></table></div>'

    return render_template('upload.html', result=output)


@app.route('/output/')
def output():
    return render_template('output.html')


if __name__ == '__main__':
    app.run(debug=True)
