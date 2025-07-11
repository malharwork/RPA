import os
import subprocess
import sys

def install_system_dependencies():
    """Install system-level dependencies"""
    print("Installing system dependencies...")
    
    # Update package list
    os.system("sudo apt update")
    
    # Install required packages
    packages = [
        "python3-pip",
        "python3-venv", 
        "tesseract-ocr",
        "tesseract-ocr-eng",
        "libopencv-dev",
        "python3-opencv",
        "poppler-utils"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        os.system(f"sudo apt install -y {package}")

def create_virtual_environment():
    """Create and setup virtual environment"""
    print("Creating virtual environment...")
    
    # Create virtual environment
    subprocess.run([sys.executable, "-m", "venv", "rpa_env"])
    
    # Activate and install packages
    activate_script = "rpa_env/bin/activate"
    if os.path.exists(activate_script):
        print("Virtual environment created successfully!")
        print("To activate: source rpa_env/bin/activate")
        return True
    else:
        print("Failed to create virtual environment")
        return False

def install_python_packages():
    """Install Python packages"""
    print("Installing Python packages...")
    
    packages = [
        "pandas==2.1.4",
        "openpyxl==3.1.2", 
        "PyPDF2==3.0.1",
        "pytesseract==0.3.10",
        "Pillow==10.1.0",
        "opencv-python==4.8.1.78",
        "python-docx==1.1.0",
        "requests==2.31.0",
        "beautifulsoup4==4.12.2",
        "schedule==1.2.0",
        "python-dateutil==2.8.2"
    ]
    
    for package in packages:
        print(f"Installing {package}...")
        subprocess.run([sys.executable, "-m", "pip", "install", package])

def create_sample_data():
    """Create sample test data"""
    print("Creating sample test data...")
    
    # Create sample PO files
    sample_po1 = """PURCHASE ORDER

Customer: ABC Manufacturing Corp
Date: 2024-01-15

Item Description: Red Steel Widget 10kg
Quantity: 50
Unit Price: $25.00

Total: $1,250.00

Delivery Address:
123 Industrial Ave
Manufacturing District
"""

    sample_po2 = """Purchase Order #PO-2024-002

Client: XYZ Industries Ltd  
Order Date: January 20, 2024

Product: Blue Aluminum Component 5kg
Qty: 25 units
Price per unit: $45.00

Total Amount: $1,125.00

Ship to:
456 Factory Road
Industrial Zone
"""

    # Write sample files
    os.makedirs("data/input", exist_ok=True)
    
    with open("data/input/sample_po_2.txt", "w") as f:
        f.write(sample_po2)
    
    print("Sample PO files created in data/input/")

def main():
    """Main setup function"""
    print("=" * 60)
    print("🤖 RPA POC Setup - Python Implementation")
    print("=" * 60)
    
    choice = input("\nSelect setup option:\n1. Full setup (system + Python packages)\n2. Python packages only\n3. Create sample data only\nEnter choice (1-3): ")
    
    if choice == "1":
        install_system_dependencies()
        create_virtual_environment()
        install_python_packages()
        create_sample_data()
        print("\n✅ Full setup completed!")
        print("Next steps:")
        print("1. source rpa_env/bin/activate")
        print("2. python main.py")
        
    elif choice == "2":
        install_python_packages()
        create_sample_data()
        print("\n✅ Python setup completed!")
        
    elif choice == "3":
        create_sample_data()
        print("\n✅ Sample data created!")
        
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()