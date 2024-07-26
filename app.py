from flask import Flask, request, send_file, render_template, jsonify, redirect, url_for
import scraper  # Ensure the module name matches the file name
import os

app = Flask(__name__)

def clean_url(url):
    # Remove trailing slashes from the URL
    return url.rstrip('/')

@app.route('/')
def index():
    error = request.args.get('error')
    return render_template('index.html', error=error)

@app.route('/process', methods=['POST'])
def process():
    url = request.form.get('url')
    num_pages = int(request.form.get('num_pages', 1))
    file_format = request.form.get('file_format', 'csv')  # Default to 'csv' if not specified
    
    url = clean_url(url)
    print(f'URL: {url}, Num Pages: {num_pages}, File Format: {file_format}')

    driver = scraper.init_driver()
    try:
        print("Collecting palette data from the specified URL...")
        palette_data = scraper.collect_palette_data(driver, url, num_pages)
        if not palette_data:
            # Redirect to index with an error message if no palette data is found
            return redirect(url_for('index', error='No palette data found.'))

        # Save data based on file format
        try:
            filename = f"palette_data.{file_format}"
            file_path = os.path.join('data', filename)
            scraper.save_data(palette_data, file_path)
        except ValueError as e:
            return redirect(url_for('index', error=str(e)))

        return send_file(file_path, as_attachment=True)

    finally:
        driver.quit()

if __name__ == "__main__":
    app.run(debug=True)
