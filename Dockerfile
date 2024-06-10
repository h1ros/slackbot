FROM public.ecr.aws/lambda/python:3.10

# Copy function code
COPY app.py ${LAMBDA_TASK_ROOT}

# Install dependencies
COPY requirements.txt ./
RUN pip install pip --upgrade
RUN pip install -r requirements.txt

# Command to run the lambda handler
CMD ["app.handler"]
