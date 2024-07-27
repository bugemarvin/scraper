from flask import Flask, request, send_file, render_template, jsonify, redirect, url_for # Import necessary modules from Flask
import scraper  # Ensure the module name matches the file name accurately to avoid import errors like ModuleNotFoundError according to PEP 8
import os # Import the os module to handle file paths

app = Flask(__name__) # Initialize the Flask app

def clean_url(url):
    # Remove trailing slashes from the URL
    return url.rstrip('/')

@app.route('/')
def index():
    error = request.args.get('error') # Get the error message from the query parameters
    return render_template('index.html', error=error) # Render the index.html template with the error message

@app.route('/process', methods=['POST'])
def process():
    url = request.form.get('url') # Get the URL from the form data
    num_pages = int(request.form.get('num_pages', 1)) # Get the number of pages from the form data
    file_format = request.form.get('file_format', 'csv')  # Default to 'csv' if not specified
    
    url = clean_url(url) # Clean the URL by removing trailing slashes
    print(f'URL: {url}, Num Pages: {num_pages}, File Format: {file_format}') # Print the URL, number of pages, and file format

    driver = scraper.init_driver() # Initialize the driver
    try:
        print("Collecting palette data from the specified URL...")
        palette_data = scraper.collect_palette_data(driver, url, num_pages) # Collect palette data
        if not palette_data:
            # Redirect to index with an error message if no palette data is found
            return redirect(url_for('index', error='No palette data found.'))

        # Save data based on file format
        try:
            filename = f"palette_data.{file_format}" # Set the filename based on the file format
            file_path = os.path.join('data', filename) # Set the file path
            scraper.save_data(palette_data, file_path) # Save the data to the file
        except ValueError as e:
            # Redirect to index with an error message if an error occurs during saving
            return redirect(url_for('index', error=str(e)))

        # Return the file for download
        return send_file(file_path, as_attachment=True)

    finally:
        # Quit the driver after processing
        driver.quit()

if __name__ == "__main__":
    # Run the Flask app in debug mode
    app.run(debug=True)
