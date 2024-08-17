import os
import logging
import json

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

        for controller_name in controller_names:
            # Convert from camel case to kebab case
            route_name = ''.join(['-' + i.lower() if i.isupper() else i for i in controller_name]).lstrip('-')
            f.write(f"router.use('/{route_name}', {controller_name});\n")
        f.write("\n")

        f.write("export default router;")
    logger.info("Controller index file generated successfully.")

def generate_controller(controller_name, controller_path='src/controllers'):
    logger.info(f"Generating node controller file for {controller_name}.")
    os.makedirs(f'{controller_path}', exist_ok=True)

    with open(f'{controller_path}/{controller_name}.js', 'w') as f:
        f.write("""
                import express from 'express';
                const router = express.Router();

                router.get('/', (req, res) => {
                    res.send('Hello World!');
                });

                export default router;
        """)

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
                export const {service_name} = async () => {{
                    const response = await fetch('{uri}', {{
                        method: '{method}',
                    }});
                    return await response.json();
                }};
        """)

    logger.info("Node service file generated successfully.")

