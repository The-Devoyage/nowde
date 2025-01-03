import os
import logging
import json
import inflect
from time import sleep

logger = logging.getLogger(__name__)

def create_project_folder(project_name="node_api"):
    logger.info(f"Creating project folder: {project_name}")
    try:
        os.makedirs(project_name, exist_ok=True)
        os.makedirs(f'{project_name}/src', exist_ok=True)
    except Exception as e:
        logger.error(f"Error creating project folder: {e}")

    os.chdir(project_name)
    logger.info("Project folder created successfully.")

def install_dependencies(project_name="node_api"):
    os.system('npm init -y')
    os.system('npm install express helmet cors nodemon')
    with open('package.json', 'r') as f:
        package_data = json.load(f)
    package_data["type"] = "module"
    package_data["name"] = project_name
    package_data["main"] = "src/index.js"
    package_data["scripts"] = {
        "start": "node src/index.js",
        "dev": "nodemon src/index.js"
    }
    with open('package.json', 'w') as f:
        json.dump(package_data, f, indent=2)


def format_files():
    # use prettier to format the node_api directory recursively
    os.system('npx prettier --write ./')

def generate_entrypoint(port=3000, controller_path='controllers'):
    logger.info("Generating entrypoint file.")

    with open('src/index.js', 'w') as f:
        f.write(f"""
                import express from 'express';
                import cors from 'cors';
                import helmet from 'helmet';
                import controllers from './{controller_path}/index.js';

                const app = express();
                const port = {port};

                app.use(helmet());
                app.use(cors());

                app.use('/', controllers);

                app.listen(port, () => {{
                    console.log(`Server is running on http://localhost:${{port}}`);
                }});
        """)

    logger.info("Node index file generated successfully.")

def generate_controller_index(controller_names, controller_path='src/controllers'):
    logger.info("Generating controller index file.")

    os.makedirs(f'{controller_path}', exist_ok=True)

    with open(f'{controller_path}/index.js', 'w') as f:
        f.write("""
        import express from 'express';
        """)

        for controller_name in controller_names:
            f.write(f"import {controller_name} from './{controller_name}.js';\n")
        f.write("\n")

        f.write("const router = express.Router();\n")

        f.write("\n")

        unique_controller_names = []

        for controller_name in controller_names:
            # Convert from camel case to kebab case
            route_name = ''.join(['-' + i.lower() if i.isupper() else i for i in controller_name]).lstrip('-')
            # Remove "-controller" from the route name
            route_name = route_name.replace('-controller', '')
            route_name = route_name.replace('get-', '')
            unique_controller_names.append(route_name)

        unique_singular_controller_names = []
        p = inflect.engine()
        for unique_name in unique_controller_names:
            # make it singlur using inflect
            singular_name = p.singular_noun(unique_name)

            # if inflect is unable to find singular name, then use the unique name
            if singular_name is False:
                singular_name = unique_name

            # if the singular name is unique, then use it
            if singular_name not in unique_singular_controller_names:
                logger.info(f"Unique name: {unique_name}, Singular name: {singular_name}")
                unique_singular_controller_names.append(singular_name)

        for controller_name, route_name in zip(controller_names, unique_singular_controller_names):
            f.write(f"router.use('/{route_name}', {controller_name});\n")

        f.write("\n")

        f.write("export default router;")
    logger.info("Controller index file generated successfully.")

def generate_controller(controller_name, services, controller_path='src/controllers', method='GET', endpoint=None):
    logger.info(f"Generating node controller file for {controller_name}.")
    os.makedirs(f'{controller_path}', exist_ok=True)

    if not services or len(services) == 0:
        logger.error("No services found. Please create services first.")
        return

    existing = ""

    #  remove the export default from the original file, if it exists
    controller_exists = os.path.exists(f'{controller_path}/{controller_name}.js')
    if controller_exists:
        with open(f'{controller_path}/{controller_name}.js', 'r') as f2:
            lines = f2.readlines()
        with open(f'{controller_path}/{controller_name}.js', 'w') as f2:
            f2.writelines(lines[:-1])
            existing = lines[:-1]

    sleep(1)

    with open(f'{controller_path}/{controller_name}.js', 'w') as f:
        service_imports = []
        for service in services:
            service_imports.append(f"import {{ {service} }} from '../services/{service}/index.js';")

        service_calls = []
        for service_name in services:
            service_calls.append(f"const {service_name}Data = await {service_name}({{params, body, query}});")
            service_calls.append(f"finalData['{service_name}'] = {service_name}Data;")
            service_calls.append("\n")

        dyn_endpoint = endpoint if endpoint else '/'

        if not controller_exists:
            f.write(f"""
                import express from 'express';
                const router = express.Router();
                {"".join(service_imports)}

            """)
        else:
            f.write("".join(service_imports))
            f.writelines(existing)

        f.write(f"""

            router.{method.lower()}('{dyn_endpoint}', async (req, res) => {{
                const {{ params, body, query }} = req;
                try {{
                    let finalData = {{}};
                    {"".join(service_calls)}
                    res.json(finalData);
                }} catch (error) {{
                    res.status(500).json({{ error: error.message }});
                }}
            }});

        """)

        f.write("export default router;")

    logger.info("Node controller file generated successfully.")
    
def generate_services_index(service_names, service_path='src/services'):
    logger.info("Generating services index file.")
    logger.info(f"Service path: {service_path}")
    logger.info(f"Service names: {service_names}")

    os.makedirs(f'{service_path}', exist_ok=True)

    with open(f'{service_path}/index.js', 'w') as f:
        for service_name in service_names:
            f.write(f"export * from './{service_name}/index.js';\n")

    logger.info("Services index file generated successfully.")

def generate_service(service_name, uri, service_path='src/services', method='GET'):
    logger.info(f"Generating node service file for {service_name}.")

    os.makedirs(f'{service_path}/{service_name}', exist_ok=True)

    with open(f'{service_path}/{service_name}/index.js', 'w') as f:
        f.write(f"""
                export const {service_name} = async ({{params, body, query}}) => {{
                        const search_query_string = new URLSearchParams(query).toString();

                        try {{
                            const response = await fetch(`{uri}` + search_query_string, {{
                                method: '{method}',
                                headers: {{
                                    'Content-Type': 'application/json'
                                }},
                                body: JSON.stringify(body)
                            }});

                            return await response.json();
                        }} catch (error) {{
                            console.error(error);
                            return {{ error: error.message }};
                        }}
                }};
        """)

    logger.info("Node service file generated successfully.")
