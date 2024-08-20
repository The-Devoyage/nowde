# Nowde

Generate Node API with Gemini API. Generate an instant No(w)de API Now(de)!

## Introduction

Install and run the Nowde CLI to create an instant NodeJS/Express API from just about any description. You
can instantly consume the API in development or use it as a kickstart to your next project.

## Features

- Directory Based Context - Drop OpenAPI Spec, JSON Schema, or even a descriptive text file into 
a directory and have it automatically read into context when running the application.
- Creates a Node/Express JS API Instantly using Google Gemini
- Services are created for each endpoint found in context.
- Controllers are created for each entity.
- Routes are created for each service within each controller.

## Usage

### Build

1. Build

```
pyinstaller main.py
```

2. Add to path

```
cp ./dist/main/main /usr/bin/nowde
```

3. Run

```
nowde 
```

Custom Context Directory

```
nowde --context ./path_to_context_dir
```

### Run

```
python3 main.py --context ./path_to_context_dir
```


