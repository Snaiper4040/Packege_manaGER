from flask import Flask, send_file
import os

app = Flask(__name__)

PACKAGES_DIR = "/repository/packages/"
PORT = 8080

@app.route('/download/<package_name>')
def download_package(package_name):
    """Отправка пакета по имени"""
    package_path = os.path.join(PACKAGES_DIR, package_name)
    
    if not os.path.exists(package_path):
        return "Package not found", 404
    
    return send_file(
        package_path,
        as_attachment=True,
        download_name=package_name
    )

if __name__ == '__main__':
    os.makedirs(PACKAGES_DIR, exist_ok=True)
    
    print(f"Starting simple file server on port {PORT}")
    print(f"Packages directory: {PACKAGES_DIR}")
    print("Usage: http://server-ip:8080/download/package-name.pger")
    
    app.run(host='0.0.0.0', port=PORT)