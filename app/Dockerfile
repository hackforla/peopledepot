# pull official base image
FROM python:3.10-bullseye

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get --no-install-recommends install -y \
  netcat=1.10-46 \
  gcc=4:10.2.1-1 \
  graphviz=2.42.2-5 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# install dependencies
RUN pip install --no-cache-dir pip~=21.3.1
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh \
  && chmod +x /usr/src/app/entrypoint.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
