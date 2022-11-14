# start by pulling the python image
FROM continuumio/miniconda3:latest

# switch working directory
WORKDIR /app

# Create the environment:
COPY tensorflow-apple-metal.yml .
RUN conda env create -f tensorflow-apple-metal.yml -n tensorflow
 
# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "tensorflow", "/bin/bash", "-c"]


# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
#ENTRYPOINT [ "python" ]
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "tensorflow", "python", "view.py"]

CMD ["view.py" ]
