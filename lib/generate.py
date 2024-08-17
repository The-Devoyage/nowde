import os
import logging
import google.generativeai as genai
from .api_builder import install_dependencies, format_files, generate_entrypoint, generate_controller_index, generate_controller, generate_services_index, generate_service, create_project_folder

logger = logging.getLogger(__name__)

"""
Returns the context of the directory. This is the content of the files in the directory.
Does not support nested directories.
"""
def get_context(path):
    logger.info(f"Getting context from path: {path}")
    context = []
    for root, dirs, files in os.walk(path):
        for file in files:
            context.append(os.path.join(root, file))
    content = []
    for c in context:
        with open(c, 'r') as f:
            data = {
                    "path": c,
                    "content": f.read()
                    }
            content.append(data)
    logger.info(f"Context: {content}")
    return content


"""
Returns the declarations for the functions that can be called to generate the API.
"""
def get_declarations():
    logger.info("Getting declarations.")
    generate_entrypoint = genai.protos.FunctionDeclaration(
        name='generate_entrypoint',
        description="Generates a node index file which starts a simple express server.",
    )
    generate_controller_index = genai.protos.FunctionDeclaration(
        name='generate_controller_index',
        description="Generates a controller index file which exports all the controllers. Only needs to be called once.",
        parameters=genai.protos.Schema(
            type=genai.protos.Type.OBJECT,
            properties={
                'controller_names':genai.protos.Schema(
                    type=genai.protos.Type.ARRAY,
                    items=genai.protos.Schema(type=genai.protos.Type.STRING),
                    description="List of controller names to export."
                )
            },
            required=['controller_names']
        )
    )
    generate_controller = genai.protos.FunctionDeclaration(
        name='generate_controller',
        description="Generates a node controller file. Can be called multiple times to create multiple controllers.",
        parameters=genai.protos.Schema(
            type=genai.protos.Type.OBJECT,
            properties={
                'controller_name':genai.protos.Schema(
                    type=genai.protos.Type.STRING,
                    description="Name of the controller."
                )
            },
            required=['controller_name']
        )
    )
    format_files = genai.protos.FunctionDeclaration(
        name='format_files',
        description="Formats the node_api directory using prettier."
    )
    install_dependencies = genai.protos.FunctionDeclaration(
        name='install_dependencies',
        description="Installs the necessary dependencies for the node_api directory.",
        parameters=genai.protos.Schema(
            type=genai.protos.Type.OBJECT,
            properties={
                'project_name':genai.protos.Schema(
                    type=genai.protos.Type.STRING,
                    description="Name of the project folder."
                )
            },
            required=['project_name']
        )
    )
    generate_services_index = genai.protos.FunctionDeclaration(
        name='generate_services_index',
        description="Generates a services index file which exports all the services. Only needs to be called once.",
        parameters=genai.protos.Schema(
            type=genai.protos.Type.OBJECT,
            properties={
                'service_names':genai.protos.Schema(
                    type=genai.protos.Type.ARRAY,
                    items=genai.protos.Schema(type=genai.protos.Type.STRING),
                    description="List of service names to export."
                ),
                'service_path':genai.protos.Schema(
                    type=genai.protos.Type.STRING,
                    description="Path to the services directory."
                )
            },
            required=['service_names']
        )
    )
    generate_service = genai.protos.FunctionDeclaration(
        name='generate_service',
        description="Generates a node service file. Can be called multiple times to create multiple services.",
        parameters=genai.protos.Schema(
            type=genai.protos.Type.OBJECT,
            properties={
                'service_name':genai.protos.Schema(
                    type=genai.protos.Type.STRING,
                    description="Name of the service."
                ),
                'uri':genai.protos.Schema(
                    type=genai.protos.Type.STRING,
                    description="URI of the service."
                ),
                'service_path':genai.protos.Schema(
                    type=genai.protos.Type.STRING,
                    description="Path to the services directory. Default is 'src/services'."
                ),
                'method':genai.protos.Schema(
                    type=genai.protos.Type.STRING,
                    description="HTTP method of the service. Default is GET."
                )
            },
            required=['service_name', 'uri']
        )
    )
    create_project_folder = genai.protos.FunctionDeclaration(
        name='create_project_folder',
        description="Creates a project folder for the API.",
        parameters=genai.protos.Schema(
            type=genai.protos.Type.OBJECT,
            properties={
                'project_name':genai.protos.Schema(
                    type=genai.protos.Type.STRING,
                    description="Path to create the project folder."
                )
            },
            required=['project_name']
        )
    )

    return [generate_entrypoint, generate_controller_index, generate_controller, format_files, install_dependencies, generate_services_index, generate_service, create_project_folder]


"""
Executes the function based on the function name returned from the model.
Arguments are passed to the function to generate the API - but they may not exist as some args are optional.
"""
def execute_function(fn, args):
    if fn.name == 'generate_entrypoint':
        port = args.get('port', 3000)
        controller_path = args.get('controller_path', 'controllers')
        generate_entrypoint(port, controller_path)
    elif fn.name == 'generate_controller_index':
        controller_path = args.get('controller_path', 'src/controllers')
        controller_names = args.get('controller_names', [])
        generate_controller_index(controller_names, controller_path)
    elif fn.name == 'generate_controller':
        controller_path = args.get('controller_path', 'src/controllers')
        controller_name = args.get('controller_name')
        generate_controller(controller_name, controller_path)
    elif fn.name == 'install_dependencies':
        project_name = args.get('project_name', 'node_api')
        install_dependencies(project_name)
    elif fn.name == 'format_files':
        format_files()
    elif fn.name == 'generate_services_index':
        service_names = args.get('service_names', [])
        service_path = args.get('service_path', 'src/services')
        generate_services_index(service_names, service_path)
    elif fn.name == 'generate_service':
        service_name = args.get('service_name')
        uri = args.get('uri')
        service_path = args.get('service_path', 'src/services')
        method = args.get('method', 'GET')
        generate_service(service_name, uri, service_path, method)
    elif fn.name == 'create_project_folder':
        project_name = args.get('project_name')
        create_project_folder(project_name)
    else:
        logger.error(f"Function {fn.name} not found.")

"""
Runs the application. This is the main function that is called to generate the API.
"""
def run(path="./test"):
    logger.info("Starting the application.")
    google_api_key = os.getenv('GOOGLE_API_KEY')

    declarations = get_declarations()
    context = get_context(path)

    genai.configure(api_key=google_api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash", tools=declarations)

    chat = model.start_chat()
    prompt = f"""
        Your job is to build APIs based on the context found in this directory.
        Build the API by generating the necessary files and code.

        Then, generate the necessary files and code to build the API by running the
        available functions.

        Rules:
            - Always create the project folder first.
            - Always install the necessary dependencies.
            - Always create the entrypoint file before generating controllers.
            - Always generate service index and controller index before generating individual services and controllers.
            - Always generate services before controllers.
            - Always format the code using prettier when all tasks are complete.

        Use the following context to generate the API:
            {context}
        """
    response = chat.send_message(prompt)

    logger.info("Response received.")
    logger.info(response)

    for part in response.parts:
        if fn := part.function_call:
            # Prompt the user if they want to execute the function.
            print(f"Function: {fn.name}")
            print("Arguments: ", fn.args)
            is_execute = input(f"Execute? (y/n): ")
            if is_execute != 'y':
                continue
                    
            execute_function(fn, fn.args)
