FROM python3.10

ENV GITHUB_TOKEN=${GITHUB_TOKEN}
ENV OPENAI_ORGANIZATION=${OPENAI_ORGANIZATION}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the source code
COPY . .

# Set the working directory
ENTRYPOINT [ "" ]