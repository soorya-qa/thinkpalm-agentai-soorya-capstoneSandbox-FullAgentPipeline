import os
import sys

def main():
    print("Starting AI Test Automation Pipeline...")
    # Entry point simply kicks off the Streamlit UI
    os.system(f"{sys.executable} -m streamlit run ui/app.py")

if __name__ == "__main__":
    main()
