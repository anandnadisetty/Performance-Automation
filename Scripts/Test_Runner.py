import subprocess
from Scripts.token_generator import generate_token
from Scripts.jmx_creator import create_jmx
from config.config import JMX_FILE_PATH  # Import JMX file path from your configuration


def run_tests():
    # Step 1: Generate Bearer Token
    token = generate_token()
    if not token:
        print("Test execution aborted due to token generation failure.")
        return

    print("Bearer Token generated successfully.")

    # Step 2: Create or update the JMX file with the generated token
    try:
        create_jmx()  # Pass the token to the create_jmx function if needed
        print(f"JMX file created at {JMX_FILE_PATH} with the dynamic token.")
    except Exception as e:
        print(f"Failed to create JMX file: {e}")
        return

    # Step 3: Run the JMeter test plan using subprocess
    try:
        result = subprocess.run([
            r"C:\EndPointCentral\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat",
            # Path to your JMeter executable
            "-n",  # Non-GUI mode
            "-t", JMX_FILE_PATH,  # Path to the JMX test plan
            "-l", "C:/Users/AnandNadisetty/Documents/results.jtl",  # Log file for test results
            "-e",  # Enable report generation
            "-o", "C:/Users/AnandNadisetty/Documents/newhtmlreport"  # Output folder for HTML report
        ], check=True)

        if result.returncode == 0:
            print("JMeter test executed successfully.")
        else:
            print(f"JMeter test execution failed with return code {result.returncode}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while executing JMeter: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    run_tests()
