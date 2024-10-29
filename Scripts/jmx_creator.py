import xml.etree.ElementTree as ET
from config.config import JMX_FILE_PATH
from Scripts.token_generator import generate_token  # Import the token generator

def create_jmx():
    # Generate the Bearer token
    bearer_token = generate_token()

    if bearer_token is None:
        print("Failed to generate the Bearer token. Exiting.")
        return  # Exit if token generation fails

    print(f"Generated Bearer Token: {bearer_token}")  # Debug: Print the generated token

    # Create the root element for the JMeter test plan
    jmeter_test_plan = ET.Element("jmeterTestPlan", {
        "version": "1.2",
        "properties": "5.0",
        "jmeter": "5.6.3"
    })
    hash_tree_root = ET.SubElement(jmeter_test_plan, "hashTree")

    # Test Plan
    test_plan = ET.SubElement(hash_tree_root, "TestPlan", {
        "guiclass": "TestPlanGui",
        "testclass": "TestPlan",
        "testname": "Test Plan",
        "enabled": "true"
    })
    ET.SubElement(test_plan, "stringProp", {"name": "TestPlan.comments"}).text = ""
    ET.SubElement(test_plan, "boolProp", {"name": "TestPlan.functional_mode"}).text = "false"
    ET.SubElement(test_plan, "boolProp", {"name": "TestPlan.serialize_threadgroups"}).text = "false"
    ET.SubElement(test_plan, "elementProp", {
        "name": "TestPlan.user_defined_variables",
        "elementType": "Arguments",
        "guiclass": "ArgumentsPanel",
        "testclass": "Arguments",
        "testname": "User Defined Variables",
        "enabled": "true"
    })
    test_plan_user_defined_vars = ET.SubElement(test_plan, "collectionProp", {"name": "Arguments.arguments"})
    argument_element = ET.SubElement(test_plan_user_defined_vars, "elementProp", {
        "name": "",
        "elementType": "Argument"
    })
    ET.SubElement(argument_element, "stringProp", {"name": "Argument.name"}).text = "BearerToken"
    ET.SubElement(argument_element, "stringProp", {"name": "Argument.value"}).text = bearer_token
    ET.SubElement(argument_element, "stringProp", {"name": "Argument.metadata"}).text = "="

    test_plan_hash_tree = ET.SubElement(hash_tree_root, "hashTree")

    # Thread Group
    thread_group = ET.SubElement(test_plan_hash_tree, "ThreadGroup", {
        "guiclass": "ThreadGroupGui",
        "testclass": "ThreadGroup",
        "testname": "Thread Group",
        "enabled": "true"
    })
    ET.SubElement(thread_group, "stringProp", {"name": "ThreadGroup.num_threads"}).text = "1"
    ET.SubElement(thread_group, "stringProp", {"name": "ThreadGroup.ramp_time"}).text = "1"
    ET.SubElement(thread_group, "stringProp", {"name": "ThreadGroup.duration"}).text = "60"
    ET.SubElement(thread_group, "boolProp", {"name": "ThreadGroup.scheduler"}).text = "false"

    # Add the main controller to the Thread Group
    main_controller = ET.SubElement(thread_group, "elementProp", {
        "name": "ThreadGroup.main_controller",
        "elementType": "LoopController",
        "guiclass": "LoopControlPanel",
        "testclass": "LoopController",
        "testname": "Loop Controller",
        "enabled": "true"
    })
    ET.SubElement(main_controller, "boolProp", {"name": "LoopController.continue_forever"}).text = "false"
    ET.SubElement(main_controller, "stringProp", {"name": "LoopController.loops"}).text = "1"

    thread_group_hash_tree = ET.SubElement(test_plan_hash_tree, "hashTree")

    # Main API Test Sampler
    api_sampler = ET.SubElement(thread_group_hash_tree, "HTTPSamplerProxy", {
        "guiclass": "HttpTestSampleGui",
        "testclass": "HTTPSamplerProxy",
        "testname": "API Test",
        "enabled": "true"
    })
    ET.SubElement(api_sampler, "stringProp", {"name": "HTTPSampler.domain"}).text = "api.c021.eagleeyenetworks.com"
    ET.SubElement(api_sampler, "stringProp", {"name": "HTTPSampler.path"}).text = "api/v3.0/cameras"
    ET.SubElement(api_sampler, "stringProp", {"name": "HTTPSampler.method"}).text = "GET"

    # HashTree for API Sampler
    api_sampler_hash_tree = ET.SubElement(thread_group_hash_tree, "hashTree")

    # Header Manager with Dynamic Token, wrapped in its own HashTree
    header_manager = ET.SubElement(api_sampler_hash_tree, "HeaderManager", {
        "guiclass": "HeaderPanel",
        "testclass": "HeaderManager",
        "testname": "HTTP Header Manager",
        "enabled": "true"
    })
    headers_collection = ET.SubElement(header_manager, "collectionProp", {"name": "HeaderManager.headers"})
    header_element = ET.SubElement(headers_collection, "elementProp", {
        "name": "",
        "elementType": "Header"
    })
    ET.SubElement(header_element, "stringProp", {"name": "Header.name"}).text = "Authorization"
    ET.SubElement(header_element, "stringProp",
                  {"name": "Header.value"}).text = "Bearer ${BearerToken}"  # Ensure correct format

    # HashTree for Header Manager
    ET.SubElement(api_sampler_hash_tree, "hashTree")

    # Listener for results
    listener = ET.SubElement(test_plan_hash_tree, "ResultCollector", {
        "guiclass": "ViewResultsFullVisualizer",
        "testclass": "ResultCollector",
        "testname": "View Results Tree",
        "enabled": "true"
    })
    ET.SubElement(listener, "stringProp", {"name": "filename"}).text = "results.jtl"
    ET.SubElement(test_plan_hash_tree, "hashTree")

    # Save JMX file
    tree = ET.ElementTree(jmeter_test_plan)
    tree.write(JMX_FILE_PATH, xml_declaration=True, encoding='UTF-8')
    print(f"Created JMX file at {JMX_FILE_PATH}")


if __name__ == "__main__":
    create_jmx()
