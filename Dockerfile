FROM public.ecr.aws/lambda/python:3.10

# set work directory
WORKDIR ${LAMBDA_TASK_ROOT}

# install dependencies
RUN pip install pip --upgrade

COPY requirements.txt ./
RUN pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# copy project
COPY . ${LAMBDA_TASK_ROOT}

EXPOSE 8080

# Command to run the lambda handler
CMD ["app.handler"]
